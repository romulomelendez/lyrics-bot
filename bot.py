import os
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.deepseek.com")


def create_prompt(song_name: str) -> str:
    return f"Return only the full lyrics of the song '{song_name}'. Format it in a simple and easy-to-read format and add emojis. No other text and no bold words."


async def get_lyrics(song_name: str) -> str:
    prompt = create_prompt(song_name)
       
    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return completion.choices[0].message.content


# Comando /lyrics
async def lyrics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    song_name = " ".join(context.args)
    if not song_name:
        await update.message.reply_text("⚠️ Type a song name. Example: /lyrics Bohemian Rhapsody")
        return

    await update.message.reply_text("🔍 Searching Lyrics... Please wait!")
    lyrics_text = await get_lyrics(song_name)
    await update.message.reply_text(lyrics_text)


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("lyrics", lyrics))
    
    application.run_polling()


if __name__ == "__main__":
    main()