from __future__ import unicode_literals

from re import search
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackAction, URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate, PostbackEvent

import json
import pymongo
import redis
import configparser


from class_def.User import User
from button_method.reg_user import Reg_User


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


    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    if "stock_news_app" in dblist:
        print("已存在stock_news_app")
    else:
        mydb = myclient["stock_news_app"]

    mydb = myclient["stock_news_app"]
    user_info_table = mydb["user_info"]
    user_sub_topics_table = mydb["user_sub_topic"]

    json_body = json.loads(str(event))
    input_txt = json_body['message']['text']
    # category, status
    user = User(None,None)
    #建立User資訊暫存進redis
    r.set(json_body['source']['userId'], json.dumps(user.to_dict()), nx=True)

    # 從redis取出json
    user_json = json.loads(r.get(json_body['source']['userId']))
    
    # 轉換回 User 物件
    user_obj = User.from_dict(user_json)

    #已經有狀態的情況
    if user_obj.category == "新手教學":

        print("新手教學")

    elif user_obj.category == "優惠方案":

        print("優惠方案")

    elif user_obj.category == "會員專區":

        Reg_User.reg_step(r.get(json_body['source']['userId'])[2],event)
    
    elif user_obj.category == "訂閱內容":

        print("訂閱內容")

    elif user_obj.category == "查詢修改":

        print("查詢修改")

    elif user_obj.category == "其它" :

        print("其它")


    # richmenu選單 未有狀態的情況
    if '新手教學' == input_txt:

        user_obj.category = "新手教學"
        user_obj.status = None

        r.set(json_body['source']['userId'], [User(json_body['source']['userId'], "none", "none", "none", "none", "none", "none"),"新手教學","none"], xx=True)
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="移轉到網頁？")
        )
        
    elif '優惠方案' == input_txt:

        r.set(json_body['source']['userId'], [User(json_body['source']['userId'], "none", "none", "none", "none", "none", "none"),"優惠方案","none"], xx=True)
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我不知道這樣做啥")
        )
    
    elif '會員專區' == input_txt:

        r.set(json_body['source']['userId'], [User(json_body['source']['userId'], "none", "none", "none", "none", "none", "none"),"會員專區","none"], xx=True)
        
        line_bot_api.push_message(json_body['source']['userId'], TemplateSendMessage(
            alt_text='ButtonsTemplate',
            template=ButtonsTemplate(
                thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                title='會員專區',
                text='加入會員會取消會員',
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
        
        r.set(json_body['source']['userId'], [User(json_body['source']['userId'], "none", "none", "none", "none", "none", "none"),"訂閱內容","none"], xx=True)

        line_bot_api.push_message(json_body['source']['userId'], TemplateSendMessage(
            alt_text='ButtonsTemplate',
            template=ButtonsTemplate(
                thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                title='會員專區',
                text='會員專區',
                actions=[
                    MessageAction(
                        label='加入訂閱關鍵字',
                        text='加入關鍵字'
                    ),
                    MessageAction(
                        label='刪除訂閱關鍵字',
                        text='刪除關鍵字'
                    )
                ]
            )
        ))

    elif '查詢修改' == input_txt:

        r.set(json_body['source']['userId'], [User(json_body['source']['userId'], "none", "none", "none", "none", "none", "none"),"查詢修改","none"], xx=True)

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

        r.set(json_body['source']['userId'], [User(json_body['source']['userId'], "none", "none", "none", "none", "none", "none"),"其它","none"], xx=True)

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

