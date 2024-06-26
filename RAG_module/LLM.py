import os
import json
import openai
import datetime
from llama_index import(
    SimpleDirectoryReader,
    GPTVectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    ServiceContext,
    PromptHelper
)
from llama_index.embeddings import LangchainEmbedding
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from llama_index.indices.service_context import ServiceContext

openai.api_key = os.environ["OPENAI_API_KEY"]
import logging
from logging import DEBUG
import re
import functions

class ChatWithoutIndex(object):
    def __init__(self, model="gpt-3.5-turbo-16k", temperature=0.2, max_tokens=4096, top_p=1.0, frequency_penalty=0, presence_penalty=0.6):
        self.model = model
        self.temperature = temperature
        self.max_tokens=max_tokens
        self.top_p=top_p
        self.frequency_penalty=frequency_penalty
        self.presence_penalty=presence_penalty
        self.chat_history = []
    
    def GetAIResponse(self, query, show_flag=False, savefile=''):
        self.chat_history.append({"role":"user", "content": query})
        response =openai.ChatCompletion.create(
            model = self.model,
            temperature = self.temperature,
            max_tokens = self.max_tokens,
            top_p = self.top_p,
            messages = self.chat_history
        )

        response_text = str(response.choices[0].message['content'])
        if show_flag:
            print(response_text)
        if savefile!='':
            with open(savefile, 'w') as f:
                json.dump(response, f, indent=2, ensure_ascii=False)
        return response_text

    def GetAIResponseWithFunctions(self, query, show_flag=False, savefile=''):
        self.chat_history.append({"role":"user", "content": query})
        flist = functions.StockMail()
        response =openai.ChatCompletion.create(
            model = self.model,
            temperature = self.temperature,
            max_tokens = self.max_tokens,
            top_p = self.top_p,
            messages = self.chat_history,
            functions=flist.functions_list,
            function_call="auto",
        )

        response_text = str(response.choices[0].message['content'])
        if show_flag:
            print(response_text)
        if savefile!='':
            with open(savefile, 'w') as f:
                json.dump(response, f, indent=2, ensure_ascii=False)
        return response_text


class ChatWithVectorStorIndex(object):
    def __init__(self, model="gpt-3.5-turbo-16k", temperature=0.2, max_tokens=4096, top_p=1.0, frequency_penalty=0, presence_penalty=0.6,
                 embedding_model='text-embedding-ada-002', chunk_overlap_rate=0.1, chunk_size_limit=1024, num_output=512, similarity_top_k=1):
        # LLM
        self.model = model
        self.temperature = temperature
        self.max_tokens=max_tokens
        self.top_p=top_p
        self.frequency_penalty=frequency_penalty
        self.presence_penalty=presence_penalty
        llm = ChatOpenAI(model = self.model,
                        temperature = self.temperature,
                        max_tokens = self.max_tokens,
                         model_kwargs={"top_p": self.top_p}
                        )
        # Embedding
        self.embedding_model = embedding_model
        embedding_llm = LangchainEmbedding(
                        OpenAIEmbeddings(
                            model=self.embedding_model,
                        ),
                        embed_batch_size=1,
                    )
        #Prompt Helper
        self.chunk_overlap_rate=chunk_overlap_rate
        self.chunk_size_limit=chunk_size_limit
        self.num_output = num_output
        self.similarity_top_k = similarity_top_k
        prompt_helper = PromptHelper(
            chunk_overlap_ratio=chunk_overlap_rate,
            chunk_size_limit=self.chunk_size_limit,
            num_output=self.num_output
        )
        # Service Context
        self.service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embedding_llm,
            prompt_helper=prompt_helper
        )
    
    def indexing_from_documents(self, documents_dir, index_dir):
        documents = SimpleDirectoryReader(documents_dir).load_data()
        index = GPTVectorStoreIndex.from_documents(
            documents, service_context=self.service_context
        )
        index.storage_context.persist(index_dir)
        with open(index_dir + "/docstore.json", "wt", encoding='utf-8') as f:
            json.dump(index.storage_context.docstore.to_dict(), f, indent=2, ensure_ascii=False)

    def GetAIResponse(self, query, index_dir, show_flag=False, save_dir=''):
        #Log
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        if save_dir != "":
            self.logfile = save_dir + "/log_" + nowtime + ".log"
            logging.basicConfig(level=DEBUG, filename=self.logfile, encoding='utf-8')
        storage_context = StorageContext.from_defaults(persist_dir=index_dir)
        index = load_index_from_storage(storage_context)
        with open(index_dir + "/docstore.json", "wt", encoding='utf-8') as f:
            json.dump(index.storage_context.docstore.to_dict(), f, indent=2, ensure_ascii=False)
        query_engine = index.as_query_engine(service_context=self.service_context, 
                                             similarity_top_k = self.similarity_top_k,
                                             response_modes="refine")
        # response mode :https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/response_modes/
        response = query_engine.query(query)
        response_text = str(response)
        if show_flag:
            print(response_text)
        
        # クエリとアウトプットをjsonに保存
        if save_dir!='':
            savefile = save_dir + "/result_" + nowtime + ".json"
            content = [{'query': query, 'response': response_text}]
            with open(savefile, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)

        # 引用テキストを保存
        if save_dir!="":
            self.LoadLog(self.logfile, index_dir, save_dir, nowtime)
        return response_text
    
    def LoadLog(self, log_path, index_dir, save_dir, nowtime):
        with open(log_path, 'r', encoding='utf-8') as f:
            logtext = f.read()
        pattern = r'\[Node ([a-f0-9\-]+)\]'
        nodes = re.findall(pattern, logtext)
        with open(index_dir + "/docstore.json", 'r', encoding='utf-8') as file:
            logtext = json.load(file)
        cited_text = []
        for i in range(len(nodes)):
            index = str(nodes[i])
            cited_text.append(logtext['docstore/data'][index]['__data__']['text'])
        cited_text_filename = save_dir + "/citation_" + nowtime + ".txt"
        with open(cited_text_filename, 'w', encoding='utf-8') as f:
            for context in cited_text:
                f.write(context)
                f.write("\n---------\n\n")





    