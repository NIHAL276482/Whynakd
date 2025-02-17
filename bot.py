from telethon import TelegramClient, events
from telethon.tl.types import PeerUser
import random
import time

# Configuration (Get from https://my.telegram.org/apps)
API_ID = 25305140
API_HASH = '6d19044c96341ccb3da294f878df7659'
PHONE_NUMBER = '+919301483971'

# Stylish Offline Messages (with random emojis)
OFFLINE_MESSAGES = [
    "🚫 **I'm Currently Offline** 🚫\n\n"
    "📆 _Last Active: {time}_\n"
    "💤 **Auto-Reply**: I'll respond when I'm back! {emoji}",

    "🌙 **Away From Keyboard** 🌙\n\n"
    "⏰ _Last Seen: {time}_\n"
    "📨 Your message is saved! {emoji}",

    "⏳ **Temporarily Unavailable** ⏳\n\n"
    "🕒 _Active Until: {time}_\n"
    "📬 Message queued! {emoji}"
]

EMOJIS = ["✨", "🌟", "💫", "🎯", "🔮", "⚡", "🌠"]

client = TelegramClient('selfbot', API_ID, API_HASH)

async def send_typing(event):
    await client.send_read_acknowledge(event.chat_id)
    await client(typing.Request(peer=event.chat_id, action=typing.ActionTyping()))

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def auto_reply(event):
    if isinstance(event.peer_id, PeerUser):  # Only reply to users
        sender = await event.get_sender()
        if not sender.bot:  # Don't reply to bots
            await send_typing(event)
            time.sleep(1)  # Simulate typing delay
            
            chosen_msg = random.choice(OFFLINE_MESSAGES)
            emoji = random.choice(EMOJIS)
            current_time = time.strftime("%H:%M %Z")
            
            response = chosen_msg.format(time=current_time, emoji=emoji)
            await event.reply(
                response,
                parse_mode='md',  # Markdown formatting
                link_preview=False
            )
            print(f"Replied to {sender.first_name}")

async def main():
    await client.start(PHONE_NUMBER)
    print("Self-Bot Running! Press Ctrl+C to stop.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped.")
