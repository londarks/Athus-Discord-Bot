import discord
from discord.ext import commands
import asyncio
from io import BytesIO
import os, re
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps
from itertools import cycle



class Meme(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def trump(self, ctx):
        """memes do donalt trump coma pasta"""
        meme = ctx.message.content[7:]
        if len(meme) > 107:
            await ctx.send("Menssagem muito grande")
            return
        fundo = Image.open('img/mesmes/trump.jpg')
        Fonte = ImageFont.truetype('fonts/uni-sans.heavy-caps.otf',90)
        escreve = ImageDraw.Draw(fundo)
        a1, r, ter = 1, 1, len(meme)+1
        # nosso "paginador"
        itens_por_linha = 20
        ends = [''] * (itens_por_linha - 1)
        ends.append('\n')
        a = 0
        eixo_x = 740
        eixo_y = 570
        quebra = 1
        for item, end in zip(range(a1, r * ter, r), cycle(ends)):
            #print("i", end=end)
            #print(meme[item], end=end)
            if quebra == 20:
                quebra = 1
                eixo_y += 100 
                eixo_x = 740
            #print(meme[a],end=end)
            escreve.text(xy=(eixo_x,eixo_y), text=meme[a],end=end, fill=(13, 13, 13), font=Fonte)
            eixo_x += 50
            a += 1
            quebra += 1
        fundo.save('img/mesmes/trump_1.png')
        info_png = discord.File('img/mesmes/trump_1.png')
        await ctx.send(file=info_png)
        self.client.counter += 1
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def robin(self, ctx):
        """memes do robin levando tapa"""
        meme = ctx.message.content[7:]
        if len(meme) > 38:
            await ctx.send("Menssagem muito grande")
            return
        fundo = Image.open('img/mesmes/robin.jpg')
        Fonte = ImageFont.truetype('fonts/uni-sans.heavy-caps.otf',22)
        escreve = ImageDraw.Draw(fundo)
        a1, r, ter = 1, 1, len(meme)+1
        # nosso "paginador"
        itens_por_linha = 14
        ends = [''] * (itens_por_linha - 1)
        ends.append('\n')
        a = 0
        eixo_x = 10
        eixo_y = 10
        quebra = 1
        for item, end in zip(range(a1, r * ter, r), cycle(ends)):
            if quebra == 14:
                quebra = 1
                eixo_y += 30 
                eixo_x = 10
            escreve.text(xy=(eixo_x,eixo_y), text=meme[a],end=end, fill=(13, 13, 13), font=Fonte)
            eixo_x += 15
            a += 1
            quebra += 1
        fundo.save('img/mesmes/robin_1.png')
        info_png = discord.File('img/mesmes/robin_1.png')
        await ctx.send(file=info_png)
        self.client.counter += 1



    # @commands.cooldown(1,5,commands.BucketType.user)
    # @commands.command()
    # async def (self, ctx):
    #     """meme do bolsonaro vendo tv"""
    #     ...

def setup(client):
    client.add_cog(Meme(client))