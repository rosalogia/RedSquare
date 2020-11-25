import json
import discord
from discord.ext import commands
from utilities import get_config, create_ine, get_res
from datetime import datetime
from typing import Dict, Any

config: Dict[str, Any] = get_config()

class bcolors:
    HEADER      = "\033[95m"
    OKBLUE      = "\033[94m"
    OKGREEN     = "\033[92m"
    WARNING     = "\033[93m"
    FAIL        = "\033[91m"
    ENDC        = "\033[0m"
    BOLD        = "\033[1m"
    UNDERLINE   = "\033[4m"

intents: discord.Intents = discord.Intents.default()
intents.members = True
intents.guilds  = True

# Initialize bot with prefix '!'
bot: discord.Client = commands.Bot(command_prefix=commands.when_mentioned, intents=intents, help_command=None)

# This file will be referenced in other cogs, so make sure it's created here!
create_ine("res/guild_configurations.json")

@bot.event
async def on_guild_join(guild: discord.Guild) -> None:
    with get_res("local/guild_configurations") as guild_configs:
        if str(guild.id) not in guild_configs.keys():
            guild_configs[str(guild.id)] = {"language": "en", "channels": {}, "strings": {}, "features": []}

# Load extensions specified in features
for feature in config["features"]:
    try:
        bot.load_extension(f"cogs.{feature}")
    except Exception as e:
        print(f"{bcolors.FAIL}WARN: Cog {feature} failed to load{bcolors.ENDC}")
        with open("log.txt", "a") as log_file:
            current_time = datetime.now().strftime("%H:%M:%S")
            msg = f"[{current_time}] in cog {feature}:\n{e}\n\n"
            log_file.write(msg)

# Run the bot using the token in config.json
bot.run(config["botToken"])
