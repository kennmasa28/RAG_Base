import os
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import BSHTMLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import LLMChain
from langchain import PromptTemplate
from bs4 import BeautifulSoup
import requests


class Parser():

    def __init__(self, source_path):
        self.source_path = source_path
        if source_path.endswith(".txt"):
            self.full_source_text = self.GetSourceFromText()
        else:
            self.full_source_text = ""

    def GetSourceFromText(self):
        with open(self.source_path, encoding="utf-8") as f:
            input_txt = f.read()
        return input_txt

    def GetSourceFromCSV(self):
        loader = CSVLoader(file_path=self.source_path, csv_args={
            'delimiter': ',',
            'quotechar': '"',
            'fieldnames': ['year', 'sell', 'profit']
        })
        data = loader.load()
        return data

    def GetSourceFromHTML(self):
        response = requests.get(self.source_path)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser',
                             from_encoding='utf-8')
        text_content = soup.get_text()
        return text_content
