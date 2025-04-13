import streamlit as st
from open_deep_research.utils import format_sections
from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.graph import builder
from langgraph.types import Command
import uuid 
import asyncio
from typing import Any

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "final_report" not in st.session_state:
    st.session_state.final_report = False
def on_click_generate_report():
    st.session_state.final_report = True

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
    
    st.button("Generate report", type = "primary", on_click=on_click_generate_report)

feedback = st.chat_input("feedback on the plan")

async def generate_plan(topic: str, thread: dict[str, Any]):
    async for event in graph.astream({"topic": topic}, thread, stream_mode="updates"):
        for k, v in event.items():
            if k == "generate_report_plan":
                sections = format_sections(list(v.values())[0])
                return sections

async def process_feedback(feedback: str, thread: dict[str, Any]):
    async for event in graph.astream(Command(resume=feedback), thread, stream_mode="updates"):
        for k, v in event.items():
            if k == "generate_report_plan":
                sections = format_sections(list(v.values())[0])
                return sections

async def generate_report(thread):
    async for event in graph.astream(Command(resume=True), thread, stream_mode="updates"):
        for k, v in event.items():
            if k == "compile_final_report":
                final_report = list(v.values())[0]
                return final_report

async def research(topic: str):
    # plan
    st.chat_message("user").markdown(topic)
    st.session_state.messages.append({"role": "user", "content": topic})
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
    with st.spinner("Generating report plan...", show_time=True):
        # plan = asyncio.run(generate_plan(topic, thread))
        original_plan = await generate_plan(topic, thread)
        with st.chat_message("assistant"):
            st.markdown(original_plan)
        st.session_state.messages.append({"role": "assistant", "content": original_plan})

    # feedback
    if feedback:
        st.chat_message("user").markdown(feedback)
        st.session_state.messages.append({"role": "user", "content": feedback})
        with st.spinner("Processing your feedback...", show_time=True):
            new_plan = await process_feedback(feedback, thread)
            with st.chat_message("assistant"):
                st.markdown(new_plan)
            st.session_state.messages.append({"role": "assistant", "content": new_plan})

    # final report
    if st.session_state.final_report:
        thread = st.session_state.thread
        st.write(f"thread: {thread}")
        with st.spinner("Generating the final report...", show_time=True):
            final_report = await generate_report(thread)
            with st.chat_message("assistant"):
                st.markdown(final_report)
            st.session_state.messages.append({"role": "assistant", "content": final_report})
        st.session_state.final_report = False
if topic not in st.session_state:
    st.session_state.topic = None
if topic:
    st.session_state.topic = topic
if st.session_state.topic is not None:
    asyncio.run(research(st.session_state.topic))