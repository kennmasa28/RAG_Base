import json

class StockMail(object):
    def __init__(self):
        self.stock = [
        {"item": "みかん", "stock": 0, "supplier_for_item": "温州コーポレーション"},
        {"item": "りんご", "stock": 10, "supplier_for_item": "ハローKiddy Industory"},
        {"item": "バナナ", "stock": 0, "supplier_for_item": "The Donkey Foods"},
        {"item": "パイナップル", "stock": 1000, "supplier_for_item": "ペンパイナッポー流通"},
        {"item": "ぶどう", "stock": 100, "supplier_for_item": "グレープ Fruits inc."},
        ]

        # 呼び出し可能な関数の定義
        self.functions_list=[
            # 在庫チェック関数の定義
            {
                # 関数名
                "name": "inventory_search",
                # 関数の説明
                "description": "在庫商品を検索します。商品名は必ずカンマ区切りである必要があります。",
                # 関数の引数の定義
                "parameters": {
                    "type": "object",
                    "properties": {
                        "inventory_names": {
                            "type": "string",
                            "description": "検索文字列",
                        },
                    },
                    # 必須引数の定義
                    "required": ["input"],
                },
            },
            # メール送信関数の定義
            {
                # 関数名
                "name": "send_mail",
                # 関数の説明
                "description": "サプライヤにメールします。メールは一度に１人にしか送れません",
                # 関数の引数の定義
                "parameters": {
                    "type": "object",
                    "properties": {
                        "supplier_name": {
                            "type": "string",
                            "description": "商品のサプライヤー",
                        },
                        "message_body": {
                            "type": "string",
                            "description": "サプライヤーへのメッセージ",
                        },
                        "items": {
                            "type": "string",
                            "description": "サプライヤーに通知する商品名。商品は一度に１つしか指定できません",
                        },
                    },
                    # 必須引数の定義
                    "required": ["item_shortage"],
                },
            },
        ]

    # 在庫チェック関数
    def inventory_search(self, arguments):
        # 名前で在庫を探す
        inventory_names = json.loads(arguments)["inventory_names"]
        inventories = []
        for x in inventory_names.split(","):
            inventories.append(next((item for item in self.stock if item["item"] == x), None))

        return json.dumps(inventories)
    
    # メール送信関数
    def send_mail(self, arguments):
        args = json.loads(arguments)
        print("""
            mail sent as follows
            =====
            {}さま
            いつもお世話になっております。
            商品名：{}
            {}
            よろしくお願いします。

            """.format(args["supplier_name"], args["items"], args["message_body"]))
        return json.dumps({"status": "success"})
    


