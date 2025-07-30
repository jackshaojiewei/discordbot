import os
import discord
import openai
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
@bot.command()
async def chat(ctx, *, prompt):
    await ctx.trigger_typing()
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a friendly and slightly silly bread expert chatbot."},
                      {"role": "user", "content": message}],
            max_tokens=200
        )
        reply = response.choices[0].message.content
        await ctx.send(reply)
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Bread fact command
async def get_bread_fact():
    prompt = "Tell me an interesting fact about bread. Just one fact. Keep it fun but informative."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a bread expert who gives fun and surprising bread facts."},
            {"role": "user", "content": prompt}
        ]
    )
    fact = response["choices"][0]["message"]["content"]
    return fact.strip()

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

@bot.command(name='breadfact')
async def breadfact(ctx):
    fact = await get_bread_fact()
    await ctx.send(f"🍞 {fact}")

# Run the bot
bot.run(DISCORD_TOKEN)
