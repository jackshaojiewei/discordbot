# 🍞 ChatGPT Discord Bot (with AI Bread Facts!)

A Python-based Discord bot that integrates OpenAI’s ChatGPT for conversational AI — with an extra slice of fun: **random bread facts** when prompted!

---

## 🍞 Features

* AI-powered responses using ChatGPT
* `/breadfact` command for fun, random bread trivia
* Easy environment-based setup with `.env` support
* Bread quiz

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

Randomly picks from a list of fun bread-related facts and sends one back to the user.

---

## 🍞 Example `bot.py` Snippet

```python
import os
import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
        await ctx.send(f"⚠️ Error: {e}")

# Bread fact command (GPT-generated)
@bot.command()
async def breadfact(ctx):
    try:
        prompt = "Tell me one interesting and fun fact about bread."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        fact = response.choices[0].message["content"].strip()
        await ctx.send(f"🍞 Fun Bread Fact: {fact}")
    except Exception as e:
        await ctx.send(f"⚠️ Error: {e}")

# Run the bot
bot.run(TOKEN)

---

## 🍞 License

MIT License — do whatever you like, just keep the bread warm 🍞
