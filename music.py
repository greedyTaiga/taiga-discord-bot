import discord
from discord import Client
from discord.ext import commands
from discord import FFmpegPCMAudio
import youtube_dl

#options used to fetch the song from Youtube and create an OPUS encoded source from it
YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
FFMPEG_OPTIONS = {
    'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

#uses video_id as a search request from Youtube, uses the first entry in results, returning it as an OPUS encoded source
async def get_source(video_id):
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            song_url = ydl.extract_info(f"ytsearch:{video_id}", download=False)['entries'][0]['formats'][0]['url']

            source = await discord.FFmpegOpusAudio.from_probe(song_url, **FFMPEG_OPTIONS)
            return source

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = dict()

    async def play_next_song(self, ctx):
        id = ctx.guild.id
        vc = ctx.voice_client
        if self.song_queue[id] != [] and (vc):
            song_name = self.song_queue[id].pop(0)
            source = await get_source(song_name)
            await ctx.send(f"Playing the {song_name} now.")
            vc.play(source, after = lambda err = None : self.bot.loop.create_task( self.play_next_song(ctx) ) )

    @commands.command(pass_context = True)
    async def play(self, ctx, *args):

        if len(args) == 0:
            return await ctx.send("Give a name to a song please.")

        song_name = " ".join(args)

        if ctx.author.voice is None:
            await ctx.send("You are not connected to any channels.")
            return
        
        if ctx.guild.id not in self.song_queue: 
            self.song_queue[ctx.guild.id] = []
        
        if ctx.voice_client is None:
            vc = await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel.id != ctx.author.voice.channel.id:
            vc = await ctx.voice_client.move_to(ctx.author.voice.channel)
        else:
            vc = ctx.voice_client
        
        if vc.is_playing():
            self.song_queue[ctx.guild.id].append(song_name)
        else:
            source = await get_source(song_name)
            await ctx.send(f"Playing the {song_name} now.")
            vc.play(source, after = lambda err = None : self.bot.loop.create_task( self.play_next_song(ctx) ) )

    @commands.command(pass_context = True)
    async def skip(self, ctx):
        vc = ctx.voice_client
        if vc is None or not vc.is_playing():
            return
        vc.stop()

    @commands.command(pass_context = True)
    async def stop(self, ctx):
        id = ctx.guild.id
        vc = ctx.voice_client
        self.song_queue[id].clear()

        if vc is None:
            return await ctx.send("Not playing anything")

        vc.stop()
        await vc.disconnect()
        await ctx.send(f"Stopped playing.")

    @commands.command(pass_context = True)
    async def pause(ctx):
        vc = ctx.voice_client
        if vc is None or not vc.is_playing():
            return await ctx.send("Not playing anything.")
        if vc.is_paused():
            return await ctx.send("Already paused")
        
        vc.pause()
        return await ctx.send("Paused.")

    @commands.command(pass_context = True)
    async def resume(ctx):
        vc = ctx.voice_client
        if vc is None or (not vc.is_playing() and not vc.is_paused()):
            return await ctx.send("Not playing anything.")
        if not vc.is_paused():
            return await ctx.send("Already playing.")
        
        vc.resume()
        return await ctx.send("Resumed.")