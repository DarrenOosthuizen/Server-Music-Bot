from pathlib import Path
import time as t
import datetime
import asyncio
import discord
from discord.ext import commands
from bot.cogs.help import Help
from bot.cogs.music import Music

import threading
import sys

afkTime = 0
lasttime = 0
newMusicSelf = "1"
newPlayerSelf = "1"
disconnected = True
th = None

async def SetMusicSelf(selfobj):
    global newMusicSelf
    newMusicSelf = selfobj

async def SetPlayerSelf(selfobj):
    global newPlayerSelf
    newPlayerSelf = selfobj



class MusicBot(commands.Bot):
    
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True, help_command=None,)

    def setup(self):
        print("Running setup...")
        
        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f" Loaded `{cog}` cog.")

        print("Setup complete.")

    def run(self):
        self.setup()

        with open("data/token.0", "r", encoding="utf-8") as f:
            TOKEN = f.read()

        print("Running bot...")
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f" Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")

    async def on_error(self, err, *args, **kwargs):
        raise

    async def on_command_error(self, ctx, exc):
        raise getattr(exc, "original", exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="-help"))
        print("Bot ready.")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("-")(bot, msg)
        
    async def process_commands(self, msg):
        global disconnected
        global lasttime
        global afkTime
        global th
        
        ctx = await self.get_context(msg, cls=commands.Context)

        
        lasttime = datetime.datetime.now()
        
        
        afkTime = lasttime + datetime.timedelta(minutes = 10)
        lasttime = datetime.datetime.strftime(lasttime,"%H:%M:%S")
        afkTime = datetime.datetime.strftime(afkTime,"%H:%M:%S")

        
        th = threading.Thread(target=asyncio.run, args=(self.timeout(ctx),))
        
        
        
        
        print(disconnected)
        if disconnected:
            disconnected = False
            th.start()
            
        


        if ctx.command is not None:
            await self.invoke(ctx)
        else:
            em = discord.Embed(title=f"INVALID COMMAND",description=f"Command : {ctx.message.content} not found.", color=discord.Colour.red())
            await ctx.send(embed=em)
            await Help.help(self, ctx)         


    # async def process_commands(self, msg):
    #     ctx = await self.get_context(msg, cls=commands.Context)
    #     if ctx.command is not None:
    #         await self.invoke(ctx)
    #     else:
    #         em = discord.Embed(title=f"INVALID COMMAND",description=f"Command : {ctx.message.content} not found.", color=discord.Colour.red())
    #         await ctx.send(embed=em)
    #         await Help.help(self, ctx)

    
    async def timeout(self,ctx):
        try:
            global disconnected
            while disconnected == False:
                print(afkTime)
                newtime = datetime.datetime.now()
                newtime = datetime.datetime.strftime(newtime,"%H:%M:%S")
                if(newtime == afkTime):
                    disconnected = True
                t.sleep(1)
            await Music.disconnect_afk(newMusicSelf,ctx)

        except Exception as e:
            print(e)

    async def testshit(self):
        global th
        th.join()
        print("Send nudes")

    async def afkbot(self,ctx):
        await Music.disconnect_command(newMusicSelf,ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)


