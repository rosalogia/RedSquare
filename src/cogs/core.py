import discord
from discord import Permissions
from discord.ext import commands
from utilities import get_string, fetch_res, update_res
from utilities.configuration import configuration_options
import os
from typing import Dict, Tuple, Any, List

class Core(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Prints message to terminal when bot is ready"""
        print(f"Logged on as {self.bot.user}")

    def prepare_feature_strings(self, guild_config: Dict[str, Any]) -> Tuple[str, str]:
        guild_features = guild_config["features"]
        feature_string = "- " + "\n- ".join(guild_features) if guild_features else "You currently have no features enabled."

        feature_name    = lambda n: n.split(".")[0]
        feature_filter  = lambda n: n.endswith(".py") and feature_name(n) not in guild_features and feature_name(n) != "core"

        available_features = list(map(feature_name, filter(feature_filter, os.listdir("src/cogs/"))))

        available_feature_string = "- " + "\n- ".join(available_features) if available_features else "You have all currently existing features enabled."

        return (feature_string, available_feature_string)

    @commands.command()
    async def configure(self, ctx: commands.Context, feature: str=None, option: str=None, *args) -> None:
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("You do not have sufficient permissions to use this command.")
            return

        guild_configurations = fetch_res("local/guild_configurations")
        guild_config = guild_configurations[str(ctx.guild.id)]
        guild_lang = guild_config["language"]
        
        if feature is None:
            await ctx.send(get_string("configurationHelp", guild_lang) % self.prepare_feature_strings(guild_config))
            return
        else:
            if option is None:
                await ctx.send(get_string(f"{feature}Configuration", guild_lang))
                return
            if option == "enable":
                if feature not in guild_config["features"]:
                    guild_configurations[str(ctx.guild.id)]["features"].append(feature)
                    update_res("local/guild_configurations", guild_configurations)
                    await ctx.send(get_string("featureEnabled", guild_lang) % feature)
                else:
                    await ctx.send(get_string("featureAlreadyEnabled", guild_lang) % feature)
            elif option == "disable":
                if feature in guild_config["features"]:
                    guild_configurations[str(ctx.guild.id)]["features"].remove(feature)
                    update_res("local/guild_configurations", guild_configurations)
                    await ctx.send(get_string("featureDisabled", guild_lang) % feature)
                else:
                    await ctx.send(get_string("featureAlreadyDisabled", guild_lang) % feature)
            else:
                await configuration_options[feature][option](ctx, *args)

    @commands.command()
    async def help(self, ctx: commands.Context, option: str=None) -> None:
        guild_config = fetch_res("local/guild_configurations")[str(ctx.guild.id)]
        guild_lang = guild_config["language"]
        embed = discord.Embed(title=get_string("help", guild_lang), description=get_string("description", guild_lang))

        embed.add_field(name=get_string("usage", guild_lang), value=get_string("usageHelp", guild_lang), inline=False)

        feature_name    = lambda n: n.split(".")[0]
        feature_filter  = lambda n: n.endswith(".py") and feature_name(n) != "core"

        features = list(map(feature_name, filter(feature_filter, os.listdir("src/cogs/"))))
        feature_string = "- " + "\n- ".join(features) if features else "You have all currently existing features enabled."

        embed.add_field(name=get_string("features", guild_lang), value=feature_string, inline=False)

        await ctx.send(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Core(bot))
