import discord
from discord.ext import commands
import asyncio
from googletrans import Translator




class Translation(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def trans(self, ctx):
        """translation"""
        first_run = True
        translation = ctx.message.content[7:]
        while True:
            if first_run:
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/6zMLSah.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Traduzir")
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="Texto", value=translation, inline=True)
                first_run = False
                msg = await ctx.send(embed=embed)

            reactmoji = []
            reactmoji.extend(['🇺🇸'])
            reactmoji.append('🇧🇷')
            reactmoji.append('🇻🇳')
            reactmoji.append('🇯🇵')
            reactmoji.append('🇦🇲')
            reactmoji.append('🇿🇦')
            reactmoji.append('🇦🇱')
            reactmoji.append('🇦🇴')
            #exit
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
            elif '🇺🇸' in str(res.emoji):
                country = 'en'
                translator = Translator()
                traduzido=translator.translate(translation, dest=country)
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/6zMLSah.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Traduzido")
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="Texto", value=traduzido.text, inline=True)
                await msg.clear_reactions()
                await msg.edit(embed=embed)
                
            elif '🇧🇷' in str(res.emoji):
                country = 'pt'
                translator = Translator()
                traduzido=translator.translate(translation, dest=country)
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/6zMLSah.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Traduzido")
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="Texto", value=traduzido.text, inline=True)
                await msg.clear_reactions()
                await msg.edit(embed=embed)
             

            elif '🇻🇳' in str(res.emoji):
                country = 'zh-tw'
                translator = Translator()
                traduzido=translator.translate(translation, dest=country)
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/6zMLSah.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Traduzido")
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="Texto", value=traduzido.text, inline=True)
                await msg.clear_reactions()
                await msg.edit(embed=embed)  

            elif '🇯🇵' in str(res.emoji):
                country = 'ja'
                translator = Translator()
                traduzido=translator.translate(translation, dest=country)
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/6zMLSah.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Traduzido")
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="Texto", value=traduzido.text, inline=True)
                await msg.clear_reactions()
                await msg.edit(embed=embed)


            elif '🇦🇲' in str(res.emoji):
                country = 'hy'
                translator = Translator()
                traduzido=translator.translate(translation, dest=country)
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/6zMLSah.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Traduzido")
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="Texto", value=traduzido.text, inline=True)
                await msg.clear_reactions()
                await msg.edit(embed=embed)


            elif '🇿🇦' in str(res.emoji):
                country = 'af'
                translator = Translator()
                traduzido=translator.translate(translation, dest=country)
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/6zMLSah.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Traduzido")
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="Texto", value=traduzido.text, inline=True)
                await msg.clear_reactions()
                await msg.edit(embed=embed)


            elif '🇦🇱' in str(res.emoji):
                country = 'sq'
                translator = Translator()
                traduzido=translator.translate(translation, dest=country)
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/6zMLSah.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Traduzido")
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="Texto", value=traduzido.text, inline=True)
                await msg.clear_reactions()
                await msg.edit(embed=embed)


            elif '🇦🇴' in str(res.emoji):
                country = 'am'
                translator = Translator()
                traduzido=translator.translate(translation, dest=country)
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/6zMLSah.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Traduzido")
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="Texto", value=traduzido.text, inline=True)
                await msg.clear_reactions()
                await msg.edit(embed=embed)


            elif '❌' in str(res.emoji):
                await ctx.message.delete()
                return await msg.delete()
        self.client.counter += 1

def setup(client):
    client.add_cog(Translation(client))