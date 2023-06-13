from __future__ import unicode_literals
from asyncio import events
from email import message
import os
from re import search
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackAction, URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate, PostbackEvent

import requests
import json
import datetime
import pymongo

now=datetime.datetime.now()
now=now.strftime('%Y-%M-%D %H:%M:%S')

import configparser

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'




# template 按鈕回呼
@handler.add(PostbackEvent)
def handle_postback(event):

    # 接收到 postback 事件時的處理邏輯
    data = event.postback.data



# 文字訊息擷取
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    dblist = myclient.list_database_names()

    if "user" in dblist:
        print("已存在user.db")
    else:
        mydb = myclient["user"]

    mydb = myclient["user"]
    mytable = mydb["user_info"]

    json_body = json.loads(str(event))
    input_txt = json_body['message']['text']


# 檢查用戶是否在存在在資料庫中
    if mytable.count_documents({'userid': json_body['source']['userId']}):

        myquery = {"userid": json_body['source']['userId']}
        mydoc = mytable.find_one(myquery)

        # 檢查用戶是否在正在輸入資料中
        if input_txt == "加入會員":

            line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入姓名"))

            newvalues = {"$set": {"status": "enter_name"}}
            mytable.update_one(myquery, newvalues)
            
        elif mydoc["status"] == "enter_name":
            newvalues = {"$set": {"status": "enter_id", "name": input_txt}}
            mytable.update_one(myquery, newvalues)
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage("請輸入身分證字號"))

        elif mydoc["status"] == "enter_id":
            newvalues = {"$set": {"status": "enter_phone", "id": input_txt}}
            mytable.update_one(myquery, newvalues)
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage("請輸入電話"))

        elif mydoc["status"] == "enter_phone":
            newvalues = {"$set": {"status": "enter_email", "phone": input_txt}}
            mytable.update_one(myquery, newvalues)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="輸入e-mail")
            )
        elif mydoc["status"] == "enter_email":
            newvalues = {"$set": {"status": "none", "email": input_txt}}
            mytable.update_one(myquery, newvalues)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="輸入完成")
            )

        if input_txt == "取消會員":
            myquery = {"userid": json_body['source']['userId']}
            mytable.delete_one(myquery)

    else:

        user_data = {"userid": json_body['source']['userId'],
                    "status": "none", "name": "none", "id":"none", "phone": "none", "email": "none", "in_day":now}
        mytable.insert_one(user_data)




    # richmenu選單
    if '新手教學' == input_txt:

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="移轉到網頁？")
        )
    elif '優惠方案' == input_txt:

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我不知道這樣做啥")
        )
    elif '會員專區' == input_txt:

        line_bot_api.push_message(json_body['source']['userId'], TemplateSendMessage(
            alt_text='ButtonsTemplate',
            template=ButtonsTemplate(
                thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                title='會員專區',
                text='會員專區',
                actions=[
                    MessageAction(
                        label='加入',
                        text='加入會員'
                    ),
                    MessageAction(
                        label='取消',
                        text='取消會員'
                    )
                ]
            )
        ))
    elif '訂閱內容' == input_txt:

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入您想訂閱的內容")
        )

    elif '查詢修改' == input_txt:

        line_bot_api.push_message(json_body['source']['userId'], TemplateSendMessage(
            alt_text='ButtonsTemplate',
            template=ButtonsTemplate(
                thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                title='查詢修改',
                text='查詢修改',
                actions=[
                    MessageAction(
                        label='基本資料',
                        text='基本資料'
                    ),
                    MessageAction(
                        label='方案',
                        text='方案'
                    ),
                    MessageAction(
                        label='內容',
                        text='內容'
                    ),
                    MessageAction(
                        label='修改資料',
                        text='修改資料'
                    )
                ]
            )
        ))

    elif '其它' == input_txt:

        line_bot_api.push_message(json_body['source']['userId'], TemplateSendMessage(
            alt_text='ButtonsTemplate',
            template=ButtonsTemplate(
                thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                title='其他功能',
                text='其他功能',
                actions=[
                    PostbackAction(
                        label='最新公告',
                        data='最新公告'
                    ),
                    PostbackAction(
                        label='聯絡我們',
                        data='聯絡我們'
                    )
                ]
            )
        ))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請按下方功能鍵互動")
        )


if __name__ == "__main__":
    app.run()
