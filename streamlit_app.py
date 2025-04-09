import streamlit as st
from open_deep_research.utils import format_sections

def on_click_generate():
    st.write("You've clicked the 'Generate report' button")
with st.sidebar:
    model = st.selectbox(
        "Choose a model",
        ("llama3.2:1b", "qwen2.5:0.5b")
    )
    search_engine = st.selectbox(
        "Choose a search engine",
        ("duckduckgo", "arxiv")
    )
    topic = st.text_input(
    "Topic",
    )

    generate = st.button("Generate report", type = "primary", on_click=on_click_generate)

feedback = st.chat_input("feedback")

from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.graph import builder
import uuid 
import asyncio

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

thread = {"configurable": {"thread_id": str(uuid.uuid4()),
                           "search_api": search_engine,
                           "planner_provider": "ollama",
                           "planner_model": model,
                           "writer_provider": "ollama",
                           "writer_model": model,
                           "max_search_depth": 1,
                           }}
topic = "Overview of the AI inference market with focus on Fireworks, Together.ai, Groq"
report_plan_sections = graph.astream({"topic":topic,}, thread, stream_mode="updates")
#["generate_report_plan"]["sections"]
async def get_stream(event):
    report_plan = await anext(report_plan_sections)
    report_plan = report_plan.get("generate_report_plan").get("sections")
    # return iter(format_sections(report_plan))
    return format_sections(report_plan)

st.write_stream(iter(asyncio.run(get_stream(report_plan_sections))))