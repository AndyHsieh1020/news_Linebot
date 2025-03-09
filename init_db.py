import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dblist = myclient.list_database_names()

if "user" in dblist:
        print("已存在user.db")
else:
    mydb = myclient["user"]

mydb = myclient["user"]
mytable = mydb["user_info"]

# user_data = {"userid": json_body['source']['userId'], "目前用戶對話狀態":"", "姓名": "", "電話": "", "email": "","剩餘天數": 30,"訂閱方案": "","訂閱公司+關鍵字":"","訂閱開始時間":"" }
user_data = {"userid": "test", "status": "none", "name":"none", "phone":"none", "email":"none", "day_left":0, "sub_plan":"none", "sub_com_key":"none", "sub_start":"none" }
mytable.insert_one(user_data)

