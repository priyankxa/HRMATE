
from langchain_ollama import ChatOllama


def create_llm():
    return ChatOllama(
        model="llama3.2",
        temperature=0
    )


def test_llm():
    llm = create_llm()
    response = llm.invoke(
        "Introduce yourself in one short sentence."
    )
    print("AI Response:")
    print(response.content)


if __name__ == "__main__":
    test_llm()
