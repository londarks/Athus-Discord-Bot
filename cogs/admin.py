import discord
from discord.ext import commands
import asyncio
import psutil
import datetime
import sqlite3

start_time = datetime.datetime.utcnow() # Timestamp of when it came online

class Admin(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def add_channel(self, ctx):
        """set channel bot sau"""
        try:
            channel_id = ctx.message.channel.id
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()
            cursor.execute('SELECT Id_channel From Channel_list')
            variables = cursor.fetchall()
            n = 0
            for i in range(len(variables)):
                if variables[n][0] == channel_id:
                    await ctx.send("Esses canal ja Foi adicionado")
                    return
                n += 1
            cursor.execute("INSERT INTO Channel_list (Id_channel) VALUES (?)", (channel_id,))
            connection.commit()
            await ctx.send("Canal adicionado")
            self.client.counter += 1
        except Exception as e:
            print(e)

    @commands.command()
    async def admin_gif(self, ctx):
        """Joins a voice channel"""
        admin = ctx.message.content[11:]
        if ctx.author.id == 228268072706899968:
        	if admin == '1':
        		info_png = discord.File('img/gif/gif_1.gif')
        		await ctx.send(file=info_png)
        	elif admin == '2':
        		info_png = discord.File('img/gif/gif_2.gif')
        		await ctx.send(file=info_png)
        self.client.counter += 1


    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def status(self, ctx):
        psutil.cpu_percent()
        # gives an object with many fields
        ram = psutil.virtual_memory()
        # you can convert that object to a dictionary 
        cpu = dict(psutil.virtual_memory()._asdict())
        ram = psutil.virtual_memory()

        now = datetime.datetime.utcnow() # Timestamp of when uptime function is run
        delta = now - start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if days:
            time_format = "{d}days,{h}hours,{m}minutes,{s}seconds."
        else:
            time_format = "{d}days,{h}hours,{m}minutes,{s}seconds."
        uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
        #await client.say("{} has been up for {}".format(client.user.name, uptime_stamp))

        icon_bot = "https://i.imgur.com/4Jtk29h.jpg"
        embed = discord.Embed(color=0x1ccc09)
        embed.set_thumbnail(url=icon_bot)
        embed.set_author(name="Information",icon_url=icon_bot)
        embed.set_footer(text="Athus V1.0")
        embed.add_field(name="Up Time", value="```fix\n"
                                              "{}"
                                              "```".format(uptime_stamp), inline=True)
        embed.add_field(name="Users", value="```css\n"
                                            "[{}]\n"
                                            "```".format(len(self.client.users)), inline=True)
        embed.add_field(name="Servers", value="```yaml\n"
                                              " {}"
                                              "```".format(len(self.client.guilds)), inline=True)
        embed.add_field(name="Commands Usage", value="```yaml\n"
                                              "{}"
                                              "```".format(self.client.counter), inline=True)
        embed.add_field(name="CPU Usage", value="```yaml\n"
                                              "{}"
                                              "```".format(cpu['used']), inline=True)
        embed.add_field(name="RAM Usage", value="```fix\n"
                                                "{}%"
                                                "```".format(ram[2]), inline=True)
        await ctx.send(embed=embed)
        self.client.counter += 1

def setup(client):
    client.add_cog(Admin(client))