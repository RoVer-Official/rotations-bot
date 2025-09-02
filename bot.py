import discord
from discord.ext import tasks, commands
import datetime
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Rotation schedule
rotation = {
    "A": ["Period 4", "Period 8"],
    "B": ["Period 3", "Period 7"],
    "C": ["Period 2", "Period 6"],
    "D": ["Period 1", "Period 5"],
}

# First A day (adjust if needed)
start_date = datetime.date(2025, 9, 2)

# Holiday list...
holidays = {
    datetime.date(2025, 9, 1),   # Labor Day
    datetime.date(2025, 9, 23), datetime.date(2025, 9, 24),  # Rosh Hashanah
    datetime.date(2025, 10, 2),  # Yom Kippur
    datetime.date(2025, 10, 13), # Columbus Day
    datetime.date(2025, 10, 20), # Diwali
    datetime.date(2025, 11, 6), datetime.date(2025, 11, 7),  # NJEA
    datetime.date(2025, 11, 27), datetime.date(2025, 11, 28),  # Thanksgiving
    datetime.date(2025, 12, 24), datetime.date(2025, 12, 25),
    datetime.date(2025, 12, 26), datetime.date(2025, 12, 29),
    datetime.date(2025, 12, 30), datetime.date(2025, 12, 31),  # Winter Break
    datetime.date(2026, 1, 1),   # New Year’s
    datetime.date(2026, 1, 19),  # MLK
    datetime.date(2026, 2, 16),  # Presidents
    datetime.date(2026, 2, 17),  # Lunar New Year
    datetime.date(2026, 2, 18), datetime.date(2026, 2, 19), datetime.date(2026, 2, 20),  # Feb Break
    datetime.date(2026, 3, 30), datetime.date(2026, 3, 31),  # Spring Recess
    datetime.date(2026, 4, 1), datetime.date(2026, 4, 2),    # Spring Recess
    datetime.date(2026, 4, 3),  # Good Friday
    datetime.date(2026, 5, 25), # Memorial Day
    datetime.date(2026, 6, 19), # Juneteenth
}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    announce_rotation.start()

def get_rotation_day():
    today = datetime.date.today()
    # Count only valid school days since start_date
    days = list(rotation.keys())
    count = 0
    d = start_date
    while d < today:
        if d.weekday() < 5 and d not in holidays:
            count += 1
        d += datetime.timedelta(days=1)
    day_index = count % len(days)
    day_name = days[day_index]
    dropped = rotation[day_name]
    return day_name, dropped

@tasks.loop(minutes=1)
async def announce_rotation():
    now = datetime.datetime.now()
    if now.hour == 6 and now.minute == 0:
        today = datetime.date.today()
        if today.weekday() >= 5 or today in holidays:
            return
        channel = bot.get_channel(CHANNEL_ID)
        day_name, dropped = get_rotation_day()
        drop_text = " and ".join(dropped)
        await channel.send(f"📢 Today is **{day_name} Day** — {drop_text} drop!")

bot.run(TOKEN)
