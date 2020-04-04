import discord
from discord.ext import commands
import asyncio
from io import BytesIO
import os, re
import json
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps




class Sound(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def teste(self, ctx):
        background_teste = ctx.message.content[7:]
        if background_teste == 'Locked':
            return
        try:
            badges_import_1 = Image.open("img/badges/admin_badges.png")
            badges_import_2 = Image.open("img/badges/console_badges.png")
            badges_import_3 = Image.open("img/badges/bug_badges.png")
            badges_import_4 = Image.open("img/badges/ahegao_badges.png")
            badges_import_5 = Image.open("img/badges/100k_badges.png")
            badges_import_6 = Image.open("img/badges/1000k_badges.png")      

            back_ground = Image.open("img/background/theme_{}_backgroun.png".format(background_teste))
            avatar = Image.open('img/teste.png')
            fundo = Image.open('img/profile.png')
            nome_fonte = ImageFont.truetype('fonts/uni-sans.heavy-caps.otf',35)
            lvl_resp = ImageFont.truetype('fonts/uni-sans.heavy-caps.otf',50)
            cash_rank = ImageFont.truetype('fonts/uni-sans.heavy-caps.otf',30)

            back_ground.paste(fundo, (0, 0), fundo)

            nome = ImageDraw.Draw(back_ground)
            nome.text(xy=(210,230), text="Athus", fill=(255, 255, 255), font=nome_fonte)

            Level = ImageDraw.Draw(back_ground)
            Level.text(xy=(521,47), text="99", fill=(13, 13, 13), font=lvl_resp)

            Resp = ImageDraw.Draw(back_ground)
            Resp.text(xy=(521,150), text="99", fill=(13, 13, 13), font=lvl_resp)

            Cash_money = ImageDraw.Draw(back_ground)
            Cash_money.text(xy=(94,315), text="$900000", fill=(13, 13, 13), font=cash_rank)

            Rank = ImageDraw.Draw(back_ground)
            Rank.text(xy=(94,380), text="#1", fill=(13, 13, 13), font=cash_rank)

            back_ground.paste(avatar, (33, 108), avatar)

            back_ground.paste(badges_import_1, (360, 283), badges_import_1)

            back_ground.paste(badges_import_2, (430, 283), badges_import_2)

            back_ground.paste(badges_import_3, (501, 283), badges_import_3)

            back_ground.paste(badges_import_4, (360, 356), badges_import_4)

            back_ground.paste(badges_import_5, (432, 356), badges_import_5)

            back_ground.paste(badges_import_6, (503, 356), badges_import_6)

            back_ground.save('img/status.png')
            info_png = discord.File('img/status.png')
            await ctx.send(file=info_png)
            self.client.counter += 1

        except Exception as e:
            await ctx.send("Não temos esse Background.!")
            self.client.counter += 1



def setup(client):
    client.add_cog(Sound(client))