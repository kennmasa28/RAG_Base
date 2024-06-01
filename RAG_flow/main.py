from parser_class import Parser
from splitter_class import Splitter
from retriever_class import Retriever
from reader_class import Reader
from llm_setting import LLMSetting


def main():
    setting = LLMSetting()
    query = "三菱重工の歴代社長を教えてください"
    source_path = "langchain_py/mhi.txt"
    parser = Parser(source_path)
    full_text = parser.full_source_text
    splitter = Splitter()
    retriever = Retriever(setting)
    reader = Reader(setting)

    splitted_text = splitter.chunking_to_plaintext(full_text)
    print(splitted_text)
    query_related_component = retriever.retrieve_by_faiss(splitted_text, query)
    print(query_related_component)
    output = reader.create_answer_at_a_time(query_related_component, query)
    print(output)


if __name__ == "__main__":
    main()
