from langchain.chains.question_answering import load_qa_chain
from llm_setting import LLMSetting


class Reader(LLMSetting):
    def create_answer_at_a_time(self, query_related_component, query):
        chain = load_qa_chain(llm=self.llm)

        result = chain({"input_documents": query_related_component,
                        "question": query},
                       return_only_outputs=True)
        return result['output_text']