from langchain.text_splitter import CharacterTextSplitter
from llm_setting import LLMSetting
import json


class Splitter(LLMSetting):
    def __init__(self):
        self.text_splitter = CharacterTextSplitter(chunk_size=5000, chunk_overlap=0)
    
    def chunking_to_plaintext(self,full_text):
        if full_text == "":
            print("ERROR: text is empty.")
            exit()
        splitted_texts = self.text_splitter.split_text(full_text)
        return splitted_texts
    
if __name__=='__main__':
    from pathlib import Path
    current_dir = Path(__file__).parent
    source = str(current_dir) + "/mhi.txt"
    with open(source, encoding="utf-8") as f:
            full_text = f.read()
            
    # split開始
    splitter = Splitter()
    splitted_text = splitter.chunking_to_plaintext(full_text)

    # save
    output_json = json.dumps([[{"index": index, "content": content},] for index, content in enumerate(splitted_text)], ensure_ascii=False)
    save_path = str(current_dir) + "/splitted_texts.json"
    with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(output_json, f, indent=2, ensure_ascii=False)