import discord
from discord.ext import commands
import asyncio
import requests
from bs4 import BeautifulSoup




class LOL(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def lol(self, ctx):
        reply_menssagen = ctx.message.content[5:]

        conect = requests.get('https://br.op.gg/summoner/userName={}'.format(reply_menssagen))
        soup = BeautifulSoup(conect.text, "lxml")
        
        Summoner_Icon=soup.find_all('div',{'class':'ProfileIcon'})[0].find('img')

        
        #soloQ Rank
        Summoner_TierQ=soup.find_all('div',{'class':'TierRankInfo'})[0].find_all('div')[1].text#.text[4:]
        try:
            Summoner_pdl_TierQ=soup.find_all('div',{'class':'TierInfo'})[0].find_all('span')[0].text[5:]
            wins=soup.find_all('div',{'class':'TierInfo'})[0].find_all('span')[1].text[1:]
            loser=soup.find_all('div',{'class':'TierInfo'})[0].find_all('span')[1].text[1:]
            Summoner_graf_TierQ=soup.find_all('div',{'class':'TierInfo'})[0].find_all('span')[1].text[1:]
        except IndexError as e:
            Summoner_pdl_TierQ="........"
            Summoner_graf_TierQ="......."
            wins="................."
            loser="................."
        #5x5
        Summoner_Tier=soup.find_all('div',{'class':'sub-tier__info'})[0].find_all('div')[1].text[19:]
        try:
            Summoner_pdl_Tier=soup.find_all('div',{'class':'sub-tier__league-point'})[0].text#[5:]
            Summoner_winrete=soup.find_all('div',{'class':'sub-tier__gray-text'})[0].text[8:]
            #Summoner_winrete[3:]
        except IndexError as e:
            Summoner_pdl_Tier="..."
            Summoner_winrete="......"

        try:
            embed = discord.Embed(color=0x1ccc09)
            embed.set_thumbnail(url="https:{}".format(Summoner_Icon['src']))
            embed.set_author(name=reply_menssagen)
            embed.set_footer(text="Athus V1.0")
            embed.add_field(name="Tier SoloQ", value=Summoner_TierQ, inline=True)
            embed.add_field(name="Tier SoloQ Pdls", value="{}LP/{} {}".format(Summoner_pdl_TierQ[:1],wins[:3],loser[4:7]), inline=True)
            embed.add_field(name="Win Ratio SoloQ", value=Summoner_graf_TierQ[9:], inline=True)
            embed.add_field(name="Tier Flex", value=Summoner_Tier, inline=True)
            embed.add_field(name="Tier Flex Pdls", value=Summoner_pdl_Tier, inline=True)
            embed.add_field(name="Win Ratio Flex", value=Summoner_winrete[3:], inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("Um erro Aconteceu.!...Nome do invocador errado ou server Offline.!! ")
        self.client.counter += 1
def setup(client):
    client.add_cog(LOL(client))