import discord
from discord.ext import commands
import asyncio
from io import BytesIO
import os, re
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps
import sqlite3




class Status(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()
    @commands.Cog.listener()
    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            pass


    @commands.cooldown(1,86400,commands.BucketType.user)
    @commands.command()
    async def Rep(self, ctx,*, member: discord.Member=None):
        #connection = sqlite3.connect('users.db')
        #cursor = connection.cursor()
        if not member:
            member = ctx.author
            await ctx.send("Usuario Invalido")
        if member.id == ctx.author.id:
            await ctx.send("Bocó...Tenta denovo")
        else:
            resp = 1
            self.cursor.execute('SELECT reputation From usuarios WHERE discord_id="%s"'%(member.id))
            reputation=self.cursor.fetchone()
            soma_ = reputation[0] + resp
            await ctx.send("Você deu 1 resp para <@!{}>, Volte Daqui 24H 59M".format(member.id))
            self.cursor.execute("""
            UPDATE usuarios
            SET reputation = ?
            WHERE discord_id = ?
            """, (soma_,member.id))
            self.connection.commit()
        self.client.counter += 1


    @commands.cooldown(1,86400,commands.BucketType.user)
    @commands.command()
    async def daily(self, ctx):
        list_money = [1000,10000,100000,1000000]
        switcher = {
           1000: "1k",
           10000: "10k",
           100000: "100k",
           1000000: "1000k"
        }
        #dia = switcher.get(dia_semana)
        daily = 300
        check = False
        self.cursor.execute('SELECT cash From usuarios WHERE discord_id="%s"'%(ctx.author.id))
        cash_db=self.cursor.fetchone()
        soma_ = cash_db[0] + daily
        await ctx.send("Você recebeu {} 💵, Volte Daqui 24H 59M".format(daily))
        self.cursor.execute("""
        UPDATE usuarios
        SET cash = ?
        WHERE discord_id = ?
        """, (soma_,ctx.author.id))
        self.connection.commit()
        #badges de dinheiro
        for i in range(len(list_money)):
            if soma_ > list_money[i]:
                deposit = switcher.get(list_money[i])
                """abr eum conexão com banco de dados roda  todos os nome das badges pertecente ao id
                que usou o comando, depois gira em uma lista comparando os nomes para não duplicar a recompença
                caso ja tenha ele retorna  check = False e não adiciona a recompença"""
                self.cursor.execute('SELECT nome_item From inventario WHERE id_usuario="%s" AND tipo_item="badges"'% (ctx.author.id))
                comquistas = self.cursor.fetchall()
                for j in range(len(comquistas)):
                    if comquistas[j][0] == deposit:
                        check = False
                        break
                    else:
                        check = True
                if check == True:
                    item_id = 1
                    nome_item = deposit
                    tipo_item = 'badges'
                    self.cursor.execute("INSERT INTO inventario (id_usuario, item_id,nome_item,tipo_item) VALUES (?,?,?,?)", (ctx.author.id,item_id,nome_item,tipo_item))
                    self.connection.commit()
                    await ctx.send("<@!{}>Você recebeu uma badges por acumular: {}".format(ctx.author.id,deposit))
        self.client.counter += 1

    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def profile(self, ctx,*, member: discord.Member=None):
        try:
            if not member:
                member = ctx.author
            self.cursor.execute('SELECT level,experience,cash,Reputation,badges_1,badges_2,badges_3,badges_4,badges_5,badges_6,background From usuarios WHERE discord_id="%s"'%(member.id))
            info_player=self.cursor.fetchall()
            if info_player is None:
                return
            self.cursor.execute('SELECT * From rank ORDER BY Level DESC')
            rank_player=self.cursor.fetchall()
            rank_set = 0
            for i in range(len(rank_player)):
                if member.id == rank_player[i][0]:
                    i += 1 
                    rank_set = i
            LVL = info_player[0][0]
            XP = info_player[0][1]
            Cash = info_player[0][2]
            Reputation = info_player[0][3]
            badges_import_1 = info_player[0][4]
            badges_import_2 = info_player[0][5]
            badges_import_3 = info_player[0][6]
            badges_import_4 = info_player[0][7]
            badges_import_5 = info_player[0][8]
            badges_import_6 = info_player[0][9]
            Background = info_player[0][10]

            url =requests.get(member.avatar_url)
            avatar = Image.open(BytesIO(url.content))
            avatar = avatar.resize((160, 160));
            bigsize = (avatar.size[0] * 3,  avatar.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize(avatar.size, Image.ANTIALIAS)
            avatar.putalpha(mask)
            output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)
            back_ground = Image.open(Background)
            output.save('img/avatar.png')
            fundo = Image.open('img/profile.png')
            nome_fonte = ImageFont.truetype('fonts/uni-sans.heavy-caps.otf',35)
            lvl_resp = ImageFont.truetype('fonts/uni-sans.heavy-caps.otf',50)
            cash_rank = ImageFont.truetype('fonts/uni-sans.heavy-caps.otf',30)

            badges_1 = Image.open(badges_import_1)
            badges_2 = Image.open(badges_import_2)
            badges_3 = Image.open(badges_import_3)
            badges_4 = Image.open(badges_import_4)
            badges_5 = Image.open(badges_import_5)
            badges_6 = Image.open(badges_import_6)
            

            if int(LVL) >= 10:
                x_lvl = 521
            else:
                x_lvl = 529
            if int(Reputation) >= 10:
                x_Reputation = 521
            else:
                x_Reputation = 529

            back_ground.paste(fundo, (0, 0), fundo)

            nome = ImageDraw.Draw(back_ground)
            nome.text(xy=(210,230), text="{}".format(member.name), fill=(255, 255, 255), font=nome_fonte)

            Level = ImageDraw.Draw(back_ground)
            Level.text(xy=(x_lvl,47), text="{}".format(LVL), fill=(13, 13, 13), font=lvl_resp)

            Resp = ImageDraw.Draw(back_ground)
            Resp.text(xy=(x_Reputation,150), text="{}".format(Reputation), fill=(13, 13, 13), font=lvl_resp)

            Cash_money = ImageDraw.Draw(back_ground)
            Cash_money.text(xy=(94,315), text="${}".format(Cash), fill=(13, 13, 13), font=cash_rank)

            Rank = ImageDraw.Draw(back_ground)
            Rank.text(xy=(94,380), text="#{}".format(rank_set), fill=(13, 13, 13), font=cash_rank)

            back_ground.paste(avatar, (33, 108), avatar)

            back_ground.paste(badges_1, (360, 283), badges_1)

            back_ground.paste(badges_2, (430, 283), badges_2)

            back_ground.paste(badges_3, (501, 283), badges_3)

            back_ground.paste(badges_4, (360, 356), badges_4)

            back_ground.paste(badges_5, (432, 356), badges_5)

            back_ground.paste(badges_6, (503, 356), badges_6)

            back_ground.save('img/status.png')
            info_png = discord.File('img/status.png')
            await ctx.send(file=info_png)
            self.client.counter += 1

        except Exception as e:
            print(e)
            self.client.counter += 1

    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def setbds(self, ctx):
        first_run = True
        badges_name = ctx.message.content[8:]
        Observer = False
        #with open('users.json', 'r') as f:
        #    users = json.load(f)
        self.cursor.execute('SELECT nome_item From inventario WHERE id_usuario="%s"'%(ctx.author.id))
        bp = self.cursor.fetchall()
        for i in range(len(bp)):
            #print(bp[i][0])
            if bp[i][0] == badges_name:
                Observer = True
        if badges_name == 'remove':
            Observer= True
        if Observer == False:
            await ctx.send("Você não tem esse Item")

        while Observer:
            if first_run:
                embed = discord.Embed(color=0x19212d)
                embed=discord.Embed(title="badges!",description="Clique no numero correspondente ao numero do perfil",color=0x4664ee)
                first_run = False
                msg = await ctx.send(embed=embed)

            reactmoji = []
            reactmoji.extend(['1️⃣'])
            reactmoji.append('2️⃣')
            reactmoji.append('3️⃣')
            reactmoji.append('4️⃣')
            reactmoji.append('5️⃣')
            reactmoji.append('6️⃣')
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
            elif '1️⃣' in str(res.emoji):
                
                badges= 'img/badges/{}_badges.png'.format(badges_name)
                self.cursor.execute("""
                UPDATE usuarios
                SET badges_1 = ?
                WHERE discord_id = ?
                """, (badges,ctx.author.id))
                self.connection.commit()
                await ctx.message.delete()
                return await msg.delete()

            elif '2️⃣' in str(res.emoji):
                
                badges= 'img/badges/{}_badges.png'.format(badges_name)
                self.cursor.execute("""
                UPDATE usuarios
                SET badges_2 = ?
                WHERE discord_id = ?
                """, (badges,ctx.author.id))
                self.connection.commit()
                await ctx.message.delete()
                return await msg.delete()

            elif '3️⃣' in str(res.emoji):

                
                badges= 'img/badges/{}_badges.png'.format(badges_name)
                self.cursor.execute("""
                UPDATE usuarios
                SET badges_3 = ?
                WHERE discord_id = ?
                """, (badges,ctx.author.id))
                self.connection.commit()
                await ctx.message.delete()
                return await msg.delete()

            elif '4️⃣' in str(res.emoji):

                
                badges= 'img/badges/{}_badges.png'.format(badges_name)
                self.cursor.execute("""
                UPDATE usuarios
                SET badges_4 = ?
                WHERE discord_id = ?
                """, (badges,ctx.author.id))
                self.connection.commit()
                await ctx.message.delete()
                return await msg.delete()

            elif '5️⃣' in str(res.emoji):

                
                badges= 'img/badges/{}_badges.png'.format(badges_name)
                self.cursor.execute("""
                UPDATE usuarios
                SET badges_5 = ?
                WHERE discord_id = ?
                """, (badges,ctx.author.id))
                self.connection.commit()
                await ctx.message.delete()
                return await msg.delete()

            elif '6️⃣' in str(res.emoji):

                
                badges= 'img/badges/{}_badges.png'.format(badges_name)
                self.cursor.execute("""
                UPDATE usuarios
                SET badges_6 = ?
                WHERE discord_id = ?
                """, (badges,ctx.author.id))
                self.connection.commit()
                await ctx.message.delete()
                return await msg.delete()


            elif '❌' in str(res.emoji):
                await ctx.message.delete()
                return await msg.delete()
        self.client.counter += 1


    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def setbg(self, ctx):
        background = ctx.message.content[7:]
        self.cursor.execute('SELECT nome_item From inventario WHERE id_usuario="%s"'%(ctx.author.id))
        bp = self.cursor.fetchall()
        checagem = False
        for i in range(len(bp)):
            if bp[i][0] == background:
                set_bg= 'img/background/{}_backgroun.png'.format(background)
                self.cursor.execute("""
                UPDATE usuarios
                SET background = ?
                WHERE discord_id = ?
                """, (set_bg,ctx.author.id))
                self.connection.commit()
                await ctx.send("Background Atualizado")
                checagem = True
        if checagem == False:
            await ctx.send("Você não tem esse background")
        self.client.counter += 1
            
def setup(client):
    client.add_cog(Status(client))