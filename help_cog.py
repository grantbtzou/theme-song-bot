import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = ""
        self.text_channel_list = []
        self.set_message()

    def set_message(self): 
        self.help_message = f"""
        ```
        {self.bot.command_prefix}help -- displays all the available commands
        {self.bot.command_prefix}set -- use with a youtube link and a duration in the format {self.bot.command_prefix}set [youtube link] [value up to 30 seconds] to set a theme song
        {self.bot.command_prefix}list -- list users and their songs 
        {self.bot.command_prefix}enable -- enables the bot for you 
        {self.bot.command_prefix}disable -- disables the bot for you 
        {self.bot.command_prefix}prefix -- change bot prefix 
        ```"""
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Set the bot's status to the help command"""
        await self.bot.change_presence(activity=discord.Game(f"type {self.bot.command_prefix}help"))

    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        """Send the help message"""
        await ctx.send(self.help_message)

    @commands.command(name="prefix", help="Change bot prefix")
    async def prefix(self, ctx, *args):
        """Update the bot prefix"""
        self.bot.command_prefix = " ".join(args)
        self.set_message()
        await ctx.send(f"prefix set to **'{self.bot.command_prefix}'**")
        await self.bot.change_presence(activity=discord.Game(f"type {self.bot.command_prefix}help"))
