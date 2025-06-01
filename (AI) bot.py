#requires .env and update ur bot token and open ai api key in that
#install requirements.txt in cmd/terminal in vsc
#install the requirements using 'pip install -r requirements.txt'
#run it using 'python (AI)_bot.py' in vsc terminal
#if cmd link to the drive and floder

import discord
from discord.ext import commands, tasks
import random
import asyncio
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Data stores
user_scores = {}
asked_users = set()
current_question = None
correct_answer = None
question_asker = None

# AI Question Generator
def generate_ai_question():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Generate a yes or no dumb question that sounds funny and illogical."},
                {"role": "user", "content": "Give me a single dumb yes or no question."}
            ],
            max_tokens=50,
            temperature=1.0
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("OpenAI error:", e)
        return random.choice(["Can I plug my phone into a potato for power?", "Does clapping recharge my energy?"])

# Ask dumb question every 10 minutes
@tasks.loop(minutes=10)
async def ask_dumb_question():
    global current_question, correct_answer, question_asker, asked_users
    current_question = generate_ai_question()
    correct_answer = random.choice(["yes", "no"])
    asked_users.clear()
    question_asker = None

    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                await channel.send(f"🧠 DumbBot Asks: **{current_question}**\nReply with `!yes` or `!no`!")
                break  # Ask only in the first accessible text channel
            except:
                continue

@bot.event
async def on_ready():
    print(f'🤖 DumbBot is online as {bot.user}')
    ask_dumb_question.start()

@bot.command()
async def yes(ctx):
    await process_answer(ctx, "yes")

@bot.command()
async def no(ctx):
    await process_answer(ctx, "no")

async def process_answer(ctx, user_answer):
    global asked_users, correct_answer, question_asker
    user = ctx.author
    if user.id in asked_users:
        await ctx.send(f"🧠 {user.mention}, you already answered! Looks like you got temporary memory loss! 😵")
        return

    asked_users.add(user.id)

    if user_answer == correct_answer:
        user_scores[user.id] = user_scores.get(user.id, 0) + 1
        await ctx.send(f"🎉 {user.mention} is correct! Score: {user_scores[user.id]}")
    else:
        await ctx.send(f"🤪 {user.mention} is dumb! That's wrong. Score: {user_scores.get(user.id, 0)}")

# Commands
@bot.command()
async def leaderboard(ctx):
    if not user_scores:
        await ctx.send("📉 No scores yet!")
        return
    sorted_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
    msg = "🏆 DumbBot Leaderboard:\n"
    for i, (user_id, score) in enumerate(sorted_scores[:10], 1):
        user = await bot.fetch_user(user_id)
        msg += f"{i}. {user.name} - {score} dumb points\n"
    await ctx.send(msg)

@bot.command()
async def dumbrate(ctx):
    percent = random.randint(1, 100)
    await ctx.send(f"🧠 {ctx.author.mention}, your dumbness rate is {percent}%")

@bot.command()
async def dumbfact(ctx):
    facts = [
        "Humans share 60% of DNA with bananas 🍌",
        "You can't hum while holding your nose. Try it!",
        "A group of flamingos is called a flamboyance.",
        "Cows have best friends. Moo-ving story! 🐄",
        "Octopuses have three hearts and still get ghosted. 💔"
    ]
    await ctx.send(random.choice(facts))

@bot.command()
async def brag(ctx):
    score = user_scores.get(ctx.author.id, 0)
    await ctx.send(f"😎 {ctx.author.mention} has {score} dumb points. Absolute legend!")

@bot.command()
async def dumbidea(ctx):
    ideas = [
        "Make a sandwich using pop-tarts as bread.",
        "Invent edible shoes for midnight snacks.",
        "Start a podcast with your cat.",
        "Build a time machine using only spoons.",
        "Use bubble wrap as gym flooring."
    ]
    await ctx.send(random.choice(ideas))

@bot.command()
async def dumbify(ctx, *, text):
    dumb_text = ''.join(random.choice((c.upper(), c.lower())) for c in text)
    await ctx.send(f"🤪 {dumb_text}")

@bot.command()
async def reset(ctx):
    user_scores.clear()
    await ctx.send("🧹 DumbBot leaderboard wiped clean!")

# Run the bot
bot.run(DISCORD_TOKEN)
