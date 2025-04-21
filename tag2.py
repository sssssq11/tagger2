from telethon import TelegramClient, events
import re

# Вставь сюда свои данные
api_id = 21150163       # <-- Твой api_id
api_hash = '7baabf784258d6218e920c19238e0d17'

client = TelegramClient('session_name', api_id, api_hash)
active = True

@client.on(events.NewMessage(pattern=r'^!tag\s+"(.+?)"'))
async def tag_handler(event):
    global active
    if not active:
        await event.reply("Упоминание отключено.")
        return

    text = event.pattern_match.group(1)

    participants = []
    async for user in client.iter_participants(event.chat_id):
        if user.bot:
            continue
        if user.username:
            participants.append(f"@{user.username}")
        else:
            participants.append(f"[{user.first_name}](tg://user?id={user.id})")

    msg = f"{text}\n" + " ".join(participants)
    await client.send_message(event.chat_id, msg, parse_mode="md")

@client.on(events.NewMessage(pattern=r'^!stop'))
async def stop_handler(event):
    global active
    active = False
    await event.reply("Упоминание отключено.")

@client.on(events.NewMessage(pattern=r'^!start'))
async def start_handler(event):
    global active
    active = True
    await event.reply("Упоминание включено.")

print("Юзербот запущен...")
client.start()
client.run_until_disconnected()