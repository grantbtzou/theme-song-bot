import asyncio
import discord 
import re 
import requests 
import yt_dlp as youtube_dl
from discord.ext import commands 

from youtube_dl import YoutubeDL

class music_cog(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot

        self.FFMPEG_OPTIONS = {'options': '-vn'}
     
        self.vc = None 

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after): 
        """Join voice call to play music for enabled users"""
        ytdl_format_options = {
            'format': 'bestaudio/best',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0' 
        }
        # Join if a channel was switched
        if before.channel != after.channel: 
            with open("users.txt") as file: 
                content = file.read()
                pattern = re.compile(r'(\d+),\s*([^,]+),\s*(\d+)\b,\s*([^\n]+)')
                matches = pattern.findall(content)
                foundUser = False
                # Search for the user that just joined in the user file 
                for match in matches: 
                    if match[0] == str(member.id) and match[3] == "ON": 
                        voice_channel = await member.voice.channel.connect()
                        link = match[1]
                        duration = int(match[2]) + 2
                        foundUser = True
                if not foundUser: 
                    return
        # Get the song and play it, then disconnect 
        with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
            info = ydl.extract_info(link, download=False)
            url2 = info['url']
        voice_channel.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('done', e))
        await asyncio.sleep(duration)
        await voice_channel.disconnect()
        return 
    
    @commands.command(name="set song", aliases=["set"], help="Set your theme song with a YouTube link")
    async def set_song(self, ctx, *args): 
        """Set the song for the user"""
        # Set the song duration 
        song_duration = 10
        if(len(args) == 0): 
            await ctx.send("Provide a url and duration") 
            return 
        if(len(args) == 1): # Default for no provided duration
            song_duration = 10
        else:
            if(int(args[1]) > 30): 
                await ctx.send("Max duration 30 seconds, duration set to 10 seconds") 
                song_duration = 10
            else: 
                song_duration = args[1] 
        # Get the URL and check if it works 
        url = args[0] 
        r = requests.get(url)
        if "Video unavailable" in r.text: 
            await ctx.send("Invalid link, try another")
            return
        user_id = str(ctx.author.id) 
        # Read the current list and update 
        with open('users.txt') as file:
            content = file.read()
            pattern = re.compile(r'(\d+),\s*([^,]+),\s*(\d+)\b,\s*([^\n]+)')
            matches = pattern.findall(content)
            found = False
            for match in matches: 
                if match[0] == user_id:
                    content, numreplacements= re.subn(rf'{user_id},\s*([^,]+),\s*(\d+)\b,\s*([^\n]+)',f"{match[0]}, {url}, {song_duration}, ON\n",content)
                    found = True
            if not found: 
                content += f"{user_id}, {url}, {song_duration}, ON\n"
        with open('users.txt', 'w') as file: 
            file.write(content)
        await ctx.send(f'{url} set as theme song, duration: {song_duration} seconds') 
        return
    
    @commands.command(name="list users", aliases=["list"], help="list the current users and their songs")
    async def list_songs(self, ctx, *args): 
        """List the current users and their songs"""
        pattern = re.compile(r'\b(\d+),\s*([^,]+),\s*(\d+)\b,\s*([^,]+)')
        message = ""
        # Search the text file and create a message with all of the information 
        with open('users.txt') as file: 
            for line in file: 
                match = pattern.search(line)
                if match: 
                    user = await self.bot.fetch_user(match.group(1))
                    message += f'{user.display_name}: {match.group(4)}<{match.group(2)}>\nDuration: {match.group(3)} seconds\n'
            await ctx.send(message)
        return
    
    @commands.command(name="enable", help="allows the bot to play for the user")
    async def enable(self, ctx, *args):
        """Enable the bot for the user"""
        user_id = str(ctx.author.id) 
        with open('users.txt') as file: 
            content = file.read() 
            pattern = re.compile(r'\b(\d+),\s*([^,]+),\s*(\d+)\b,\s*([^,]+)')
            # Try and replace the user's line with a line containing ON if the ID matches and it does not contain ON, otherwise make no changes 
            content, num_replacements = pattern.subn(
            lambda match: f"{match.group(1)}, {match.group(2)}, {match.group(3)}, ON\n" if str(match.group(1)) == user_id and match.group(4) != "ON\n" 
            else match.group(0), content
            )
        with open('users.txt', 'w') as file: 
            file.write(content)
            if num_replacements == 0: 
                await ctx.send("Already enabled") 
            else: 
                await ctx.send("Enabled ")
        return 
    
    @commands.command(name="disable", help="stops the bot from playing for the user")
    async def disable(self, ctx, *args):
        """Disable the bot for the user"""
        user_id = str(ctx.author.id) 
        with open('users.txt') as file: 
            content = file.read() 
            pattern = re.compile(r'\b(\d+),\s*([^,]+),\s*(\d+)\b,\s*([^,]+)') 
            # Try and replace the user's line with a line containing OFF if the ID matches and does not contain OFF, otherwise make no changes 
            content, num_replacements = pattern.subn(
            lambda match: f"{match.group(1)}, {match.group(2)}, {match.group(3)}, OFF\n" if str(match.group(1)) == user_id and match.group(4) != "OFF\n" 
            else match.group(0), content
            )
        with open('users.txt', 'w') as file: 
            file.write(content)
            if num_replacements == 0: 
                await ctx.send("Already disabled") 
            else: 
                await ctx.send("Disabled")
        return 