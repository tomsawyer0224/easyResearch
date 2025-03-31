from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.graph import builder

import asyncio

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

import uuid 
thread = {"configurable": {"thread_id": str(uuid.uuid4()),
                           "search_api": "duckduckgo",
                           "planner_provider": "ollama",
                           "planner_model": "llama3.2:1b",
                           "writer_provider": "ollama",
                           "writer_model": "llama3.2:1b",
                           "max_search_depth": 1,
                           }}

topic = "Overview of the AI inference market with focus on Fireworks, Together.ai, Groq"

async def main():
    async for event in graph.astream({"topic":topic,}, thread, stream_mode="updates"):
        print(event)

if __name__=="__main__":
    asyncio.run(main())