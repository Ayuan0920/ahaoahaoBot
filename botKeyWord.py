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

keyword_gif = {
    ("阿豪", "豪", "聾", "聽不到", "喵夢", "ゆうてんじ", "にゃむ"): [
        ("https://cdn.discordapp.com/attachments/815052373398650882/1370278317231444059/1746770188455.gif", 75),
        ("https://cdn.discordapp.com/attachments/1308309865772482610/1354821659458011347/ah.gif?ex=6846ecfe&is=68459b7e&hm=214091b0cd44bbcbcede57cab3a6cc606a86ad92189253d3228e0013c0533d0e", 10),
        ("https://media.discordapp.net/attachments/1308309865772482610/1367777188992253992/trim.559F57BF-A43D-42FD-8513-83F9E6D88BAC-ezgif.com-video-to-gif-converter.gif?ex=684698c5&is=68454745&hm=d7dddcdb59ee6d7ee9fead51adfd14555703e7cd4a3f6dbdf4c17bb2fc566099&=&width=486&height=648", 10),
        ("https://media.discordapp.net/attachments/1159063923333529661/1377204364954959972/15-9_TW2-302098500_02_1.gif?ex=68469d83&is=68454c03&hm=9c050cef16278922f340becdd1645df1e8e48c59d97faadc5aa7fbf495e74ec0&=&width=926&height=597", 5),
        ("https://media.discordapp.net/attachments/1353220886815051807/1381858602230353992/1.gif?ex=68490b9c&is=6847ba1c&hm=45bacf183431acf2257ad9953523760485a375b7c4b761d2a3f72ccbf8402428&=&width=829&height=667", 5),
        ("https://media.discordapp.net/attachments/1353220886815051807/1381859084042506293/2.gif?ex=68490c0f&is=6847ba8f&hm=7cae71cac2d3b13252195884f80e4c0970aeaf9b3d1d79cec2c217539be2c82a&=&width=745&height=718", 5),
    ],
    ("臭海獺"): [
        ("https://media.discordapp.net/attachments/1308309865772482610/1380861440759693382/image-25.png", 100),
      # ("https://images-ext-1.discordapp.net/external/KqflxnMlIlpPiIjrL1PCULF_RgD3ssz5z24XmOLN4zU/https/media.tenor.com/DXn1Zdlu3HUAAAPo/ave-mujica-umiri.mp4", 50), # 可以也和我重修舊好嗎
    ],
    #"另一個關鍵字": "另一個GIF連結"  # 請替換成實際的 GIF 連結
}

# 多個特定用戶的 ID 對應要回傳的 GIF 連結
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

    # 檢查訊息中是否包含任何關鍵字
    for keywords, gif_probabilities in keyword_gif.items():
        if isinstance(keywords, tuple):  # 如果關鍵字是元組
            if any(keyword in message.content for keyword in keywords):
                gif_url = random.choices([url for url, prob in gif_probabilities], weights=[prob for url, prob in gif_probabilities], k=1)[0]
                reply = await message.channel.send(gif_url, silent=True)
                message_replies[message.id] = reply.id
                return  # 如果找到一個關鍵字就停止檢查
        else:  # 如果關鍵字是單個字串
            if keywords in message.content:
                gif_url = random.choices([url for url, prob in gif_probabilities], weights=[prob for url, prob in gif_probabilities], k=1)[0]
                reply = await message.channel.send(gif_url, silent=True)
                message_replies[message.id] = reply.id
                return  # 如果找到一個關鍵字就停止檢查

    for user in message.mentions:
        if user.id in target_users:
            gif_url = target_users[user.id]
            reply = await message.channel.send(gif_url, silent=True)
            message_replies[message.id] = reply.id
            return  # 若要一次只回應一個人，這邊 return；若都回應，可移除

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
            
if __name__ == "__main__":
    # 從環境變數中取得 token
    TOKEN = os.getenv("AHAOTOKEN")
    client.run(TOKEN)