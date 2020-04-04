import discord
from discord.ext import commands
import asyncio
import sqlite3



class Rank(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()

    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def rank(self, ctx):
        """Joins a voice channel"""
        embed = discord.Embed(color=0x1ccc09)
        embed.set_author(name="Rank")
        embed.set_footer(text="Athus V1.0")
        self.cursor.execute('SELECT * From rank ORDER BY Level DESC')
        rank_player=self.cursor.fetchall()
        rank_set = 0
        j = 0
        for i in range(len(rank_player)): 
            j += 1 
            rank_set = j
            embed.add_field(name="Top {}".format(j), value="<@!{}>".format(rank_player[i][0]), inline=False)
        await ctx.send(embed=embed)
        self.client.counter += 1
 

def setup(client):
    client.add_cog(Rank(client))