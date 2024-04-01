from LLM import ChatWithVectorStorIndex, ChatWithoutIndex

# cvs = ChatWithVectorStorIndex(logfile='a.log', similarity_top_k=1)
# res = cvs.GetAIResponse(query="三菱重工の歴代社長を答えよ", index_dir="index")

agent = ChatWithoutIndex()
res = agent.GetAIResponseWithFunctions(query="みかん、ぶどう、バナナについて、在庫が0であるか調べ、在庫が0の場合は商品のサプライヤーに追加注文のメールを送ってください。")
print(res)
