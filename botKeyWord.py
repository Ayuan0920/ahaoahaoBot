# 導入Discord.py模組
import discord
import os
import random
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)
intents.members = True  # 為了能找到用戶 ID

# 調用event函式庫
@client.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {client.user}")

# 重構後的規則列表
rules = [
    {
        "keyword_include": ["阿豪", "豪", "聾", "聽不到", "喵夢", "ゆうてんじ", "にゃむ"],
        "keyword_exclude": [],
        "reply_gif": [
            {"url": "https://cdn.discordapp.com/attachments/815052373398650882/1370278317231444059/1746770188455.gif", "weight": 75},
            {"url": "https://cdn.discordapp.com/attachments/1308309865772482610/1354821659458011347/ah.gif?ex=6846ecfe&is=68459b7e&hm=214091b0cd44bbcbcede57cab3a6cc606a86ad92189253d3228e0013c0533d0e", "weight": 10},
            {"url": "https://media.discordapp.net/attachments/1308309865772482610/1367777188992253992/trim.559F57BF-A43D-42FD-8513-83F9E6D88BAC-ezgif.com-video-to-gif-converter.gif?ex=684698c5&is=68454745&hm=d7dddcdb59ee6d7ee9fead51adfd14555703e7cd4a3f6dbdf4c17bb2fc566099&=&width=486&height=648", "weight": 10},
            {"url": "https://media.discordapp.net/attachments/1159063923333529661/1377204364954959972/15-9_TW2-302098500_02_1.gif?ex=68469d83&is=68454c03&hm=9c050cef16278922f340becdd1645df1e8e48c59d97faadc5aa7fbf495e74ec0&=&width=926&height=597", "weight": 5},
        ]
    },
    {
        "keyword_include": ["臭海獺"],
        "keyword_exclude": [],
        "reply_gif": [
            {"url": "https://media.discordapp.net/attachments/1308309865772482610/1380861440759693382/image-25.png", "weight": 100},
        ]
    },
    {
        "keyword_include": ["貓", "neko", "ねこ", "ネコ", "樂奈", "rana", "ranna", "らーな", "らあな", "ラーナ", "楽奈"],
        "keyword_exclude": ["貓娘", "nekopara", "ネコぱら", "ねこぱら", "ネコパラ", "三毛貓", "咪萪貓", "みけねこ", "mikeneko"],
        "reply_gif": [
            {"url": "https://img.senen.dev/raana_round.gif", "weight": 100},
        ]
    },
    # ... 更多規則
]

# 特定使用者直接回 GIF
target_users = {
    #745923333241045063: "https://cdn.discordapp.com/attachments/815052373398650882/1370278317231444059/1746770188455.gif",  # 阿豪本人
    1380212364980256768: "https://cdn.discordapp.com/attachments/815052373398650882/1370278317231444059/1746770188455.gif",  # ahaoahao
}

# 儲存訊息 ID 和對應的回覆 ID 的字典
message_replies = {}

@client.event
# 當頻道有新訊息
async def on_message(message):
    # 排除機器人本身的訊息，避免無限循環
    if message.author == client.user:
        return

    # 先檢查 @提及 的特定使用者
    for user in message.mentions:
        if user.id in target_users:
            reply = await message.channel.send(target_users[user.id], silent=True)
            message_replies[message.id] = reply.id
            return

    # 逐一檢查規則
    for rule in rules:
        content = message.content
        # 1. 包含任一 include 關鍵字
        if not any(kw in content for kw in rule["keyword_include"]):
            continue
        # 2. 不包含任何 exclude 關鍵字（若有設定）
        if any(ex in content for ex in rule.get("keyword_exclude", [])):
            continue
        # 3. 隨機選圖並回覆
        urls = [gif["url"] for gif in rule["reply_gif"]]
        weights = [gif["weight"] for gif in rule["reply_gif"]]
        chosen_url = random.choices(urls, weights=weights, k=1)[0]
        reply = await message.channel.send(chosen_url, silent=True)
        message_replies[message.id] = reply.id
        return  # 找到符合的就停止

@client.event
async def on_message_delete(message):
    if message.id in message_replies:
        try:
            reply_id = message_replies[message.id]
            reply = await message.channel.fetch_message(reply_id)
            await reply.delete()
            del message_replies[message.id]  # 刪除已刪除訊息的記錄
            print(f"已刪除對訊息 {message.id} 的回覆 {reply_id}")
        except discord.NotFound:
            print(f"找不到對訊息 {message.id} 的回覆 {reply_id}")
        except discord.Forbidden:
            print(f"沒有權限刪除對訊息 {message.id} 的回覆 {reply_id}")
        except Exception as e:
            print(f"刪除對訊息 {message.id} 的回覆 {reply_id} 時發生錯誤: {e}")

def validate_rules(rules):
    """
    檢查 rules 列表的歧義：
    - 若兩個規則的 include keywords 有交集，
      且該交集中沒有被任何一方的 exclude keywords 完全排除，就視為歧義。
    回傳一個 warning list，若非空就列印出來或是 raise Exception。
    """
    warnings = []
    n = len(rules)
    for i in range(n):
        inc_i = set(rules[i]["keyword_include"])
        exc_i = set(rules[i].get("keyword_exclude", []))
        for j in range(i+1, n):
            inc_j = set(rules[j]["keyword_include"])
            exc_j = set(rules[j].get("keyword_exclude", []))
            # 交集關鍵字
            common = inc_i & inc_j
            if not common:
                continue
            # 檢查交集裡是否所有詞都被至少一方的 exclude 擋掉
            ambiguous = []
            for kw in common:
                if kw not in exc_i and kw not in exc_j:
                    ambiguous.append(kw)
            if ambiguous:
                warnings.append(
                    f"規則 {i+1} 和 {j+1} 在 include 關鍵字 {ambiguous} 上有歧義，"
                    "請檢查是否要加上 exclude 或調整權重/順序。"
                )
    return warnings
            
if __name__ == "__main__":
    # 檢查規則歧義
    from sys import exit
    amb = validate_rules(rules)
    if amb:
        print("【規則歧義警告】")
        for w in amb:
            print("  -", w)
        exit(1)  # 或者改成 exit(0) 只是 warning，但建議先修正再啟動
    else:
        print("nothing wrong")
    # 從環境變數中取得 token
    TOKEN = os.getenv("AHAOTOKEN")
    client.run(TOKEN)