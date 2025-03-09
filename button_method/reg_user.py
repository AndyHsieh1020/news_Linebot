from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackAction, URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate, PostbackEvent

import redis
import pymongo
import json
import yaml
import datetime
import configparser

from class_def.user import User

config = configparser.ConfigParser()
config.read('..config.ini')

now=datetime.datetime.now()
now=now.strftime('%Y-%M-%D %H:%M:%S')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dblist = myclient.list_database_names()

if "stock_news_app" in dblist:
    print("已存在stock_news_app")
else:
    mydb = myclient["stock_news_app"]

mydb = myclient["stock_news_app"]
user_info_table = mydb["user_info"]
user_sub_topics_table = mydb["user_sub_topic"]

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))

with open("conversation.yaml", "r", encoding="utf-8") as file:
    dialog_flow = yaml.safe_load(file)
        
def reg_step(step, event):

    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    new_user = r.get(json_body['source']['userId'])[0]
    new_user_status = r.get(json_body['source']['userId'])[2]


    json_body = json.loads(str(event))
    input_txt = json_body['message']['text']

    if step == "加入會員":
        new_user_status = "enter_name"
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入姓名"))
        
    elif step == "enter_name":
        new_user.name = input_txt
        new_user_status = "enter_id"
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage("請輸入身分證字號"))

    elif step == "enter_id":
        new_user.id = input_txt
        new_user_status = "enter_phone"
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage("請輸入電話"))

    elif step == "enter_phone":
        new_user.phone = input_txt
        new_user_status = "enter_email"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="輸入e-mail")
        )
    elif step == "enter_email":
        new_user.email = input_txt
        new_user.in_day = now
        new_user_status = "none"
        user_info_table.insert_one(new_user)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="輸入完成")
        )
        

    

    
    
    


