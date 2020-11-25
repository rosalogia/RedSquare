import discord
from discord.ext import commands
from utilities import get_res, fetch_res, get_string, feature_users

class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        guild_id = member.guild.id

        if guild_id not in feature_users("verification"):
            return

        gcs = fetch_res("local/guild_configurations")

        guild_config = gcs[str(guild_id)]
        guild_lang = guild_config["language"]
        
        if "verificationMessage" in guild_config["strings"]:
            await member.send(guild_config["strings"]["verificationMessage"])
        else:
            await member.send(get_string("verificationMessage", guild_lang))

        response = await self.bot.wait_for(
            # pyre-ignore[16]: Pyre lacks information about the member class, causing faulty errors
            "message", check=lambda m: m.channel.id == member.dm_channel.id and m.author.id == member.id
        )

        if "verificationChannel" in guild_config["channels"]:
            verification_channel = self.bot.get_channel(guild_config["channels"]["verificationChannel"])
        else:
            verification_channel = self.bot.get_guild(guild_id).owner.dm_channel

        await verification_channel.send(
            get_string("verificationReport", guild_lang) + f"{member.mention}:\n\n{response.content}"
        )

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Verification(bot))
