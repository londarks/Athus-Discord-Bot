import sqlite3
import discord
from discord.ext import commands
import asyncio
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import time


class Levelling(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        connection = sqlite3.connect('users.db')
        result = connection.cursor()
        if message.author.bot == True:
            return
        author = message.author.id 
        result.execute('SELECT discord_id From usuarios WHERE discord_id="%s"' % (author))
        check_db=result.fetchone()
        if check_db is None:
            await self.update_data(author)
        else:
            result.execute('SELECT experience From usuarios WHERE discord_id="%s"' % (author))
            experience_user=result.fetchone()
            soma_ =  (experience_user[0] + 5)
            result.execute("""
            UPDATE usuarios
            SET experience = ?
            WHERE discord_id = ?
            """, (soma_,author))
            connection.commit()
        await self.level_up(author, message.channel.id, message.author.id,message.author.avatar_url)



    async def update_data(self,user):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        _id = user
        experience = 0
        level = 1
        Cash= 0
        sapphire = 0
        Reputation = 0
        badges_1 = 'img/badges/novice_badges.png'
        badges_2 = 'img/badges/None_badges.png'
        badges_3 = 'img/badges/None_badges.png'
        badges_4 = 'img/badges/None_badges.png'
        badges_5 = 'img/badges/None_badges.png'
        badges_6 = 'img/badges/None_badges.png'
        Background = 'img/background/theme_0_backgroun.png'
        #fazendo registro de usuarios
        cursor.execute("INSERT INTO usuarios (discord_id,experience,level,cash,sapphire,reputation,badges_1,badges_2,badges_3,badges_4,badges_5,badges_6,background) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (_id,experience,level,Cash,sapphire,Reputation,badges_1,badges_2,badges_3,badges_4,badges_5,badges_6,Background))
        connection.commit()
        item_id = 1
        nome_item = 'novice'
        tipo_item = 'badges'
        cursor.execute("INSERT INTO inventario (id_usuario, item_id,nome_item,tipo_item) VALUES (?,?,?,?)", (user,item_id,nome_item,tipo_item))
        connection.commit()
        cursor.execute("INSERT INTO rank (user_id,level) VALUES (?,?)", (user,level))
        connection.commit()
        item_id = 2
        nome_item = 'theme_0'
        tipo_item = 'theme'
        cursor.execute("INSERT INTO inventario (id_usuario, item_id,nome_item,tipo_item) VALUES (?,?,?,?)", (user,item_id,nome_item,tipo_item))
        connection.commit()



    async def level_up(self,user,canal, person,img):
        list_lvl = [10,20,30,40,50,60,70,80,90,100]
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT experience,level From usuarios WHERE discord_id="%s"' % (user))
        add_lvl = cursor.fetchone()
        info_player = []
        for add in add_lvl:
            info_player.append(add)
        experience = info_player[0]
        lvl_start = info_player[1]
        lvl_end = int(experience ** (1 / 4))
        if lvl_start < lvl_end:
            cursor.execute("""UPDATE usuarios SET level = ? WHERE discord_id = ?""",(lvl_end,user))
            connection.commit()
            channel = self.client.get_channel(canal)
            #await self.level_card(img,lvl_end,canal)
            await channel.send(f'<@!{person}> Você subio de Level.!!')
            cursor.execute("""
            UPDATE rank
            SET level = ?
            WHERE user_id = ?
            """, (lvl_end,person))
            connection.commit()
            #badges rank
            #gera um swit para passar os numeros para o nome da badges
            # switcher = {
            # 10:"rank10",
            # 9: "rank9",
            # 8: "rank8",
            # 7: "rank7",
            # 6: "rank6",
            # 5: "rank5",
            # 4: "rank4",
            # 3: "rank3",
            # 2: "rank2",
            # 1: "rank1"
            # }
            # g = 1
            # #verifica se o usuario faz parte do top 10
            # cursor.execute('SELECT * From rank ORDER BY level AND level DESC LIMIT 10')
            # rank=cursor.fetchall()
            # print(rank)
            # for r in range(len(rank)):
            # 	if user == rank[r][0]:
            #     	rank_switcher = switcher.get(g)
            #     	print(rank_switcher)
            #     	print("entrei")
            #     	#fazendo check-up na backpack
            #     	cursor.execute('SELECT nome_item From inventario WHERE id_usuario="%s" AND tipo_item="badges"'%(user))
            #     	comquistas = cursor.fetchall()
            #     	print(comquistas)
            #     	print(len(comquistas))
            #     	for l in range(len(comquistas)):
            #     		print(comquistas[l][0])
            #     		if comquistas[l][0] == rank_switcher:
            #     			print("entro")
            #     			break
            #     		else:
            #     			item_id = 1
            #     			nome_item = 'rank{}'.format(g)
            #     			tipo_item = 'badges'
            #     			cursor.execute("INSERT INTO inventario (id_usuario, item_id,nome_item,tipo_item) VALUES (?,?,?,?)", (user,item_id,nome_item,tipo_item))
            #     			connection.commit()
            #     			await channel.send("<@!{}>Você recebeu uma badges por estar: rank{}".format(user,g))
            #     			return
            #     	g += 1

            """Adiciona Badges por leveles ele faz umas rapida pesquisa
            na sua bacpack e diz se você tem o item ou não caso tenha ele quebra o codigo com 
            um return para nao adicionar mais nada e essa função so será chamada outra vez caso
            você pegue um level  ==  da tabela list_lvl """
            for i in range(len(list_lvl)):
                if lvl_end == list_lvl[i]:
                    nome_item = 'lvl{}'.format(lvl_end)
                    cursor.execute('SELECT nome_item From inventario WHERE id_usuario="%s" AND tipo_item="badges"'% (user))
                    comquistas = cursor.fetchall()
                    for j in range(len(comquistas)):
                        if comquistas[j][0] == nome_item:
                        	return
                    await channel.send("<@!{}> Você ganhou por passar para o nivel{}".format(person,lvl_end))
                    item_id = 1
                    tipo_item = 'badges'
                    cursor.execute("INSERT INTO inventario (id_usuario, item_id,nome_item,tipo_item) VALUES (?,?,?,?)", (user,item_id,nome_item,tipo_item))
                    connection.commit()
            """comando para adicionar badges no lvl30 não precisa de nenhum tipo de checagem pois você
            so upa level 30 uma vez e esse codigo so será execultado somente uma vez"""
            if lvl_end == 30:
                await channel.send("<@!{}> Você ganhou uma badges por ser um veterano".format(person))
                item_id = 1
                nome_item = 'veterano'
                tipo_item = 'badges'
                cursor.execute("INSERT INTO inventario (id_usuario, item_id,nome_item,tipo_item) VALUES (?,?,?,?)", (user,item_id,nome_item,tipo_item))
                connection.commit()

    # async def level_card(self,img,lvl,canal):
    #     url =requests.get(img)
    #     avatar = Image.open(BytesIO(url.content))
    #     avatar = avatar.resize((130, 130));
    #     bigsize = (avatar.size[0] * 3,  avatar.size[1] * 3)
    #     mask = Image.new('L', bigsize, 0)
    #     draw = ImageDraw.Draw(mask)
    #     draw.ellipse((0, 0) + bigsize, fill=255)
    #     mask = mask.resize(avatar.size, Image.ANTIALIAS)
    #     avatar.putalpha(mask)
    #     output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    #     output.putalpha(mask)
    #     output.save('img/levelup/avatar.png')
    #     #back_ground = Image.open('img/levelup/levelupcard.png')

    #     def create_gif(seta_1,seta_2,seta_3,seta_4,seta_5,seta_6,lvl):
    #         back_ground = Image.open('img/levelup/levelupcard.png')
    #         setinha = Image.open("img/levelup/setinha.png")
    #         nome_fonte = ImageFont.truetype('fonts/uni-sans.heavy-caps.otf',35)
    #         avatar = Image.open ('img/levelup/avatar.png')
    #         level = ImageDraw.Draw(back_ground)

    #         level.text(xy=(437,46), text="{}".format(lvl), fill=(13, 13, 13), font=nome_fonte)
    #         back_ground.paste(avatar, (22, 24), avatar)
    #         back_ground.paste(setinha, (seta_1, 129), setinha)
    #         back_ground.paste(setinha, (seta_2, 129), setinha)
    #         back_ground.paste(setinha, (seta_3, 129), setinha)
    #         back_ground.paste(setinha, (seta_4, 129), setinha)
    #         back_ground.paste(setinha, (seta_5, 129), setinha)
    #         back_ground.paste(setinha, (seta_6, 129), setinha)
        
    #         return back_ground


    #     frames = []
    #     #x, y = 246, 43
    #     seta_1 = 149
    #     seta_2 = 169
    #     seta_3 = 189
    #     seta_4 = 209
    #     seta_5 = 229
    #     seta_6 = 249
    #     for i in range(10):
    #         seta_1 += 20
    #         seta_2 += 20
    #         seta_3 += 20
    #         seta_4 += 20
    #         seta_5 += 20
    #         seta_6 += 20
    #         new_frame = create_gif(seta_1,seta_2,seta_3,seta_4,seta_5,seta_6,lvl)
    #         frames.append(new_frame)

    #     # Save into a GIF file that loops forever
    #     frames[0].save('img/levelup/levelupcard_1.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0, transparency=0)
    #     info_png = discord.File('img/levelup/levelupcard_1.gif')
    #     channel = self.client.get_channel(canal)
    #     await channel.send(file=info_png)

def setup(client):
    client.add_cog(Levelling(client))