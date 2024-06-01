import os
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
import openai


class LLMSetting(object):
    def __init__(self):
        openai.api_key = os.environ["OPENAI_API_KEY"]

        # define llm
        self.llm = OpenAI(
            model_name="gpt-3.5-turbo-16k",
            temperature=0.2,
            top_p=1,
            max_tokens=8192,
            frequency_penalty=0,
            presence_penalty=0,
            n=1
        )
        self.embeddings = OpenAIEmbeddings()
