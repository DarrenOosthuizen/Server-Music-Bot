import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded \n")

    @commands.command(name="help")
    async def help(self,ctx):
        em = discord.Embed(
        url="https://www.flystudio.co.za/discord/musicbot",
        title=f"FlyMusic Bot Commands List",
        description=f"Find current list of commands available for Music Bot",
        color=discord.Colour.green(),
        )
        em.set_author(
            name="FlyMusic Bot Commands",
            icon_url="https://i.imgur.com/l2bO7Ga.jpg"
        )
        em.set_thumbnail(
            url="https://i.imgur.com/l2bO7Ga.jpg"
        )
        em.add_field(
            name="Play Song/Add song to Queue",
            value="`-play {url/songname}`",
            inline=True)
        em.add_field(
            name="Pause Song",
            value="`-pause`",
            inline=True)
        em.add_field(
            name="Resume Song",
            value="`-resume`",
            inline=True)
        em.add_field(
            name="Stop Playing",
            value="`-stop`",
            inline=True)
        em.add_field(
            name="Display songs in Queue",
            value="`-queue`",
            inline=True)
        em.add_field(
            name="Skip song",
            value="`-next/-skip`",
            inline=True)
        em.add_field(
            name="Previous song",
            value="`-previous`",
            inline=True)
        em.add_field(
            name="Shuffle Songs in Queue",
            value="`-shuffle`",
            inline=True)
        em.add_field(
            name="View Song Lyrics",
            value="`-lyrics`",
            inline=True)
        em.add_field(
            name="Skip to song in Queue",
            value="`-skip {songnumber}`",
            inline=True)
        em.add_field(
            name="Seek to time in song",
            value="`-seek {min:sec}{00:00}`",
            inline=True)


        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Help(bot))