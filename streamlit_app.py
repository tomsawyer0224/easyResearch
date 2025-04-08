import streamlit as st


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
# stream = graph.astream({"topic":topic,}, thread, stream_mode="updates")["generate_report_plan"]["sections"]
st.write_stream(graph.astream({"topic":topic,}, thread, stream_mode="updates"))
st.write_stream(stream)
