import streamlit as st
from open_deep_research.utils import format_sections
from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.graph import builder
from langgraph.types import Command
from langgraph.graph.state import CompiledStateGraph
import uuid 
import asyncio
from typing import Any, cast

from utils import parse_config, pull_model

st.set_page_config("eResearcher", page_icon="./public/einstein.png")

# pull ollama models
config = parse_config("./config.yaml")
models = config["models"]
pull_model(models)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

if "thread" not in st.session_state:
    st.session_state.thread = None
if "graph" not in st.session_state:
    st.session_state.graph = graph
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    avatar = "./public/blobstudent.png" if message["role"]=="user" else "./public/einstein.png"
    with st.chat_message(message["role"], avatar = avatar):
        st.markdown(message["content"])

if "final_report" not in st.session_state:
    st.session_state.final_report = False
def on_click_generate_report():
    st.session_state.final_report = True

with st.sidebar:
    model = st.selectbox(
        "Choose a model",
        models
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

# function to generate an original plan
async def generate_plan(graph: CompiledStateGraph, topic: str, thread: dict[str, Any]):
    async for event in graph.astream({"topic": topic}, thread, stream_mode="updates"):
        for k, v in event.items():
            if k == "generate_report_plan":
                sections = format_sections(list(v.values())[0])
                return sections

# function to process any feeback on the plan
async def process_feedback(graph: CompiledStateGraph, feedback: str, thread: dict[str, Any]):
    async for event in graph.astream(Command(resume=feedback), thread, stream_mode="updates"):
        for k, v in event.items():
            if k == "generate_report_plan":
                sections = format_sections(list(v.values())[0])
                return sections

# function to generate the final report
async def generate_report(graph: CompiledStateGraph, thread):
    async for event in graph.astream(Command(resume=True), thread, stream_mode="updates"):
        for k, v in event.items():
            if k == "compile_final_report":
                final_report = list(v.values())[0]
                return final_report

# topic to research
if topic:
    st.session_state.topic = topic
    st.chat_message("user", avatar = "./public/blobstudent.png").markdown(topic)
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
    st.session_state.thread = thread
    # generate the an original plan
    with st.spinner("Generating report plan...", show_time=True):
        original_plan = "Here's my plan\n"+asyncio.run(generate_plan(st.session_state.graph, topic, thread))
        with st.chat_message("assistant", avatar = "./public/einstein.png"):
            st.markdown(original_plan)
        st.session_state.messages.append({"role": "assistant", "content": original_plan})

# feedback to modify the plan
if feedback:
    st.chat_message("user", avatar = "./public/blobstudent.png").markdown(feedback)
    st.session_state.messages.append({"role": "user", "content": feedback})
    thread = st.session_state.thread
    with st.spinner("Processing your feedback...", show_time=True):
        new_plan = "Here's my plan\n"+asyncio.run(process_feedback(st.session_state.graph, feedback, thread))
        with st.chat_message("assistant", avatar = "./public/einstein.png"):
            st.markdown(new_plan)
        st.session_state.messages.append({"role": "assistant", "content": new_plan})

# generate the final report
if st.session_state.final_report:
    thread = st.session_state.thread
    with st.spinner("Generating the final report...", show_time=True):
        final_report = "Here's the final report\n"+asyncio.run(generate_report(st.session_state.graph, thread))
        with st.chat_message("assistant", avatar = "./public/einstein.png"):
            st.markdown(final_report)
        st.session_state.messages.append({"role": "assistant", "content": final_report})
    st.session_state.final_report = False
