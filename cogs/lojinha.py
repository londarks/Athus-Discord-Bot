import discord
from discord.ext import commands
import asyncio
import sqlite3




class Lojinha(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()


    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def shop(self, ctx):
        # começo
        #with open('users.json', 'r') as f:
        #    users = json.load(f)
        #dinheiro = users[f'{ctx.author.id}']['Cash']
        first_run = True
        while True:
            if first_run:
                icon = "https://i.imgur.com/OSpJJ9Q.png"
                embed = discord.Embed(color=0x19212d)
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Shop")
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="BackGround", value="🌆", inline=True)
                embed.add_field(name="badges", value="🔵", inline=True)
                first_run = False
                msg = await ctx.send(embed=embed)

            reactmoji = []
            reactmoji.extend(['🌆'])
            reactmoji.append('🔵')
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
                self.cursor.execute('SELECT theme_name, price, Description From themes')
                background=self.cursor.fetchall()
                icon = "https://i.imgur.com/OSpJJ9Q.png"
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/OSpJJ9Q.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Shop - BackGround")
                embed.set_footer(text="Athus V1.0")
                for i in range(len(background)):
                    embed.add_field(name="BackGround", value="{}\nPrice:{}\n{}".format(background[i][0],background[i][1],background[i][2]), inline=True)
                embed.add_field(name="Dica", value="Para testa Algum background digite:$teste<numero do tema>\n Para comprar um background digite: $buybg theme_<numero do tema>", inline=False)
                await msg.clear_reactions()
                await msg.edit(embed=embed)


            elif '🔵' in str(res.emoji):
                self.cursor.execute('SELECT badges_name, price, description From badges')
                badges=self.cursor.fetchall()
                icon = "https://i.imgur.com/OSpJJ9Q.png"
                embed = discord.Embed(color=0x19212d)
                icon = "https://i.imgur.com/OSpJJ9Q.png"
                embed = discord.Embed(color=0x1ccc09)
                embed.set_thumbnail(url=icon)
                embed.set_author(name="Shop - Badges")
                embed.set_footer(text="Athus V1.0")
                for i in range(len(badges)):
                    embed.add_field(name="Badges", value="{}\nPrice:{}\n{}".format(badges[i][0],badges[i][1],badges[i][2]), inline=True)
                #embed.add_field(name="Dica", value="Para testa Algum background digite:$teste<numero do tema>\n Para comprar um background digite: $buybg theme_<numero do tema>", inline=False)
                await msg.clear_reactions()
                await msg.edit(embed=embed)             

            elif '❌' in str(res.emoji):
                await ctx.message.delete()
                return await msg.delete()
        self.client.counter += 1
 
def setup(client):
    client.add_cog(Lojinha(client))