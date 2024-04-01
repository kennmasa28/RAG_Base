import os
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import BSHTMLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import LLMChain
from langchain import PromptTemplate
from bs4 import BeautifulSoup
import requests
from parser_class import Parser
from llm_setting import LLMSetting


def main():
    query = "三菱重工の歴代社長を教えてください"
    source_path = "mhi.txt"
    parser = Parser(source_path)
    source_text = parser.full_source_text

    llm_instance = LLMSetting()
    query_related_component = llm_instance.GetQueryRelatedComponent(
        source_text, query)

    result = llm_instance.GetAIResponseWithSource(
        query_related_component, query)
    print(result)


if __name__ == "__main__":
    main()
