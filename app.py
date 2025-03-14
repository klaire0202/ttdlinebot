from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, JoinEvent, MemberJoinedEvent, StickerMessage

import os
import re

app = Flask(__name__)

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

@line_handler.add(MemberJoinedEvent)
def handle_member_join(event):
    new_member_id = event.joined.members[0].user_id
    welcome_message = f"新成員你好，進來請先看記事本的群規。\n也可以看看記事本與相簿裡的攻略熟悉一下。\n若已有帳號，請將遊戲名片放入相簿裡。"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=welcome_message))

@line_handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    pass

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()
    cleaned_message = re.sub(r'[\U00010000-\U0010ffff]', '', user_message)  # 移除 Emoji

    responses = {
        ("dc",): None,
        ("7777", "吸", "c"): "小幫手眼紅中 別再曬了🥹",
        ("增益",): "配置【增益等級】的選手\n → 把「白卡」納入上場隊伍裡...",
        ("出界",): "使用【出界】技能 → 球靠近邊線會出現判斷出界選項。",
        ("移動",): "使用【移動攻擊】技能\n⚠️舉球員和攻擊手都需要有這個技能...",
        ("二次攻擊", "二次殺球", "二次扣球"): "觸發【二次攻擊】技能解任務 → 建議「不要」放舉球員在隊伍裡...",
        ("雙人攻擊",): "觸發【雙人攻擊】技能解任務 → 舉球員放前排，一傳接球高",
        ("主力",): "讓xx配為主力 → 讓xx上場，不能是候補喔",
        ("粉絲",): "🔹️粉絲幣可以從比賽中取得。\n🔹️隊伍裡有綠角可以提升拿粉絲幣！\n...",
        ("商店",): "❗️體力、彩石必買❗️\n🔹商店：萬能技能卡、牛奶...",
        ("課金", "微課", "儲值", "禮包"): "課金推薦套組\n✅每日禮包 $90\n✅通行證 $190\n✅月卡 $220\n28天總花費$2930",
        ("抽光還是存起來", "存起來還是抽光", "存還是", "抽還是", "抽嗎", "還是抽", "還是存"): "小幫手建議\n粉絲幣：\n看個人喜歡，覺得運氣不好的人可以用換得...",
        ("主線還是活動", "活動還是主線", "還是劇情", "還是主線"): "小幫手建議每日主線十場，然後就努力去拿西谷！\n..."
    }

    # 只有 Emoji 不回應
    if cleaned_message.strip() == "":
        return

    for keywords, reply_message in responses.items():
        if any(keyword in cleaned_message for keyword in keywords):
            if reply_message:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
            return

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
