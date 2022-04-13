import config
import discord
from discord import Client
from discord.ext import commands
from music import Music


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents = intents)

@bot.event
async def on_ready():
    print ("Ready")

#add cogs to the bot
bot.add_cog(Music(bot))

bot.run(config.DISCORD_BOT_TOKEN)

