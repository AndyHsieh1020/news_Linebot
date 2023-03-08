from __future__ import unicode_literals
from asyncio import events
from email import message
import os
from re import search
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackAction, URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate

import requests
import json
import time
import pymongo
import jieba

import configparser

import random

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


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    dblist = myclient.list_database_names()
    json_body = json.loads(str(event))

    '''keyword_dict = []
    path = 'userdict.txt'
    f = open(path, 'r')
    for line in f.readlines():
        line = line.replace('\n', "")
        keyword_dict.append(line)
    f.close()'''

    if "status" in dblist:
        print("已存在status.db")
    else:
        mydb = myclient["status"]
        mytable = mydb["user_status"]

    input_txt = json_body['message']['text']

    if '新手教學' == input_txt:
        temp_data = {"status": '訂閱關鍵字',"userid": json_body['source']['userId']}
    elif '優惠方案' == input_txt:
        status_flag = '解除訂閱關鍵字'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已解除訂閱x")
        )
    elif '會員專區' == input_txt:
        status_flag = '查詢帳戶資訊'

        line_bot_api.push_message(json_body['source']['userId'], TemplateSendMessage(
            alt_text='ButtonsTemplate',
            template=ButtonsTemplate(
                thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                title='OXXO.STUDIO',
                text='這是按鈕樣板',
                actions=[
                    PostbackAction(
                        label='加入',
                        data='加入'
                    ),
                    PostbackAction(
                        label='取消',
                        data='取消'
                    )
                ]
            )
        ))
    elif '訂閱內容' == input_txt:
        status_flag = '加入會員'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入姓名")
        )
        process_status = '輸入姓名'
        # user_data = {"userid": json_body['source']['userId'] , "姓名": "", "電話": "", "email": "","剩餘天數": 30,"訂閱方案": "","訂閱公司+關鍵字":"","訂閱開始時間":"" }
    elif '查詢修改' == input_txt:

        line_bot_api.push_message(json_body['source']['userId'], TemplateSendMessage(
            alt_text='ButtonsTemplate',
            template=ButtonsTemplate(
                thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                title='OXXO.STUDIO',
                text='這是按鈕樣板',
                actions=[
                    PostbackAction(
                        label='基本資料',
                        data='基本資料'
                    ),
                    PostbackAction(
                        label='方案',
                        data='方案'
                    ),
                    PostbackAction(
                        label='內容',
                        data='內容'
                    ),
                    PostbackAction(
                        label='修改資料',
                        data='修改資料'
                    )
                ]
            )
        ))

    elif '其它' == input_txt:

         line_bot_api.push_message(json_body['source']['userId'], TemplateSendMessage(
            alt_text='ButtonsTemplate',
            template=ButtonsTemplate(
                thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                title='OXXO.STUDIO',
                text='這是按鈕樣板',
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

    '''if "user" in dblist:
            print("資料庫存在！")
            mydb = myclient["users"]
            mytable = mydb["user_info"]
            search = { "userid":json_body['source']['userId'] }
            if mytable.count_documents(search)==0:
                mytable.insert_one(user_data)
            else:
                sub_keyword=mytable.find({ "user_id":json_body['source']['userId'] },{"訂閱公司+關鍵字":1})+','+
                newvalues = { "$set": { "訂閱公司+關鍵字":sub_keyword }}
                mytable.update_one(search, newvalues)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="已加入訂閱清單")
                )
        else:
            print("不存在該資料庫")
            mydb = myclient["user"]
            mytable = mydb["user_info"]
            mytable.insert_one(user_data)'''


if __name__ == "__main__":
    app.run()
