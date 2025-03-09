class User: # 定義類別屬性名，進行類別宣告
    def __init__(self, userid, name, id, phone, email, in_day, category, status):
        self.category = ""
        self.status = ""
    
    def to_dict(self):
        return {"category":self.category, "status":self.status}

    def from_dict(data):
        return User(data["category"], data["status"])

