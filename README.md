# theme-song-bot
A Python Discord bot that plays music when users join voice call. 



## Setup 
Create your bot following the discord docs: https://discordpy.readthedocs.io/en/stable/discord.html

Install depdencies
```
pip install poetry
poetry init
```
Create a .env file and set TOKEN="YOUR BOT'S TOKEN"

## Start the bot 
```
python main.py
```
## Usage: 
```
help -- displays all the available commands
set -- use with a youtube link and a duration in the format {self.bot.command_prefix}set [youtube link] [value up to 30 seconds] to set a theme song
list -- list users and their songs 
enable -- enables the bot for you 
disable -- disables the bot for you 
prefix -- change bot prefix 
```


