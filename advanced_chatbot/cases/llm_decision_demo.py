from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate
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


def create_tool_prompt():
    return """You have access to the following tools:

    get_weather: Get the weather for a specific location.
    Input: location (str)

    calculate_age: Calculate age from birth year.
    Input: birth_year (int)

    When you need to use these tools:
    1. For questions about weather in a specific location
    2. For calculating age based on birth year

    For other questions, just respond directly.

    Question: {question}
    """


prompt = ChatPromptTemplate.from_template(create_tool_prompt())

# 创建 LLM 实例
llm = ChatOpenAI(
    model_name='deepseek-chat',
    openai_api_key=deepseek_api_key,
    openai_api_base='https://api.deepseek.com/v1/',
)

# 绑定工具
llm_with_tools = llm.bind_tools([get_weather, calculate_age])


def test_llm_decision_making():
    questions = [
        "What's the weather like in Beijing?",
        "If someone was born in 1990, how old are they?",
        "Tell me a joke about programming.",
        "Should I bring an umbrella to Shanghai?",  # 这也需要天气工具
    ]

    for question in questions:
        print(f"\nQuestion: {question}")

        # 1. 首先看看没有工具的 LLM 如何回答
        print("Response without tools:")
        response = llm.invoke(question)
        print(response)

        # 2. 然后看看有工具的 LLM 如何回答
        print("\nResponse with tools:")
        response = llm_with_tools.invoke(
            prompt.format_messages(question=question)
            )
        print(f"Tool used: {hasattr(response, 'tool_calls')}")
        if hasattr(response, 'tool_calls'):
            for tool_call in response.tool_calls:
                print(f"Tool: {tool_call['name']}")
                print(f"Arguments: {tool_call['args']}")
        print(f"Response: {response}")


if __name__ == "__main__":
    print("=== Testing LLM Decision Making ===")
    test_llm_decision_making()
