from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_ollama import ChatOllama
from langchain import hub
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

from utils import save_graph
SYSTEM_MESSAGE = (
    "You are a helpful, respectful and honest assistant. "
    "Always answer as helpfully as possible, while being safe. "
    "Your answers should not include any harmful, unethical, "
    "racist, sexist, toxic, dangerous, or illegal content. "
    "Please ensure that your responses are socially unbiased and positive in nature."
    "\n\nIf a question does not make any sense, or is not factually coherent, "
    "explain why instead of answering something not correct. "
    "For current events, you should use the tools to search on the internet. "
    "You may not use the tools for every query, the user may need to chat with you. "
    "If you don't know the answer to a question, "
    "don't share false information."
)

model = ChatOllama(model="llama3.2:1b", temperature = 0)
# model = ChatOllama(model="gemma3:1b", temperature = 0)
search = DuckDuckGoSearchResults()
tools = [search]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_MESSAGE),
        # ("human", "{question}")
    ]
)
# graph = create_react_agent(model, tools)
graph = create_react_agent(model, tools, prompt=SYSTEM_MESSAGE)


# save_graph(graph, "abc.png")

# def stream_graph_updates(user_input: str):
#     for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content)

# while True:
#     try:
#         user_input = input("User: ")
#         if user_input.lower() in ["quit", "exit", "q"]:
#             print("Goodbye!")
#             break

#         stream_graph_updates(user_input)
#     except:
#         # fallback if input() is not available
#         user_input = "What do you know about LangGraph?"
#         print("User: " + user_input)
#         stream_graph_updates(user_input)
#         break

# inputs = {"messages": [("user", "Who created you?")]}
# inputs = {"messages": [("user", "Tell me about the earth quake in myanma")]}
inputs = {
    "messages": [
    ("user", "Who is Prime Minister of Canada?"),
    ("user", "Tell me more about him?")
    ]
}
# inputs = {"messages": [("user", "My name is Tom, what is your name?")]}
# graph.invoke(inputs)
for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
       message.pretty_print()