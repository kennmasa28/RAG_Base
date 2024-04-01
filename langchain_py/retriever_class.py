from langchain.vectorstores.faiss import FAISS
from llm_setting import LLMSetting


class Retriever(LLMSetting):
    def retrieve_by_faiss(self, splitted_texts, query):
        retriever = FAISS.from_texts(splitted_texts, self.embeddings)
        query_related_component = retriever.similarity_search(query)
        return query_related_component
