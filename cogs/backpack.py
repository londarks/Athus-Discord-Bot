import discord
from discord.ext import commands
import asyncio
import json
import sqlite3





class Backpack(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()

    @commands.cooldown(1,20,commands.BucketType.user)
    @commands.command()
    async def inventory(self, ctx):
        first_run = True
        usuario_id = ctx.author.id
        while True:
            if first_run:
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/W2DJnVc.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Backpack De {}".format(ctx.author))
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="BackGround", value="🌆", inline=True)
                embed.add_field(name="badges", value="🔵", inline=True)
                embed.add_field(name="Box", value="🎁", inline=True)
                first_run = False
                msg = await ctx.send(embed=embed)

            reactmoji = []
            reactmoji.extend(['🌆'])
            reactmoji.append('🔵')
            reactmoji.append('🎁')
            reactmoji.append('❌')
    
            for react in reactmoji:
                await msg.add_reaction(react)
    
            def check_react(reaction, user):
                if reaction.message.id != msg.id:
                    return False
                if user != ctx.message.author:
                    return False
                if str(reaction.emoji) not in reactmoji:
                    return False
                return True
    
            try:
                res, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check_react)
            except asyncio.TimeoutError:
                return await msg.clear_reactions()
            if user != ctx.message.author:
                pass
            elif '🌆' in str(res.emoji):
                
                self.cursor.execute('SELECT nome_item From inventario WHERE id_usuario="%s" AND tipo_item="theme"'% (usuario_id))
                temas = self.cursor.fetchall()
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/W2DJnVc.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Backpack De {}".format(ctx.author))
                embed.set_footer(text="Athus V1.0")
                teste = []
                if temas == teste:
                    embed.add_field(name="BackGround", value="...", inline=True)
                else:
                    for i in range(len(temas)):
                        embed.add_field(name="BackGround", value=temas[i][0], inline=True)
                await msg.clear_reactions()
                await msg.edit(embed=embed)
                
            elif '🔵' in str(res.emoji):
                #await ctx.message.delete()
                #return await msg.delete()
                self.cursor.execute('SELECT nome_item From inventario WHERE id_usuario="%s" AND tipo_item="badges"'% (usuario_id))
                comquistas = self.cursor.fetchall()
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/W2DJnVc.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Backpack De {}".format(ctx.author))
                embed.set_footer(text="Athus V1.0")
                teste = []
                if comquistas == teste:
                    embed.add_field(name="Badges", value="...", inline=True)
                else:
                    for i in range(len(comquistas)):
                        embed.add_field(name="Badges", value=comquistas[i][0], inline=True)
                await msg.clear_reactions()
                await msg.edit(embed=embed)
             

            elif '🎁' in str(res.emoji):
                self.cursor.execute('SELECT nome_item From inventario WHERE id_usuario="%s" AND tipo_item="boxes"'% (usuario_id))
                caixa = self.cursor.fetchall()
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/W2DJnVc.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Backpack De {}".format(ctx.author))
                embed.set_footer(text="Athus V1.0")
                teste = []
                if caixa == teste:
                    embed.add_field(name="Box", value="...", inline=True)
                else:
                    for i in range(len(caixa)):
                        embed.add_field(name="Box", value=caixa[i][0], inline=True)
                await msg.clear_reactions()
                await msg.edit(embed=embed)  

            elif '❌' in str(res.emoji):
                await ctx.message.delete()
                return await msg.delete()
        self.client.counter += 1


        # embed.add_field(name="Themes", value=temas, inline=True)
        #for i in range(len(comquistas)):
        #    embed.add_field(name="badges", value=comquistas[i], inline=True)
        # embed.add_field(name="Waifu", value=otaku, inline=True)
        # embed.add_field(name="Cash", value=dinheiro, inline=True)
        # embed.add_field(name="sapphire", value=safira[1], inline=True)
        # embed.add_field(name="Box", value=caixa, inline=True)
        #await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Backpack(client))