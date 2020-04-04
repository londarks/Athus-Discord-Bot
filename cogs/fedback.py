import discord
from discord.ext import commands
import asyncio




class Feedback(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def feedback(self, ctx):
        """Joins a voice channel"""
        try:
            feedback = ctx.message.content[10:]
            user = 228268072706899968
            channel = self.client.get_user(user)

            icon_bot = "https://i.imgur.com/4Jtk29h.jpg"
            fed = "https://i.imgur.com/Lmfk9Js.png"
            embed = discord.Embed(color=0x1ccc09)
            embed.set_thumbnail(url=fed)
            embed.set_author(name="FeedBack",icon_url=icon_bot)
            embed.set_footer(text="Athus V1.0")
            embed.add_field(name="FeedBack Send", value="```yaml\n"
                                                  "{}"
                                                  "```".format(feedback), inline=True)
            embed.add_field(name="User", value="```css\n"
                                                "[{}]\n"
                                                "```".format(ctx.author.name), inline=True)
            embed.add_field(name="Server", value="```yaml\n"
                                                "{}\n"
                                                "```".format(ctx.guild.name), inline=False)
            embed.add_field(name="User Id", value="```fix\n"
                                                "{}\n"
                                                "```".format(ctx.author.id), inline=False)

            await channel.send(embed=embed)
            await ctx.channel.purge(limit=1)
            await ctx.send("feedback enviado...")
            self.client.counter += 1
        except Exception as e:
            print(e)



    @commands.guild_only()
    @commands.command()
    async def say (self, ctx):
        reply_menssagen = ctx.message.content[5:]
        await ctx.channel.purge(limit=1)
        #await client.purge(limit=1)
        await ctx.send(reply_menssagen)

def setup(client):
    client.add_cog(Feedback(client))