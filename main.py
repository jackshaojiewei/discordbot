import os
import discord
import openai
import difflib
import random
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Setup OpenAI
openai.api_key = OPENAI_API_KEY

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Chat command
async def generate_chat_reply(message: str) -> str:
    """Use OpenAI to generate a response to the user's message."""
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a friendly and slightly silly bread expert chatbot."},
            {"role": "user", "content": message}
        ],
        max_tokens=200
    )
    return response.choices[0].message.content

# Bread fact command

FACT_HISTORY_FILE = "facts_history.txt"

def load_fact_history():
    if not os.path.exists(FACT_HISTORY_FILE):
        return []
    with open(FACT_HISTORY_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_fact_to_history(fact):
    with open(FACT_HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(fact + "\n")

def is_similar(fact, history, threshold=0.85):
    for old_fact in history:
        similarity = difflib.SequenceMatcher(None, fact.lower(), old_fact.lower()).ratio()
        if similarity > threshold:
            return True
    return False

async def get_bread_fact():
    prompt_styles = ["Tell me a surprising fact about bread from history.",
                     "Give me a fun bread fact related to science or chemistry.",
                     "Share a cultural tradition involving bread from a country.",
                     "Tell me a weird or little-known bread fact.",
                     "Tell me about an interesting myth or legend involving bread.",
                     "Give me a bread-related fact about ancient civilisations.",
                     "Tell me a modern, quirky fact about bread.",
                     "Give me a nutritional or health-related bread fact.",
                     "Share a fact about bread-making tools or techniques.",
                     "Tell me about an unusual type of bread from somewhere in the world."
                    ]
    history = load_fact_history()

    for _ in range(5): # Try 5 times to get a unique fact
        prompt = random.choice(prompt_styles)
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a bread expert who gives a diverse array of fun and surprising bread facts."},
                {"role": "user", "content": prompt}
            ]
        )
        fact = response["choices"][0]["message"]["content"].strip()

        if not is_similar(fact, history):
            save_fact_to_history(fact)
            return fact

    # If all facts were too similar, return the last one anyway
    return fact

# Daily task
async def send_daily_bread_fact():
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel:
        fact = await get_bread_fact()
        await channel.send(f"🍞 **Daily Bread Fact:** {fact}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Schedule daily fact at 9:00 AM
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_bread_fact, 'cron', hour=9, minute=0)
    scheduler.start()

@bot.command(name='breadhelp')
async def breadhelp(ctx):
    help_text = """
**🍞 Bread Bot Commands:**
🍞 `!breadfact` - Get a fun, unique bread fact.
🍞 `!breadchat <message>` - Chat with the bread bot.
🍞 `!breadhelp` - Show this help message.
"""
    await ctx.send(help_text)

@bot.command(name='breadfact')
async def breadfact(ctx):
    try:
        fact = await get_bread_fact()
        await ctx.send(f"🍞 {fact}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="breadchat")
async def breadchat(ctx, *, message: str):
    """Chat with the bread bot using !breadchat <message>"""
    try:
        async with ctx.typing():
         reply = await generate_chat_reply(message)
        await ctx.send(reply)
    except Exception as e:
        await ctx.send(f"Error: {e}")
        
# Run the bot
bot.run(DISCORD_TOKEN)
