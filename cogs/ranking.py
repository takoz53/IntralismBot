import discord
from discord.ext import commands
from utils.playerinfo import PlayerInfo
from cogs.userdata import UserDataCog
from utils.extensions import Extensions
from utils.rank_scraper import scrapeTop
from utils.graphcreator import createGraph

class RankingsCog(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
    
    def createEmbed(self, **kwargs):
        embed = discord.Embed(title=f"Statistics about {kwargs['username']}", color=kwargs['color'])
        embed.add_field(name="Global Ranking",value=f"{kwargs['global_rank']} / {kwargs['global_max']}")
        embed.add_field(name="Country Ranking",value=f"{kwargs['country_rank']} / {kwargs['country_max']}")
        embed.add_field(name="Average Accuracy",value=kwargs['average_accuracy'])
        embed.add_field(name="Average Misses",value=kwargs['average_misses'])
        embed.add_field(name="Steam URL",value=f"[{kwargs['username']}'s Steam Profile]({kwargs['steam_link']})")
        embed.set_image(url=kwargs['avatar'])
        embed.set_footer(text="Information fetched from Intralism Website.")
        return embed

    def showRank(self, steamID):
        """Gets Player Info and returns the created embed to it"""
        pInfo = PlayerInfo(steamID)
        embed = self.createEmbed(
            username=pInfo.userName,
            color=pInfo.getColor(int(pInfo.globalRank)),
            global_rank=pInfo.globalRank,
            global_max=pInfo.globalMax,
            country_rank=pInfo.countryRank,
            country_max=pInfo.countryMax,
            average_accuracy=pInfo.accuracy,
            average_misses=pInfo.misses,
            steam_link=pInfo.steamLink,
            avatar=pInfo.pictureURL
        )

        return embed

    async def displayAuthorRank(self, ctx : commands.Context):
        """Displays the rank of the message Author"""
        result = Extensions.userExists(ctx.author.id)
        
        if result:
            await ctx.send(embed=self.showRank(result[0]))
        else:
            await ctx.send("Can't find a Profile associated to your ID, please create one by using the command: \"link\"")
            

    async def displayRank(self, ctx, steamID):
        """Displays Rank of specific User"""
        newSteamID = Extensions.convertSteamData(steamID)
        if newSteamID is None:
            await ctx.send("The entered value is not a valid SteamID.")
            return
            
        await ctx.send(embed=self.showRank(newSteamID))
    

    @commands.command(name="top10", aliases=['top', 'topten', 'toplist', 'topplayers'])
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def printTop10(self, ctx: commands.Context):
        """ - Prints top10 Players of Intralism"""
        #Command will be blocked throughout Guild due to being a general command for everyone to see.
        #CreateTable called from Graph
        await ctx.trigger_typing()
        players = [PlayerInfo().from_object(item) for item in scrapeTop()]
        createGraph(players)
        await ctx.send(file=discord.File("top.png"))


    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rank(self, ctx: commands.Context, steamID=None):
        """- This command displays your rank or another Player its rank with the SteamID / URL as parameter"""
        await ctx.trigger_typing()
        if steamID:
            try:
                await self.displayRank(ctx, steamID)
            except ValueError:
                await ctx.send("The given SteamID hasn't played Intralism yet or doesn't exist at all.")
            return
        try:
            await self.displayAuthorRank(ctx)
        except ValueError:
            await ctx.send("There was an error fetching the given SteamID / URL.")
    
    
def setup(bot):
    bot.add_cog(RankingsCog(bot))
