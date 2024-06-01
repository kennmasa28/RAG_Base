from LLM import ChatWithVectorStorIndex, ChatWithoutIndex
from pathlib import Path

current_dir = Path(__file__).parent
logfile = str(current_dir) + "/log/a.log"
index_dir = str(current_dir) + "/index"
savefile = str(current_dir) + "/results/result.json"


agent = ChatWithVectorStorIndex(logfile=logfile, similarity_top_k=3)
res = agent.GetAIResponse(query="三菱重工の歴代社長を答えよ", index_dir=index_dir, savefile=savefile)

# agent = ChatWithoutIndex()
# res = agent.GetAIResponseWithFunctions(query="みかん、ぶどう、バナナについて、在庫が0であるか調べ、在庫が0の場合は商品のサプライヤーに追加注文のメールを送ってください。")
print(res)
