import os
from langchain_openai import ChatOpenAI


def get_llm(temperature=0, max_tokens=3000):
    model = ChatOpenAI(
        model="gpt-3.5-turbo-0125",
        temperature=temperature,
        max_tokens=max_tokens,
        max_retries=2,
        openai_api_key=os.environ['OPENAI_API_KEY'])
    return model
