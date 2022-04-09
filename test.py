#dependencies

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

from sys import exit

import requests
import random
import json

import time

#import from apikeys
from apikeys import *

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!', intents = intents)

@client.event
async def on_ready():
    print ("Ready!")

@client.event
async def on_member_join(member):
    channel = client.get_channel(959151558707269694)
    await channel.send(f"Oglanliqin bulundugu servere xos geldin {member.name}.")

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.author.voice.channel
        audio = await channel.connect()
        source = FFmpegPCMAudio(r'.\MediaResources\happy_creative_sunday.mp4')
        player = audio.play(source)
    else:
        await ctx.send("No channel to join.")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the voice chanell.")
    else:
        await ctx.send("Not connected to any chanells right now.")

@client.command(pass_context = True)
async def play(ctx):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(r'.\MediaResources\happy_creative_sunday.mp4')
    player = voice.play(source)
    

@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if (voice.is_playing()):
        voice.pause()

@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if (voice.is_paused()):
        voice.resume()
"""
@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    voice.stop()
"""

@client.command()
async def vindiesel(ctx):
    print ("Started")
    url = "https://instagram85.p.rapidapi.com/account/vindiesel/info"

    headers = {
	    "X-RapidAPI-Host": "instagram85.p.rapidapi.com",
	    "X-RapidAPI-Key": INSTA_APIKEY
    }

    response = requests.request("GET", url, headers=headers)

    response_dict = json.loads(response.text)

    posts = response_dict['data']['feed']['data']
    
    random_post = random.choice(posts)
    print (random_post)

    await ctx.send(random_post['images']['original']['high'])
    print ("picture sent")
    await ctx.send(random_post['caption'])
    print ("caption sent")


client.run(TOKEN)

#Half baked features
'''
Vin Diesel says Happy creative sunday when somebody joins the voice channel, 
it works but the bot doesn't disconnect from the channel automatically after doing that

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel:
        channel = client.get_channel(959151558707269695)
        
        audio = await channel.connect()
        source = FFmpegPCMAudio(r'.\MediaResources\happy_creative_sunday.mp4')
        player = audio.play(source)
        time.sleep(3)
        channel = client.get_channel(959151558707269694)
        await channel.send("!leave")
'''