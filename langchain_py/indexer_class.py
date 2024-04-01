from langchain.text_splitter import CharacterTextSplitter
from llm_setting import LLMSetting


class Indexer(LLMSetting):
    def __init__(self):
        self.text_splitter = CharacterTextSplitter(chunk_size=5000, chunk_overlap=0)
    
    def chunking_to_plaintext(self,full_text):
        if full_text == "":
            print("ERROR: text is empty.")
            exit()
        splitted_texts = self.text_splitter.split_text(full_text)
        return splitted_texts