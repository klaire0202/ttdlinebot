from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, JoinEvent, MemberJoinedEvent

import os

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

# 
@line_handler.add(MemberJoinedEvent)
def handle_member_join(event):
    new_member_id = event.joined.members[0].user_id
    welcome_message = f"新成員你好，進來請先看記事本的群規。\n也可以看看記事本與相簿裡的攻略熟悉一下。\n若已有帳號，請將遊戲名片放入相簿裡。"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=welcome_message))

# 
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if "增益" in user_message:
        reply_message = "配置【增益等級】的選手\n → 把「白卡」納入上場隊伍裡，上場或候補都可以。\n❗️教練不算在內❗️"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "出界" in user_message:
        reply_message = "使用【出界】技能 → 球靠近邊線會出現判斷出界選項。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "移動" in user_message:
        reply_message = "使用【移動攻擊】技能\n⚠️舉球員和攻擊手都需要有這個技能\n→  攻擊手在網子前橫向奔跑時，舉球員會多一個「移動攻擊」可以選。\n▶️舉球員在後排，會這招的攻擊手在前排更容易觸發\n✅川渡瞬己：直接開大招即可\n✅舉球員：目前大部分S都能舉移動攻擊\n❌岩泉/田中/女川/緣下沒有這個技能"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "二次攻擊" in user_message or "二次殺球" in user_message:
        reply_message = "觸發【二次攻擊】技能解任務 → 建議不要放舉球員在隊伍裡\n若真的想放❗️放前排❗️然後接球要高才有機會觸發二次攻擊"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "主力" in user_message:
        reply_message = "讓xx配為主力 → 讓xx上場，不能是候補喔"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "隊伍製作" in user_message:
        reply_message = "點選主頁左側欄位的隊伍管理，再點選排名★獎勵，總星數請達到60顆★才能過新手任務呦"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "加起來" in user_message:
        reply_message = "配置【N名A高中,B高中選手】→ 隊伍12人裡，至少要有N名A+B的選手。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "粉絲" in user_message:
        reply_message = "🔹️粉絲幣可以從比賽中取得。\n🔹️隊伍裡有綠角可以提升拿粉絲幣！\n🔹️升綠角等級、星等、上場多隻綠角也都可以獲得更多粉絲幣！\n🔹️綠角等級約等於普彩角\n🔹️在左側粉絲俱樂部可以抽綠角、換綠角、石頭...\n🔹️選手在提升能力可以做升等\n\n能力影響：\n扣球⮕影響扣球\n發球⮕影響發球\n智力⮕影響發球、二次進攻\n拋球⮕影響托球、二次進攻\n攔網、彈力⮕影響攔網\n接球、速度⮕影響接球\n運氣⮕影響扣球、發球成功率\n           基本上升到101就不會打出界了\n精神⮕增加/减少buff造成的影響"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "商店" in user_message:
        reply_message = "商店：TV商店、商店、錦標賽商店、PVP商店、夢幻比賽商店、活動商店\n\n🔹體力、彩石必買\n🔹商店：萬能技能卡、牛奶（牛奶、彩萬能技能卡，有錢可以買）\n🔹TV商店：現場幣（應援棒夠多）\n🔹活動商店：翼、彩石必買（未來會有家具、萬能技能卡也可以買）"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "課金" in user_message or "微課" in user_message or "儲值" in user_message or "禮包" in user_message:
        reply_message = "課金推薦套組\n✅每日禮包 $90\n✅通行證 $190\n✅月卡 $220\n28天總花費$2930"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "抽光還是存起來" in user_message or "存起來還是抽光" in user_message or "存還是" in user_message or "抽還是" in user_message or "抽嗎" in user_message or "還是抽" in user_message or "還是存" in user_message or "存翅膀" in user_message or "存翼" in user_message:
        reply_message = "小幫手建議\n粉絲幣：\n看個人喜歡，覺得運氣不好的人可以用換得，覺得運氣好就抽\n\n普彩角池：\n存 除非你是課佬或是對他有真愛 非要不可"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    if "主線還是活動" in user_message or "活動還是推主線" in user_message or "活動還是主線" in user_message:
        reply_message = "小幫手建議每日主線十場，然後就努力去拿西谷！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    '''if "問" in user_message or "哪" in user_message:
        reply_message = "❗請善用搜尋❗\n記事本、相簿、聊天室皆可查詢。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
