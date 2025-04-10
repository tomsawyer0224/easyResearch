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
    # st.write("You've clicked the 'Generate report' button")
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

feedback = st.chat_input("type your feedback")

# topic = "Overview of the AI inference market with focus on Fireworks, Together.ai, Groq"
thread = {"configurable": {"thread_id": str(uuid.uuid4()),
                           "search_api": search_engine,
                           "planner_provider": "ollama",
                           "planner_model": model,
                           "writer_provider": "ollama",
                           "writer_model": model,
                           "max_search_depth": 1,
                           }}
topics = []
topics.append(topic)
st.write(topics[-1])
# topic_plan = graph.astream({"topic":topic,}, thread, stream_mode="updates")
async def on_plan():
    report_plan = graph.astream({"topic":topics[-1]}, thread, stream_mode="updates")
    # report_plan = topic_plan
    report_plan = await anext(report_plan)
    report_plan = report_plan.get("generate_report_plan").get("sections")
    st.markdown(format_sections(report_plan))

async def on_feedback():
    report_plan = graph.astream(Command(resume=feedback), thread, stream_mode="updates")
    report_plan = await anext(report_plan)
    report_plan = report_plan.get("generate_report_plan").get("sections")
    st.markdown(format_sections(report_plan))

async def on_report():
    report_plan = graph.astream(Command(resume=True), thread, stream_mode="updates")
    report_plan = await anext(report_plan)
    report_plan = report_plan.get("generate_report_plan").get("sections")
    st.markdown(format_sections(report_plan))

if topic:
    asyncio.run(on_plan())
if feedback:
    asyncio.run(on_feedback())
if st.session_state.generate_report:
    asyncio.run(on_report())

# report_plan_sections = graph.astream({"topic":topic,}, thread, stream_mode="updates")
# #["generate_report_plan"]["sections"]
# async def get_stream(event):
#     report_plan = await anext(report_plan_sections)
#     report_plan = report_plan.get("generate_report_plan").get("sections")
#     # return iter(format_sections(report_plan))
#     yield format_sections(report_plan)
#     # for c in format_sections(report_plan):
#     #     yield c
# st.write(get_stream(report_plan_sections))
# # st.write_stream(get_stream(report_plan_sections))
# # st.markdown(get_stream(report_plan_sections))