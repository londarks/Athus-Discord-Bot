import discord
from discord.ext import commands
import asyncio
from imgurpython import ImgurClient
from random import randint 




class Imgur(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def imgur(self, ctx):
        """Search img imgur"""
        imgur = ctx.message.content[7:]
        client_id = 'd3189edc3d92749'
        client_secret = '6287a3394b72977dec4cc4fa9f282f2ad907987b'
        
        client = ImgurClient(client_id, client_secret)
        link = []
        # Example request
        items = client.gallery_search(imgur, advanced=None, sort='Best', window='all', page=0)
        for item in items:
            link.append(item.link)
        x = randint(0,len(link))
        await ctx.send(link[x])
        self.client.counter += 1



def setup(client):
    client.add_cog(Imgur(client))