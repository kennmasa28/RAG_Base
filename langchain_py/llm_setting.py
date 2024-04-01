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
import openai
from bs4 import BeautifulSoup
import requests


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

        self.text_splitter = CharacterTextSplitter(
            chunk_size=5000, chunk_overlap=0)
        self.embeddings = OpenAIEmbeddings()

    def GetQueryRelatedComponent(self, full_source_text, query):
        if full_source_text == "":
            print("ERROR")
            exit()
        splitted_texts = self.text_splitter.split_text(full_source_text) # chunking
        docsearch = FAISS.from_texts(splitted_texts, self.embeddings) # retriever
        query_related_component = docsearch.similarity_search(query)
        return query_related_component

    def GetAIResponseWithSource(self, input_source, query):
        chain = load_qa_chain(llm=self.llm)

        result = chain({"input_documents": input_source,
                        "question": query},
                       return_only_outputs=True)
        return result['output_text']
