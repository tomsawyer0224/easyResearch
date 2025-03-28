from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_ollama import ChatOllama
from utils import save_graph

model = ChatOllama(model="llama3.2:1b", temperature = 0)
search = DuckDuckGoSearchResults()
tools = [search]



graph = create_react_agent(model, tools=tools)

# save_graph(graph, "abc.png")

# inputs = {"messages": [("user", "Who is current prime ministry of Canada?")]}
# print(graph.invoke(inputs))


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break