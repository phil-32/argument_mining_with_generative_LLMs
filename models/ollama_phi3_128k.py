from langchain_community.chat_models import ChatOllama


def get_llm(temperature=0, max_tokens=3000):
    model = ChatOllama(model="phi3:3.8b-mini-128k-instruct-q4_K_M",
                       temperature=temperature,
                       num_predict=max_tokens)
    return model
