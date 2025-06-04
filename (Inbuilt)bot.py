#only requires .env and update your bot token in that
#install requirements.txt in cmd/terminal in vsc
#install the requirements using 'pip install -r requirements.tx
#run in vsc terminal python " python '(Inbuilt)bot.py' "

import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = discord.Object(id=1355884348192063548)  # Replace with your actual guild ID

# Set up bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Score tracking and game state
scores = {}
answered_users = set()
current_question = None
correct_answer = None
question_count = 0

# Dumb question channel
target_channel_id = None

# Dumb questions
base_questions = [
    "If I microwave ice, will I get fire?❄🧊",
    "Can I charge my phone in the bathtub?🛁",
    "If I eat a magnet, will I become magnetic?🧲",
    "Is water wet (yes) or is wet water(No)?💦",
    "If I scream in space, can aliens hear me?👽",
    "Can I cook chicken with my laptop's heat?🍗",
    "If I delete System32, will my PC run faster?💽",
    "Can I become invisible by closing my eyes?👀",
    "If I eat glow sticks, will I glow?🔆",
    "Is cereal a soup?🍲",
    "Can I get WiFi by standing on my roof?📶",
    "Does holding your breath make you stronger?💪🏼",
    "🌶,🍑,🍆,🍌 - SUS Right //",
    "Is Calcium stored in your bones?🦴",
    "Can I upload my brain to Google Drive?🧠",
    "Will drinking Red Bull actually give me wings?💸",
    "Can I use pizza as a face mask?🎭",
    "If I meow at cats enough, will they adopt me?🐱‍👤",
    "If I sleep in class, do I absorb knowledge?🧠",
    "Can I get fit just by thinking about the gym?⛹🏻‍♂️",
    "If I clap with one hand, will I time travel?🧳",
    "Will I get a girlfriend 👸🏻 ?",
    "If I am a human, would you love me? 😘",
    "Your IQ is 0 🤣",
    "My IQ is = Albert Einstein ☜(ﾟヮﾟ☜)",
    "Does chicken come from egg or egg come from chicken? 🥚",
    "Is 2 + 2 = 4 ?🤔"
]
base_questions += [f"Dumb Question #{i + 28}?" for i in range(160)]  # Adds 160 total

dumb_questions = base_questions

# Dumb jokes
jokes = [
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "What’s orange and sounds like a parrot? A carrot.",
    "I used to play piano by ear, now I use my hands.",
    "Why don’t eggs tell jokes? They’d crack each other up."
] + [f"Dumb Joke #{i + 5}: This is a really dumb joke!" for i in range(66)] + [
    "Why did the chicken join a band? Because it had the drumsticks!",
    "I told my computer I needed a break, and it said 'No problem, I’ll go to sleep.'",
    "Parallel lines have so much in common… it’s a shame they’ll never meet.",
    "What do you call fake spaghetti? An impasta!",
    "Why can't your nose be 12 inches long? Because then it would be a foot.",
    "I’m on a seafood diet. I see food and I eat it.",
    "I used to be indecisive. Now I’m not so sure.",
    "Why did the math book look sad? Because it had too many problems.",
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "I would avoid the sushi if I was you. It’s a little fishy.",
    "Want to hear a construction joke? Oh... never mind, I’m still working on that one.",
    "Why couldn’t the bicycle stand up by itself? It was two tired.",
    "What do you call a can opener that doesn’t work? A can’t opener.",
    "Did you hear about the guy who invented Lifesavers? He made a mint!",
    "What did one wall say to the other wall? I’ll meet you at the corner.",
    "Why don’t scientists trust atoms? Because they make up everything!",
    "How do you organize a space party? You planet.",
    "What do you get when you cross a snowman and a dog? Frostbite.",
    "I used to work for a blanket factory, but it folded.",
    "Why did the tomato turn red? Because it saw the salad dressing!"
]  # Total: 90 jokes

# Tasks
@tasks.loop(minutes=5)
async def ask_question():
    global current_question, correct_answer, answered_users, question_count
    if target_channel_id:
        channel = bot.get_channel(target_channel_id)
        if channel:
            current_question = random.choice(dumb_questions)
            correct_answer = random.choice(["yes", "no"])
            answered_users.clear()
            question_count += 1
            await channel.send(f"@everyone\n🧠 **Dumb Question Time!**\n{current_question}", allowed_mentions=discord.AllowedMentions(everyone=True))

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")
    ask_question.start()

# Slash commands
@bot.tree.command(name="setchannel", description="Set the channel for dumb questions")
@app_commands.describe(channel="Select the channel")
async def setchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    global target_channel_id
    target_channel_id = channel.id
    await interaction.response.send_message(f"✅ Dumb questions will be posted in {channel.mention} every 5 minutes.", ephemeral=True)

@bot.tree.command(name="yes", description="Answer yes to the dumb question")
async def yes(interaction: discord.Interaction):
    await process_answer(interaction, "yes")

@bot.tree.command(name="no", description="Answer no to the dumb question")
async def no(interaction: discord.Interaction):
    await process_answer(interaction, "no")

async def process_answer(interaction, answer):
    if not current_question:
        await interaction.response.send_message("❌ There's no active question right now!")
        return
    if interaction.user.id in answered_users:
        await interaction.response.send_message(f"🧠 {interaction.user.mention} got temporary memory loss and tried again...")
        return
    answered_users.add(interaction.user.id)
    if answer == correct_answer:
        scores[interaction.user.id] = scores.get(interaction.user.id, 0) + 1
        await interaction.response.send_message(f"✅ {interaction.user.mention} got it right! 🎉")
    else:
        await interaction.response.send_message(f"❌ {interaction.user.mention} is dumb. Better luck next time!")

@bot.tree.command(name="dumbjoke", description="Get a dumb joke")
async def dumbjoke(interaction: discord.Interaction):
    await interaction.response.send_message(f"🤣 {random.choice(jokes)}")

@bot.tree.command(name="dumbkill", description="Humorously stab someone")
@app_commands.describe(target="The user to stab")
async def dumbkill(interaction: discord.Interaction, target: discord.Member):
    await interaction.response.send_message(f"🩸 {interaction.user.mention} stuck a knife in {target.mention}'s brain! Ouch!")

@bot.tree.command(name="dumbslap", description="Humorously slap someone")
@app_commands.describe(target="The user to slap")
async def dumbslap(interaction: discord.Interaction, target: discord.Member):
    await interaction.response.send_message(f"👋 {interaction.user.mention} slapped {target.mention}!")

@bot.tree.command(name="score", description="See your dumb score")
async def score(interaction: discord.Interaction):
    await interaction.response.send_message(f"🎯 {interaction.user.mention}, your score is {scores.get(interaction.user.id, 0)} dumb points.")

@bot.tree.command(name="mysus", description="See how sus you are")
async def mysus(interaction: discord.Interaction):
    percent = random.randint(1, 100)
    await interaction.response.send_message(f"{interaction.user.mention} is {percent}% sus. 😳")

@bot.tree.command(name="brain", description="Check your brain status")
async def brain(interaction: discord.Interaction):
    score_val = scores.get(interaction.user.id, 0)
    await interaction.response.send_message(f"🧠 {interaction.user.mention} has {score_val} dumb points and isn't afraid to flaunt it!")

@bot.tree.command(name="memoryloss", description="Simulate memory loss")
async def memoryloss(interaction: discord.Interaction):
    await interaction.response.send_message(f"💭 {interaction.user.mention} got temporary memory loss!")

@bot.tree.command(name="whoiswinning", description="See who's leading")
async def whoiswinning(interaction: discord.Interaction):
    if not scores:
        await interaction.response.send_message("No one's dumb enough to win yet. 😆")
        return
    winner = max(scores.items(), key=lambda x: x[1])
    await interaction.response.send_message(f"🏅 <@{winner[0]}> is leading with {winner[1]} dumb points!")

@bot.tree.command(name="dumbboard", description="Show the dumb leaderboard")
async def dumbboard(interaction: discord.Interaction):
    if not scores:
        await interaction.response.send_message("Nobody's dumb enough to play yet. 😝")
        return
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    leaderboard = "\n".join([f"<@{uid}>: {score} dumb points" for uid, score in sorted_scores])
    await interaction.response.send_message(f"🏆 **DumbBoard** 🧠\n{leaderboard}")

@bot.tree.command(name="questioncount", description="Total dumb questions asked")
async def questioncount(interaction: discord.Interaction):
    await interaction.response.send_message(f"🤓 We've asked {question_count} dumb questions so far!")

@bot.tree.command(name="topdumbs", description="Alias for dumbboard")
async def topdumbs(interaction: discord.Interaction):
    await dumbboard(interaction)

bot.run(TOKEN)

