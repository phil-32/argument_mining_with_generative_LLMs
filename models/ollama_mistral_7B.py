from langchain_community.chat_models import ChatOllama


def get_llm(temperature=0, max_tokens=3000):
    model = ChatOllama(model="mistral:v0.3",
                       temperature=temperature,
                       num_predict=max_tokens)
    return model
