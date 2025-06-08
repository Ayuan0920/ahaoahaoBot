# 導入Discord.py模組
import discord
import os
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
    ("阿豪", "豪", "聾", "聽不到", "喵夢", "ゆうてんじ", "にゃむ"): "https://cdn.discordapp.com/attachments/815052373398650882/1370278317231444059/1746770188455.gif",
    ("臭海獺"): "https://media.discordapp.net/attachments/1308309865772482610/1380861440759693382/image-25.png",
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
    for keywords, gif_url in keyword_gif.items():
        if isinstance(keywords, tuple):  # 如果關鍵字是元組
            if any(keyword in message.content for keyword in keywords):
                reply = await message.channel.send(gif_url)
                message_replies[message.id] = reply.id  # 儲存原始訊息 ID 和回覆 ID
                return  # 如果找到一個關鍵字就停止檢查
        else:  # 如果關鍵字是單個字串
            if keywords in message.content:
                reply = await message.channel.send(gif_url)
                message_replies[message.id] = reply.id  # 儲存原始訊息 ID 和回覆 ID
                return  # 如果找到一個關鍵字就停止檢查

    for user in message.mentions:
        if user.id in target_users:
            gif_url = target_users[user.id]
            gif_reply = await message.channel.send(gif_url)
            message_replies[message.id] = gif_reply.id
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