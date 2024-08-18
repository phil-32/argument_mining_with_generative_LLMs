import os
from langchain_mistralai.chat_models import ChatMistralAI


def get_llm(temperature=0, max_tokens=3000):
    model = ChatMistralAI(mistral_api_key=os.environ['MISTRAL_API_KEY'],
                      model="open-mistral-7b",
                      temperature=temperature,
					  max_tokens=max_tokens,
					  api_key=os.environ['MISTRAL_API_KEY'])
    return model
