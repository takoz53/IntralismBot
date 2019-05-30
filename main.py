import discord
from utils.extensions import Extensions
from discord.ext import commands
import json
from discord import Member
import os
import sqlite3

#Bot Setup, e.g. Help, Description & Command Prefix
configFile = "config.json"
steamAPIKey = ""
discordAPIKey = ""
commandPrefix = ">"
description = "Intralism Utility Bot"

bot = commands.Bot(command_prefix=commandPrefix, description=description)

initial_extensions = ["cogs.ranking", "cogs.admin", "cogs.userdata" ]

def createDatabase():
    c = Extensions.SQLiteConnection.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS profilelink (
        steamID text,
        discordID UNSIGNED BIG INT
    )""")
    Extensions.SQLiteConnection.commit()

#Check if this is the main file
#If yes, load all cogs in.
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
    createDatabase()

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.send_message(ctx.message.channel, content='This command is on a %.2fs cooldown' % error.retry_after)
        raise error

@bot.event
async def on_ready():
    """Command being called, when the Bot is ready."""
    print("Authentificated as:", bot.user.name,", ID:", bot.user.id)
    await bot.change_presence(activity=discord.Game(name='servant for others.'))

def createConfig():
    """Creates Config File"""
    if os.path.exists(configFile):
        return False
    data = {
    'DiscordAPI': ''
    }

    with open(configFile, "w") as outfile:
        json.dump(data, outfile)
    return True

def readConfig():
    """Creates new Config if there was none before, else reads Data"""
    global discordAPIKey
    newFile = createConfig()
    if newFile == True:
        os._exit(0)
    else:
        with open(configFile) as json_file:  
            data = json.load(json_file)
            discordAPIKey = data["DiscordAPI"]
readConfig()

bot.run(discordAPIKey)


