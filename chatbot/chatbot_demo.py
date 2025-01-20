from dotenv import load_dotenv
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

load_dotenv()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
llm = ChatOpenAI(
    model_name="deepseek-chat",
    openai_api_key=deepseek_api_key,
    openai_api_base="https://api.deepseek.com/v1/",
    max_tokens=1024,
    temperature=0.7,
)


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

if __name__ == "__main__":
    messages = [{"role": "user", "content": "你好，请介绍一下你自己"}]
    result = graph.invoke({"messages": messages})
    try:
        graph1 = graph.get_graph()
        try:
            # 获取 Mermaid 文本
            mermaid_text = graph1.draw_mermaid()
            print("Mermaid graph definition:")
            print(mermaid_text)

            # 使用 mermaid_converter 生成图片
            from mermaid_converter import mermaid_to_image

            if mermaid_to_image(mermaid_text, "graph.png", method="api"):
                print("Graph saved as 'graph.png'")
            else:
                print("Failed to generate graph image")

        except Exception as e:
            print(f"生成图片时出错: {e}")
    except Exception as e:
        print(f"获取图时出错: {e}")

    print("\nBot's response:")
    print(result["messages"][-1].content)


def stream_graph_updates(user_input: str):
    for event in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]}
    ):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


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
