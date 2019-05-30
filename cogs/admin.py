from discord.ext import commands


class AdminCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # Shutdown the bot.
    @commands.command(name='shutdown', hidden=True)
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        await self.bot.logout()
        quit(0)
    
    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.has_permissions(administrator=True)
    async def loadCog(self, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            print(f"Error loading Cog: {type(e).__name__} - {e}")
        else:
            print(f"Success in loading {cog}")

    @commands.command(name='unload', hidden=True)
    @commands.has_permissions(administrator=True)
    async def unloadCog(self, cog: str):
        """Command which Unloads a Module.\n
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            print(f"Error unloading Cog: {type(e).__name__} - {e}")
        else:
            print(f"Success in unloading {cog}")

    @commands.command(name='reload', hidden=True)
    @commands.has_permissions(administrator=True)
    async def reloadCog(self, cog: str):
        """Command which Reloads a Module.\n
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
           print(f"Error reloading Cog: {type(e).__name__} - {e}")
        else:
            print(f"Success in reloading {cog}")


def setup(bot):
    bot.add_cog(AdminCog(bot))