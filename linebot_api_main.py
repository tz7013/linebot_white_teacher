from flask import Flask, request
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import url_get
import os

app = Flask(__name__)

channel_access = os.getenv('channel_access')
channel_secret = os.getenv('channel_secret')

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = channel_access
        secret = channel_secret
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        history_msg = []

        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            print(msg)                                       # 印出內容
            # reply = msg

            if msg == "星座運勢":
                reply = "請輸入您的星座或生日(月+日,四碼)"
                print(reply)
                line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息

            elif msg.isdigit():
                zodiac_sign, zodiac_num = (url_get.get_zodiac_sign(msg))
                reply = url_get.horoscope(zodiac_num)
                line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
            

            elif msg == "目前天氣":
                reply = '請依格式輸入：<地區> 天氣，例如：台北 天氣'
                print(reply)
                line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息

            elif "天氣" in msg:
                local = msg.split(" ")[0]
                reply = url_get.get_local_weather(local)
                line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息

            else:
                zodiac = ("金牛", "雙子", "巨蟹", "獅子", "處女", "天秤", "天蠍", "射手", "摩羯", "水瓶", "雙魚", "白羊")
                for i in range(len(zodiac)):
                    if msg[:2] == zodiac[i]:
                        zodiac_num = i+1
                        reply = url_get.horoscope(zodiac_num)
                        line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息

    except Exception as e:
        print(e)
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略

if __name__ == "__main__":
    app.run()