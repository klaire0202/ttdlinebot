import os
import re
from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, JoinEvent, MemberJoinedEvent, StickerMessage

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
    welcome_message = f"新成員你好，請先看記事本的群規。\n\n也可以看看記事本與相簿裡的攻略。\n\n❗️請將遊戲名片放入相簿裡❗️\n若無放置名片，在清人時間時，便會踢出群組呦。\n\n‼️本群組嚴禁曬卡之行為‼️\n記事本裡有曬卡須知，請詳細查閱。\n若忍不住想分享喜悅，請移駕到以下網址的群組🥳\n\nhttps://line.me/R/ti/g/-fbv48Qs8U\n\n🫶🏻謝謝配合🫶🏻"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=welcome_message))

@line_handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    pass

allowed_groups = ["Cc4939a9cf01226965d75052d3bc669e0", "C3e5e891a7c76935f3887f4da4406eb43"]

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.type == "group":
        group_id = event.source.group_id
        
        if group_id not in allowed_groups:
            return 
        user_message = event.message.text.lower()
        
        message_without_parentheses = re.sub(r'\([^\)]+\)', '', user_message)
        cleaned_message = message_without_parentheses.strip()
    
        responses = {
            ("2930","打手出界","擋出界","2290","2129"): None,
            #("dc","chatgpt","facebook","touch","gamerch",".com","2930","cd","npc","cpu","cp","ic","打手出界","擋出界","call","2290","2129","card"): None,
            #("7777", "吸", "c"): "小幫手眼紅中 別再曬了🥹",
            ("29",): "少女旭：（玻璃心中）不要再觸發我的傷心事了…小心我破防呦🥹",
            ("低手擊球",): "使用【低手擊球】技能 → 下手發球",
            ("頭上擊球",): "使用【頭上擊球】技能 → 上手發球",
            #("復刻",): "❗️這遊戲「不復刻」❗️\n❗️這遊戲「不復刻」❗️\n❗️這遊戲「不復刻」❗️\n\n只有搶錢的福袋，不要想不開，福袋坑人的程度是想不到的，不要賭福袋！除非你想一次花幾萬塊下去抽福袋😎",
            ("綠角",): "綠角建議都抽都買！\n不用問先抽/換誰，都要！",
            ("增益",): "配置【增益等級】的選手\n → 把「白卡」納入上場隊伍裡，上場或候補都可以。\n❗️教練不算在內❗️",
            ("出界",): "使用【出界】技能 → 球靠近邊線會出現判斷出界選項。",
            ("移動",): "使用【移動攻擊】技能\n⚠️舉球員和攻擊手都需要有這個技能\n→  攻擊手在網子前橫向奔跑時，舉球員會多一個「移動攻擊」可以選。\n▶️舉球員在後排，會這招的攻擊手在前排更容易觸發\n✅川渡瞬己：直接開大招即可\n✅舉球員：目前大部分S都能舉移動攻擊\n❌岩泉/田中/女川/緣下沒有這個技能",
            ("二次攻擊", "二次殺球", "二次扣球"): "觸發【二次攻擊】技能解任務 → \n建議「不要」放舉球員在隊伍裡\n若真的想放 放前排，但建議不要放比較好觸發，然後接球要高才有機會觸發二次攻擊。\n簡單說就是二觸是直接扣殺。",
            ("雙人攻擊", "雙人殺球", "雙人扣球","二次進攻"): "觸發【二次進攻】技能解任務 → \n目前只有舉球員有這個技能，請把舉球員放在前排，一傳接球高時便會觸發。\n簡單說就是偷偷吊球(撥?)過去。",
            ("主力",): "讓xx配為主力 → 讓xx上場，不能是候補喔",
            #("分解","製作","交換","碎片","合成"): "小幫手建議\n🔷️製作 - 角色\n‼️金角能全換就全換出來‼️\n自由人隨意，是不太需要啦…\n\n🔷️製作 - 碎片回收\n🔹️技能卡：因金彩技能較難拿到，所\n                     以會建議把不要的技能去\n                     製作區換金或彩萬能。\n🔹️飯團：把不需要的裝備換飯糰。\n🔹️彩石：若有滿星5星的卡，且碎片\n                 溢出來時，再去換彩石。\n                 或之後出異裝時，在每日活\n                 動出自己未有的異裝碎片再\n                 拿去交換。\n\n❗️以上量力而為就好❗️不是一定❗️\n\n🫡切記🫡\n早期所有東西都缺，現在不需要，不代表未來不需要‼️\n\n所以是建議目前的技能卡、飯團暫時不是很需要換。\n\n🔷️TV角：換\n🔹️每個月每個角都可以換一次。\n🔹️live等級全服統一。\n🔹️反正每個月都會累積很多現場幣，\n     以換最新的為主。\n🔹️如果已換到角色了，再次兌換就是\n     30碎片，如果不是很想升星，可以\n     直接拿去換彩石，但未來有異裝時\n     ，滿星活動幣加成更多喔～",
            ("分解","製作","交換","碎片","合成"): "小幫手建議\n🔷️製作 - 角色\n‼️金角能全換就全換出來‼️\n自由人隨意，是不太需要啦…\n\n🔷️製作 - 碎片回收\n🔹️技能卡：因金彩技能較難拿\n                    到，所以會建議把\n                    不要的技能去製作\n                    區換金或彩萬能。\n🔹️飯團：把不需要的裝備換飯糰。\n🔹️彩石：若有滿星5星的卡，且\n                 碎片溢出來時，再去換\n                 彩石。或之後出異裝時，\n                 在每日活動出自己未有\n                 的異裝碎片再拿去交換。\n\n❗️以上量力而為就好❗️不是一定❗️\n\n🫡切記🫡\n早期所有東西都缺，現在不需要，不代表未來不需要‼️\n\n所以是建議目前的技能卡、飯團暫時不是很需要換。\n\n🔷️TV角：換\n🔹️每個月每個角都可以換一次。\n🔹️live等級全服統一。\n🔹️反正每個月都會累積很多\n     現場幣，以換最新的為主。\n🔹️如果已換到角色了，再次兌換\n     就是30碎片，如果不是很想升\n     星，可以直接拿去換彩石，但\n     未來有異裝時 ，滿星活動幣加\n     成更多喔～",
            #("隊伍製作",): "點選主頁左側欄位的隊伍管理，再點選排名★獎勵，總星數請達到60顆★才能過新手任務呦",
            ("下個異裝","下一個異裝",): "第三個異裝主題是「水著 大海」分別有「牛島、天童、月島、山口」\n這四隻都有露腹肌喔🥰\n\n接著又回到「掃除」主題，分別有「青根、二口」\n\n再來是「制服」主題，分別有「西谷、田中」",
            ("加起來",): "配置【N名A高中,B高中選手】→ \n隊伍12人裡，至少要有N名A+B的選手。",
            ("粉絲","人氣幣"): "🔹️粉絲幣可以從比賽中取得\n🔹️隊伍裡有綠角可以提升拿\n     粉絲幣！\n🔹️升綠角等級、星等、上場多隻\n     綠角也都可以獲得更多粉絲幣\n🔹️綠角等級約等於普彩角\n🔹️在左側粉絲俱樂部可以抽綠角\n     、換綠角、石頭...\n🔹️選手在提升能力可以做升等\n\n能力影響：\n扣球⮕影響扣球\n發球⮕影響發球\n智力⮕影響發球、二次進攻\n拋球⮕影響托球、二次進攻\n攔網、彈力⮕影響攔網\n接球、速度⮕影響接球\n運氣⮕影響扣球、發球成功率\n            升到101就不會打出界\n心理⮕增加/减少buff造成的影響",
            ("能力","教練","屬性"): "能力影響：\n扣球 ⮕ 影響扣球\n發球 ⮕ 影響發球\n智力 ⮕ 影響發球、二次進攻\n拋球 ⮕ 影響托球、二次進攻\n攔網、彈力 ⮕ 影響攔網\n接球、速度 ⮕ 影響接球\n運氣 ⮕ 影響扣球、發球成功率\n              升到101就不會打出界\n心理 ⮕ 增加/减少buff造成的影響",
            ("技能",): "小幫手建議 升技能：\n🔹️銅卡：被動>托球>飛身接球>接球\n🔹️銀卡：看各個角色需求\n🔹️金卡：扣球攻擊(斜線、直線、吊球、打手出界)、托球、擋路、軟攔\n🔹️彩卡：buff、彩扣\n\n若想重製技能轉移到同角異裝也是可以，但技能要相同，顏色也要相同才可以呦！\n\n❗️重製不會返回金幣與萬能❗️會是該角色指定的技能\n\n所以要用「萬能卡」升時，必須想好哦！之後重製返回不會是萬能卡",
            ("商店",): "❗️體力、彩石必買❗️\n\n🔹商店：萬能技能卡、牛奶（牛奶、彩萬能技能卡，有錢可以買）\n🔹TV商店：選手、現場幣（應援棒夠多）\n🔹️錦標賽商店：體力、彩石\n🔹️PVP商店：體力、彩石\n🔹️DM夢幻比賽商店：萬能技能卡、彩石（牛奶隨意）\n🔹️扭蛋點數商店：偶像級選手選擇劵\n🔹️粉絲圈商店：綠卡！\n🔹️社團商店：技能萬能卡、彩石（牛奶隨意）\n🔹活動商店：翼、彩石必買（未來會有家俱、萬能技能卡也可以買）",
            ("課金", "微課", "儲值", "禮包"): "課金推薦套組\n✅每日禮包 $90\n✅通行證 $190\n✅月卡 $220\n28天總花費$2930",
            ("抽光還是存起來", "存起來還是抽光", "存還是", "抽還是", "抽嗎", "還是抽", "還是存", "存翅膀", "存翼","要抽"): "小幫手建議\n粉絲幣：\n看個人喜歡，覺得運氣不好的人可以用換得，覺得運氣好就抽\n\n普彩角池：\n存 除非你是課佬或是對他有真愛 非要不可\n\n異裝池：\n❗️想抽就抽❗️\n這遊戲不復刻異裝，只有搶錢的福袋，不要跟錢過不去，不要想不開❗️",
            #("主線還是活動", "活動還是推主線", "活動還是主線", "活動還是劇情", "還是劇情", "還是活動", "還是主線", "活動還是", "主線還是", "劇情還是"): "小幫手建議每日主線十場，然後就努力去拿金卡活動！\n之後就是看個人要把金卡衝到三星或是打主線\n\n如果金卡碎片、彩石都換完，建議去過劇情關卡，慢慢集自由人，讓下期出來時，就可以直接換金卡🥳或是刷裝備、技能關卡",
            ("120%","110%","100%","50%","30%","生命值"): "生命值越高，攻擊成功率越高，像是成功、大成功與超大成功，而使用階級越高的技能消耗越多。\n\n✔️官方含糊說詞：120%與100%的攻防還是有些許差異，體力方面就更不用說了，一定都有。\n\n當生命值低於50%時，所有屬性下降20%；當生命值低於10%時，所有屬性下降90%。\n\n在隊伍裡可以從角色的上方看到該生命值，也有⬆️↗️➡️↘️⬇️的箭頭標示，旁邊則有顯示該生命值數值。\n\n🔹️銅白TV卡：每天體力不定，\n                          幅度從30~120%。\n                          若當日體力較低，\n                          是沒有辦法提高，\n                          除非到隔天。\n🔹️綠紫卡：每天隨機100～120%。\n🔹️金卡：每天都是100%。\n🔹️彩卡：每天都是100%，\n                 但如果隊伍穿的校服與\n                 該角色同校，便會變成\n                 120%。\n\n小幫手每日吐槽，到底為什麼是翻譯成生命值，現在是打排球會死人嗎，這麼刺激的呦~",
        }
        
        if cleaned_message == "":
            return
    
        for keywords, reply_message in responses.items():
            if any(keyword in cleaned_message for keyword in keywords):
                if reply_message:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                return

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
