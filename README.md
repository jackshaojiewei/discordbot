# 🍞 ChatGPT Discord Bot (with AI Bread Facts!)

A Python-based Discord bot that integrates OpenAI’s ChatGPT for conversational AI — with an extra slice of fun: **random bread facts** when prompted!

---

## 🍞 Features

* AI-powered responses using ChatGPT
* `/breadfact` command for fun, random bread trivia
* Easy environment-based setup with `.env` support

---

## 🍞 Requirements

* Python 3.8+
* [`discord.py`](https://github.com/Rapptz/discord.py) (`2.0+` for slash commands)
* [`openai`](https://pypi.org/project/openai/)
* [`python-dotenv`](https://pypi.org/project/python-dotenv/) (optional)

---

## 🍞 Installation

### 1. Clone the repo

```bash
git clone https://github.com/jackshaojiewei/discordbot.git
cd discordbot
```

### 2. Create virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```env
DISCORD_TOKEN=your-discord-bot-token
OPENAI_API_KEY=your-openai-api-key
CHANNEL_ID=your-target-channel-id
```

---

## Running the Bot

```bash
python bot.py
```

Once running, the bot will respond to:

```
!chat What’s the difference between sourdough and rye?
```

or

```
!breadfact
```

---

## 🍞 Example Commands

### 🍞 Chat with GPT

```text
!chat Write a poem about a baguette in space.
```

### 🍞 Bread Fact

```text
!breadfact
```

Sample response:

> Did you know? The word "panini" is plural — one sandwich is technically a "panino"!

---

## 🍞 How It Works

### Chat Command

Uses OpenAI's API (`ChatCompletion`) with a simple message structure:

```python
openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
```

### Bread Fact Command

Generates a fun bread-related fact and sends it to the user.

---

## 🍞 Example `main.py` Snippet

```python
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
bot = commands.Bot(command_prefix="!", intents=intents)

# Chat command
@bot.command()
async def chat(ctx, *, prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message["content"].strip()
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

---

## 🍞 License

MIT License — do whatever you like, just keep the bread warm 🍞
