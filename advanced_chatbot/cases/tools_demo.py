import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool

load_dotenv()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")


# 1. 定义两个简单的工具
@tool
def get_weather(location: str) -> str:
    """Get the weather for a specific location."""
    # 这里简化处理，实际应该调用天气 API
    return f"The weather in {location} is sunny and 25°C"


@tool
def calculate_age(birth_year: int) -> str:
    """Calculate age from birth year."""
    current_year = 2025
    age = current_year - birth_year
    return f"A person born in {birth_year} is {age} years old"


# 2. 创建两个 LLM 实例
llm_with_tools = ChatOpenAI(
    model_name="deepseek-chat",
    openai_api_key=deepseek_api_key,
    openai_api_base="https://api.deepseek.com/v1/",
).bind_tools([get_weather, calculate_age])

llm_without_tools = ChatOpenAI(
    model_name="deepseek-chat",
    openai_api_key=deepseek_api_key,
    openai_api_base="https://api.deepseek.com/v1/",
)


# 3. 测试两种情况
def test_llms():
    # 测试问题
    questions = [
        "What's the weather like in Beijing?",
        "If someone was born in 1990, how old are they?",
        "Tell me a joke about programming.",
    ]

    print("=== Testing LLM with bound tools ===")
    for question in questions:
        response = llm_with_tools.invoke(question)
        print(f"\nQ: {question}")
        print(f"A: {response}")
        print(f"Has tool calls: {hasattr(response, 'tool_calls')}")
        if hasattr(response, "tool_calls"):
            print("Tool calls:", response.tool_calls)

    print("\n=== Testing LLM without tools ===")
    for question in questions:
        response = llm_without_tools.invoke(question)
        print(f"\nQ: {question}")
        print(f"A: {response}")
        print(f"Has tool calls: {hasattr(response, 'tool_calls')}")


if __name__ == "__main__":
    test_llms()
