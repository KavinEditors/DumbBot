#only requires .env and update ur bot token in that
#install requirements.txt in cmd/terminal in vsc
#install the requirements using 'pip install -r requirements.tx
#run in vsc terminal 'python (Inbuilt)_bot.py'

import discord
from discord.ext import commands, tasks
import random
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Scoreboard and answered tracking
scores = {}
answered_users = set()
current_question = None
correct_answer = None
question_count = 0

dumb_questions = [
    "If I microwave ice, will I get fire?",
    "Can I charge my phone in the bathtub?",
    "If I eat a magnet, will I become magnetic?",
    "Is water wet or is wet water?",
    "If I scream in space, can aliens hear me?",
    "Can I cook chicken with my laptop's heat?",
    "If I delete System32, will my PC run faster?",
    "Can I become invisible by closing my eyes?",
    "If I eat glow sticks, will I glow?",
    "Is cereal soup?",
    "Can I get WiFi by standing on my roof?",
    "Does holding your breath make you stronger?",
    "Is 5G stored in your bones?",
    "Can I upload my brain to Google Drive?",
    "Will drinking Red Bull actually give me wings?",
    "Can I use pizza as a face mask?",
    "If I meow at cats enough, will they adopt me?",
    "If I sleep in class, do I absorb knowledge passively?",
    "Can I get fit just by thinking about the gym?",
    "If I clap with one hand, will I time travel?"
] + [f"Dumb Question #{i+21}?" for i in range(80)]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    ask_question.start()

@tasks.loop(minutes=10)
async def ask_question():
    global current_question, correct_answer, answered_users, question_count
    channel = discord.utils.get(bot.get_all_channels(), name="general")  # Change to your channel name
    if channel:
        current_question = random.choice(dumb_questions)
        correct_answer = random.choice(['yes', 'no'])
        answered_users.clear()
        question_count += 1
await channel.send(f"""🧠 **Dumb Question Time!**
{current_question} (Answer with `!yes` or `!no`)""")

@bot.command()
async def yes(ctx):
    await process_answer(ctx, 'yes')

@bot.command()
async def no(ctx):
    await process_answer(ctx, 'no')

async def process_answer(ctx, answer):
    global correct_answer
    if not current_question:
        await ctx.send("❌ There's no active question right now!")
        return
    if ctx.author.id in answered_users:
        await ctx.send(f"🧠 {ctx.author.mention} got temporary memory loss and tried again...")
        return
    answered_users.add(ctx.author.id)
    if answer == correct_answer:
        scores[ctx.author.id] = scores.get(ctx.author.id, 0) + 1
        await ctx.send(f"✅ {ctx.author.mention} got it right! 🎉")
    else:
        await ctx.send(f"❌ {ctx.author.mention} is dumb. Better luck next time!")

@bot.command()
async def dumbboard(ctx):
    if not scores:
        await ctx.send("Nobody's dumb enough to play yet. 😝")
        return
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    leaderboard = "\n".join([f"<@{uid}>: {score} dumb points" for uid, score in sorted_scores])
    await ctx.send(f"🏆 **DumbBoard** 🧠\n{leaderboard}")

@bot.command()
async def dumbhelp(ctx):
    help_text = (
        "**🧠 DumbBot Commands:**\n"
        "`!yes` – Answer 'yes' to the dumb question\n"
        "`!no` – Answer 'no' to the dumb question\n"
        "`!dumbboard` – Show the leaderboard\n"
        "`!score` – See your score\n"
        "`!mysus` – See how sus you are\n"
        "`!dumbrate @user` – Rate how dumb someone is\n"
        "`!dumbfact` – Get a random dumb fact\n"
        "`!memoryloss` – Simulate memory loss\n"
        "`!dumbquestion` – Ask a dumb question immediately\n"
        "`!whoiswinning` – See who's leading\n"
        "`!dumbjoke` – Get a painfully bad joke\n"
        "`!questioncount` – Total dumb questions asked\n"
        "`!topdumbs` – Alias for dumbboard\n"
        "`!brag` – Brag about your dumb score\n"
    )
    await ctx.send(help_text)

@bot.command()
async def score(ctx):
    await ctx.send(f"🎯 {ctx.author.mention}, your score is {scores.get(ctx.author.id, 0)} dumb points.")

@bot.command()
async def mysus(ctx):
    percent = random.randint(1, 100)
    await ctx.send(f"{ctx.author.mention} is {percent}% sus. 😳")

@bot.command()
async def dumbrate(ctx, user: discord.Member):
    dumb_level = random.randint(0, 100)
    await ctx.send(f"🧠 {user.mention} is {dumb_level}% dumb!")

@bot.command()
async def dumbfact(ctx):
    facts = [
        "Bananas are berries, but strawberries aren't.",
        "Octopuses have three hearts and zero friends.",
        "You can't hum while holding your nose (try it).",
        "A group of flamingos is called a 'flamboyance'.",
        "Your feet have about 250,000 sweat glands. Ew."
    ]
    await ctx.send(f"💡 Dumb Fact: {random.choice(facts)}")

@bot.command()
async def memoryloss(ctx):
    await ctx.send(f"🧠 {ctx.author.mention} got temporary memory loss!")

@bot.command()
async def dumbquestion(ctx):
    await ask_question()

@bot.command()
async def whoiswinning(ctx):
    if not scores:
        await ctx.send("No one's dumb enough to win yet. 😆")
        return
    winner = max(scores.items(), key=lambda x: x[1])
    await ctx.send(f"🏅 <@{winner[0]}> is leading with {winner[1]} dumb points!")

@bot.command()
async def dumbjoke(ctx):
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What’s orange and sounds like a parrot? A carrot.",
        "I used to play piano by ear, now I use my hands.",
        "Why don’t eggs tell jokes? They’d crack each other up."
    ]
    await ctx.send(f"🤣 {random.choice(jokes)}")

@bot.command()
async def questioncount(ctx):
    await ctx.send(f"🤓 We've asked {question_count} dumb questions so far!")

@bot.command()
async def topdumbs(ctx):
    await dumbboard(ctx)

@bot.command()
async def brag(ctx):
    score = scores.get(ctx.author.id, 0)
    await ctx.send(f"💪 {ctx.author.mention} has {score} dumb points and isn't afraid to flaunt it!")

bot.run(TOKEN)

