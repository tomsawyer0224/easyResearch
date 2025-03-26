from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_ollama import ChatOllama

from langchain_community.tools import DuckDuckGoSearchResults

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

llm = ChatOllama(model="llama3.2:1b")
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()
# print(graph)
# print(type(graph))
tool = DuckDuckGoSearchResults(
    max_results = 5,
    # output_format="list"
)

from utils import save_graph
save_graph(graph, "zxc.png")
# from PIL import Image
# from io import BytesIO
# from IPython.display import Image, display
# img = Image.open(graph.get_graph().draw_mermaid_png(), "r")
# Image.save(img, "abc.png")

# img_in_byte = graph.get_graph().draw_mermaid_png()
# img = Image.frombytes("L", (100, 100), img_in_byte)
# Image.save(img, "abc.png")
# with Image.open(BytesIO(img_in_byte)) as img:
#     img.save('abc.png')
# img = Image.open(BytesIO(img_in_byte))
# print(img)
# img.save('abc.png')

# try:
#     PIL.Image.save(PIL.Image.open((Image(graph.get_graph().draw_mermaid_png()))), "abc.png")
# except Exception:
#     # This requires some extra dependencies and is optional
#     pass

# print(tool.invoke("Who is current Prime Ministry of Canada"))