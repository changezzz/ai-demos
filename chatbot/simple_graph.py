from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# Define the state
class State(TypedDict):
    messages: list


# Create graph
workflow = StateGraph(State)


# Define a simple function
def chatbot(state):
    return {"messages": ["Response"]}


# Add nodes and edges
workflow.add_node("chatbot", chatbot)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# Compile the graph
graph = workflow.compile()

# Get and display the graph
graph_viz = graph.get_graph()
mermaid_graph = graph_viz.draw_mermaid()
print(mermaid_graph)
