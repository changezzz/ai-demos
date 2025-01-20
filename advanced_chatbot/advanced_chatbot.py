"""
An advanced chatbot implementation using LangGraph and Tavily search
integration.
This module implements a graph-based conversational agent that can perform web
searches
and maintain contextual conversations using LangGraph's StateGraph
architecture.
"""

import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from basic_node import BasicToolNode

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 API keys
tavily_api_key = os.getenv("TAVILY_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

tool = TavilySearchResults(max_results=2)
tools = [tool]
result = tool.invoke("What's a 'node' in LangGraph?")
print(result)


class State(TypedDict):
    """
    State dictionary for the chatbot.
    """
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


llm = ChatOpenAI(
    model_name="deepseek-chat",
    openai_api_key=deepseek_api_key,
    openai_api_base="https://api.deepseek.com/v1/",
    max_tokens=1024,
    temperature=0.7,
)
# Modification: tell the LLM which tools it can call
llm_with_tools = llm.bind_tools(tools)  # 这就是langchain基于llm做的增强


def chatbot(state: State):
    """
    State dictionary for the chatbot.
    messages: Annotated[list, add_messages]
    """
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)

tool_node = BasicToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)


def route_tools(
    state: State,
):
    """
    Determine whether to route to the tools node based on the state.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(
            f"No messages found in input state to tool_edge: {state}"
        )
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", END: END},
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()
child_graph = graph.get_graph()
print(child_graph.draw_mermaid())


def stream_graph_updates(user_input_content: str):
    """
    Stream graph updates and print assistant responses.
    """
    for event in graph.stream(
        {
            "messages": [
                {"role": "user", "content": user_input_content}
            ]
        }
    ):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except Exception:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
