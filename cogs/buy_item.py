import discord
from discord.ext import commands
import asyncio
import sqlite3




class Buy(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()

    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def buybg (self,ctx):
        """Compra background na loja"""
        theme = ctx.message.content[7:]
        self.cursor.execute('SELECT cash From usuarios  WHERE discord_id="%s"'% (ctx.author.id))
        remove = self.cursor.fetchall()
        self.cursor.execute('SELECT price From themes WHERE theme_name="%s"' % (theme))
        price = self.cursor.fetchall()
        if remove[0][0] < price[0][0]:
            await ctx.send("Você Não tem saldo suficiente")
            return
        soma_ = remove[0][0] - price[0][0]
        self.cursor.execute("""
        UPDATE usuarios
        SET cash = ?
        WHERE discord_id = ?
        """, (soma_,ctx.author.id))
        self.connection.commit()
        item_id = 2
        nome_item = theme
        tipo_item = 'theme'
        self.cursor.execute("INSERT INTO inventario (id_usuario, item_id,nome_item,tipo_item) VALUES (?,?,?,?)", (ctx.author.id,item_id,nome_item,tipo_item))
        self.connection.commit()
        await ctx.send("Background Comprado")
        self.client.counter += 1


    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def buybds (self,ctx):
        """Compra background na loja"""
        badges = ctx.message.content[8:]
        self.cursor.execute('SELECT cash From usuarios  WHERE discord_id="%s"'% (ctx.author.id))
        remove = self.cursor.fetchall()
        self.cursor.execute('SELECT price From badges WHERE badges_name="%s"' % (badges))
        price = self.cursor.fetchall()
        if remove[0][0] < price[0][0]:
            await ctx.send("Você Não tem saldo suficiente")
            return
        soma_ = remove[0][0] - price[0][0]
        self.cursor.execute("""
        UPDATE usuarios
        SET cash = ?
        WHERE discord_id = ?
        """, (soma_,ctx.author.id))
        self.connection.commit()
        item_id = 1
        nome_item = badges
        tipo_item = 'badges'
        self.cursor.execute("INSERT INTO inventario (id_usuario, item_id,nome_item,tipo_item) VALUES (?,?,?,?)", (ctx.author.id,item_id,nome_item,tipo_item))
        self.connection.commit()
        await ctx.send("Badges Comprado")
        self.client.counter += 1

def setup(client):
    client.add_cog(Buy(client))