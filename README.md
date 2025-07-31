# 🍞 ChatGPT Discord Bot

A Python-based Discord bot that integrates OpenAI’s ChatGPT for conversational AI with an extra slice of fun: **random bread facts** when prompted, and daily bread facts posted at 9.00 am!

---

## 🍞 Features

* AI-powered responses using ChatGPT
* `!breadfact` command for fun, random bread trivia
* Daily bread facts posted at 9.00 am everyday
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
python main.py
```

Once running, the bot will respond to:

```
!breadchat What’s the difference between sourdough and rye?
```

or

```
!breadfact
```

---

## 🍞 Example Commands

### 🍞 Chat with GPT

```text
!breadchat Write a poem about a baguette in space.
```

### 🍞 Bread Fact

```text
!breadfact
```

Sample response:

> Did you know? The word "panini" is plural — one sandwich is technically a "panino"!

---

## 🍞 How It Works

### 🍞 Chat Command

Uses OpenAI's API (`ChatCompletion`) and responds to the user's message as a friendly bread expert chatbot.

### 🍞 Bread Fact Command

Generates a fun bread-related fact and sends it to the user, randomly choosing from a number of unique prompts.

---

## 🍞 License

MIT License — do whatever you like, just keep the bread warm 🍞
