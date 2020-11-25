from typing import List
from utilities import get_res, get_string
from discord.ext import commands
import discord
from parse import parse
# Verification

async def message(ctx: commands.Context, *args) -> None:
    with get_res("local/guild_configurations") as guild_configurations:
        guild_configurations[str(ctx.guild.id)]["strings"]["verificationMessage"] = args[0]
        guild_lang = guild_configurations[str(ctx.guild.id)]["language"]

        await ctx.send(get_string("verificationMessageSet", guild_lang))

async def channel(ctx: commands.Context, *args) -> None:
    with get_res("local/guild_configurations") as guild_configurations:
        guild_lang = guild_configurations[str(ctx.guild.id)]["language"]
        try:
            channel = ctx.bot.get_channel(int(parse("<#{}>", args[0])[0]))
            if channel is None:
                raise ValueError("Channel invalid")
            guild_configurations[str(ctx.guild.id)]["channels"]["verificationChannel"] = channel.id
            await ctx.send(get_string("verificationChannelSet", guild_lang) % args[0])
        except ValueError:
            await ctx.send(get_string("invalidChannel", guild_lang))


configuration_options = {
        "verification": {
            "message": message,
            "channel": channel
        }
}
