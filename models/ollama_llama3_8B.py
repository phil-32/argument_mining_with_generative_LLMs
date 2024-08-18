from langchain_community.chat_models import ChatOllama


def get_llm(temperature=0, max_tokens=3000):
    model = ChatOllama(model="llama3:8b",
                       temperature=temperature,
                       num_predict=max_tokens)
    return model
