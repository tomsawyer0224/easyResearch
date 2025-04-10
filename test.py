from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.graph import builder
import uuid 
import asyncio

# import logging

# logging.basicConfig(
#     # format="{asctime}::{levelname}::{name}::{message}",
#     format="[{levelname}]::{message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     level=logging.INFO,
# )


memory = MemorySaver()
graph = builder.compile(checkpointer=memory)


thread = {"configurable": {"thread_id": str(uuid.uuid4()),
                           "search_api": "duckduckgo",
                           #"search_api": "arxiv",
                           "planner_provider": "ollama",
                           "planner_model": "llama3.2:1b",
                           "writer_provider": "ollama",
                           "writer_model": "llama3.2:1b",
                           "max_search_depth": 1,
                           }}

topic = "Overview of the AI inference market with focus on Fireworks, Together.ai, Groq"
from open_deep_research.utils import format_sections
async def main():
    async for event in graph.astream({"topic":topic,}, thread, stream_mode="updates"):
        print(event)
        print("-"*50)
    print("-"*50)

    from langgraph.types import Command
    async for event in graph.astream(Command(resume="Include a revenue estimate (ARR) in the sections"), thread, stream_mode="updates"):
        print(event)

    print("-"*50)

    async for event in graph.astream(Command(resume=True), thread, stream_mode="updates"):
        print(event)
asyncio.run(main())
# if __name__=="__main__":
#     asyncio.run(main())