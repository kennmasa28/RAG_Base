from langchain.vectorstores.faiss import FAISS
from llm_setting import LLMSetting
import json

class Retriever():
    def __init__(self, setting):
        self.embeddings = setting.embeddings

    def retrieve_by_faiss(self, splitted_texts, query):
        retriever = FAISS.from_texts(splitted_texts, self.embeddings)
        query_related_component = retriever.similarity_search(query)
        return query_related_component

if __name__=='__main__':
    from pathlib import Path
    current_dir = Path(__file__).parent
    source = str(current_dir) + "/splitted_texts.json"
    with open(source, encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)
    print(data)