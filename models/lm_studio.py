from langchain_openai import ChatOpenAI


def get_llm(temperature=0, max_tokens=3000):
    # Point to the local server
    # return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    model = ChatOpenAI(
        openai_api_key="lm-studio",
        base_url="http://localhost:1234/v1",
        temperature=temperature,
        max_tokens=max_tokens)
    return model
