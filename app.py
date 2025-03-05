from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, JoinEvent, MemberJoinedEvent

import os

app = Flask(__name__)

# 從環境變數讀取 Token 和 Secret
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
line_handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=["GET"])
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    return "OK", 200

# 🔹 功能 1：歡迎新成員並 @tag
@line_handler.add(MemberJoinedEvent)
def handle_member_join(event):
    new_member_id = event.joined.members[0].user_id
    welcome_message = f"新成員你好，進來請先看記事本的群規。\n也可以看看記事本與相簿裡的攻略熟悉一下。\n若已有帳號，請將遊戲名片放入相簿裡。"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=welcome_message))

# 🔹 功能 2：偵測關鍵字「請問」並回覆
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if "增益" in user_message:
        reply_message = "配置【增益等級】的選手 → 把白卡納入上場隊伍裡。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "出界" in user_message:
        reply_message = "使用【出界】技能 → 球靠近邊線會出現判斷出界選項。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "移動攻擊" in user_message:
        reply_message = "使用【移動攻擊】技能/n⚠️舉球員和攻擊手都需要有這個技能⚠️/n→  攻擊手在網子前橫向奔跑時，舉球員會多一個「移動攻擊」可以選。/n▶️舉球員在後排，會這招的攻擊手在前排更容易觸發/n✅川渡瞬己：直接開大招即可/n✅舉球員：目前大部分S都能舉移動攻擊/n❌岩泉/田中/女川/緣下沒有這個技能。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "問" in user_message:
        reply_message = "❗請善用搜尋❗\n記事本、相簿、聊天室皆可查詢。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "哪" in user_message:
        reply_message = "❗請善用搜尋❗\n記事本、相簿、聊天室皆可查詢。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "抽光還是存起來" in user_message:
        reply_message = "❗請善用搜尋❗\n記事本、相簿、聊天室皆可查詢。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "存起來還是抽光" in user_message:
        reply_message = "❗請善用搜尋❗\n記事本、相簿、聊天室皆可查詢。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "主線還是活動" in user_message:
        reply_message = "❗請善用搜尋❗\n記事本、相簿、聊天室皆可查詢。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "活動還是推主線" in user_message:
        reply_message = "❗請善用搜尋❗\n記事本、相簿、聊天室皆可查詢。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "活動還是主線" in user_message:
        reply_message = "❗請善用搜尋❗\n記事本、相簿、聊天室皆可查詢。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
