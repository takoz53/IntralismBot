import discord
from discord.ext import commands
from utils.extensions import Extensions

class UserDataCog(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot

    @commands.command(name="link")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def linkProfile(self, ctx : commands.Context, steamID = None):
        """- This command allows you to link yourself to a SteamID with the SteamID as Parameter"""
        #No parameter given
        newSteamID = Extensions.convertSteamData(steamID)

        if newSteamID is None:
            await ctx.send("Couldn't parse your Steam ID / URL!")
            return
        
        await self.checkAndModifyProfile(ctx, newSteamID)

    async def checkAndModifyProfile(self, ctx : commands.Context, steamID):
        """Function which creates or modifies profiles"""
        discordID = ctx.author.id
        user = Extensions.userExists(discordID)
        if user:
            self.overwriteProfile(discordID, steamID)
            await ctx.send(f"{ctx.author.mention}, I overwrote your old Profile Data.")
        else:
            self.createProfile(discordID, steamID)
            await ctx.send(f"{ctx.author.mention}, I created a new Profile. now you can use the rank command")
    
    def overwriteProfile(self, discordID, steamID):
        """Function which overwrites the current Profile"""
        c = Extensions.SQLiteConnection.cursor()
        c.execute("""UPDATE profilelink SET steamID = :steamID WHERE discordID = :discordID""",{
            'steamID': steamID, 'discordID': discordID
        })
        Extensions.SQLiteConnection.commit()
        return

    def createProfile(self, discordID, steamID):
        """Function which creates a new Profile"""
        c = Extensions.SQLiteConnection.cursor()
        c.execute("INSERT INTO profilelink VALUES (?, ?)", (steamID, discordID))
        Extensions.SQLiteConnection.commit()
        return

def setup(bot):
    bot.add_cog(UserDataCog(bot))
