import chainlit as cl
from chainlit.input_widget import Select

from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.graph import builder

import uuid 

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Select(
                id="model",
                label="Model",
                values=["llama3.2:1b", "qwen2.5:0.5b"],
                initial_index=0,
            ),
            Select(
                id="search_engine",
                label="Search Engine",
                values=["duckduckgo", "arxiv"],
                initial_index=0,
            ),
            Select(
                id="research_action",
                label="Research Action",
                values=["new topic", "feedback", "generate report"],
                initial_index=0,
            ),
        ]
    ).send()
    model = settings["model"]
    search_engine = settings["search_engine"]
    reseach_action = settings["research_action"]
    thread = {"configurable": {"thread_id": "abc",
                           "search_api": search_engine,
                           "planner_provider": "ollama",
                           "planner_model": model,
                           "writer_provider": "ollama",
                           "writer_model": model,
                           "max_search_depth": 1,
                           }
            }
    cl.user_session.set("thread", thread)

@cl.on_message
async def on_message(msg: cl.Message):
    thread = cl.user_session.get("thread")
    
    final_answer = cl.Message(content="")
    # print(msg.content)
    async for event in graph.astream({"topic": msg.content}, thread, stream_mode="updates"):
        # await final_answer.stream_token(msg.content)
        print(event)

    await final_answer.send()
