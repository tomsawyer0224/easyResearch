import streamlit as st
from open_deep_research.utils import format_sections
from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.graph import builder
from langgraph.types import Command
import uuid 
import asyncio

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

if "generate_report" not in st.session_state:
    st.session_state.generate_report = False
def on_click_generate():
    st.session_state.generate_report = True
with st.sidebar:
    model = st.selectbox(
        "Choose a model",
        ("llama3.2:1b", "qwen2.5:0.5b")
    )
    search_engine = st.selectbox(
        "Choose a search engine",
        ("duckduckgo", "arxiv")
    )
    topic = st.chat_input(
    "type your topic",
    )
    
    generate = st.button("Generate report", type = "primary", on_click=on_click_generate)

feedback = st.chat_input("feedback on the plan")

# topic = "Overview of the AI inference market with focus on Fireworks, Together.ai, Groq"

async def research(topic):
    thread = {
        "configurable": {
            "thread_id": str(uuid.uuid4()),
            "search_api": search_engine,
            "planner_provider": "ollama",
            "planner_model": model,
            "writer_provider": "ollama",
            "writer_model": model,
            "max_search_depth": 1,
        }
    }
    st.write(topic)

    async for event in graph.astream({"topic": topic}, thread, stream_mode="updates"):
        for k, v in event.items():
            if k == "generate_report_plan":
                sections = format_sections(list(v.values())[0])
                st.markdown(sections)
    # feedback
    while not st.session_state.generate_report:
        if feedback:
            async for event in graph.astream(Command(resume=feedback), thread, stream_mode="updates"):
                for k, v in event.items():
                    if k == "generate_report_plan":
                        sections = format_sections(list(v.values())[0])
                        st.markdown(sections)

    # write the final report
    if st.session_state.generate_report:
        async for event in graph.astream(Command(resume=True), thread, stream_mode="updates"):
            for k, v in event.items():
                if k == "compile_final_report":
                    final_report = list(v.values())[0]
                    st.markdown(final_report)
        st.session_state.generate_report = False
if topic:
    asyncio.run(research(topic))
