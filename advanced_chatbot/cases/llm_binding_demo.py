from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv
import os

load_dotenv()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")


@tool
def get_weather(location: str) -> str:
    """Get the weather for a specific location."""
    return f"The weather in {location} is sunny and 25°C"


@tool
def calculate_age(birth_year: int) -> str:
    """Calculate age from birth year."""
    current_year = 2025
    age = current_year - birth_year
    return f"A person born in {birth_year} is {age} years old"


# 创建 LLM 实例
llm = ChatOpenAI(
    model_name='deepseek-chat',
    openai_api_key=deepseek_api_key,
    openai_api_base='https://api.deepseek.com/v1/',
)

# 直接绑定工具，不需要手动创建 prompt
llm_with_tools = llm.bind_tools([get_weather, calculate_age])


def test_automatic_tool_binding():
    """测试自动绑定工具"""
    questions = [
        "What's the weather like in Beijing?",
        "If someone was born in 1990, how old are they?",
        "Tell me a joke about programming.",
        "Should I bring an umbrella to Shanghai?",
    ]
    for question in questions:
        print(f"\nQuestion: {question}") 
        # 直接发送问题，不需要额外的 prompt
        response = llm_with_tools.invoke(
            [HumanMessage(content=question)]
        )
        print(f"Has tool calls: {hasattr(response, 'tool_calls')}")
        if hasattr(response, 'tool_calls'):
            for tool_call in response.tool_calls:
                print(f"Tool: {tool_call['name']}")
                print(f"Arguments: {tool_call['args']}")
        print(f"Response: {response}")


if __name__ == "__main__":
    print("=== Testing Automatic Tool Binding ===")
    test_automatic_tool_binding()
