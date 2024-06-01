from LLM import ChatWithVectorStorIndex, ChatWithoutIndex
from pathlib import Path

current_dir = Path(__file__).parent
index_dir = str(current_dir) + "/index"
save_dir = str(current_dir) + "/results"


agent = ChatWithVectorStorIndex(model="gpt-4",
                                similarity_top_k=3)
res = agent.GetAIResponse(query="三菱重工の2019年からの社長は誰か", 
                          index_dir=index_dir, 
                          save_dir=save_dir)

# agent = ChatWithoutIndex()
# res = agent.GetAIResponseWithFunctions(query="みかん、ぶどう、バナナについて、在庫が0であるか調べ、在庫が0の場合は商品のサプライヤーに追加注文のメールを送ってください。")
print(res)
