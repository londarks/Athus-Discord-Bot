import discord
from discord.ext import commands
import asyncio
import time
import aiohttp
import requests
from bs4 import BeautifulSoup
from jikanpy import Jikan





class Animes_Mangas(commands.Cog):
    def __init__(self,client):
        self.client = client
    def anilist_query(self):
        anilist_query = '''
        query ($page: Int, $perPage: Int, $search: String) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                    hasNextPage
                    perPage
                }
                media(search: $search, type: %s) {
                    id
                    idMal
                    title {
                        romaji
                        english
                        native
                    }
                    coverImage {
                        large
                    }
                    averageScore
                    chapters
                    volumes
                    episodes
                    format
                    status
                    source
                    genres
                    description(asHtml:false)
                    startDate {
                        year
                        month
                        day
                    }
                    endDate {
                        year
                        month
                        day
                    }
                    nextAiringEpisode {
                        airingAt
                        timeUntilAiring
                        episode
                    }
                }
            }
        }
        '''
        return anilist_query
    
    
    def monthintext(self,number):
        idn = ["January", "February", "March", "April",
                "May", "June", "July", "August",
                "September", "October", "November", "December"]
        if number is None:
            return "Unknown"
        x = number - 1
        if x < 0:
            return "Unknown"
        return idn[number - 1]
    
    
    def create_time_format(self,secs):
        months = int(secs // 2592000) # 30 days format
        secs -= months * 2592000
        days = int(secs // 86400)
        secs -= days * 86400
        hours = int(secs // 3600)
        secs -= hours * 3600
        minutes = int(secs // 60)
        secs -= minutes * 60
    
        return_text = ''
        if months != 0:
            return_text += '{} months '.format(months)
    
        return return_text + '{} days {} hours {} minutes {} seconds left'.format(days, hours, minutes, secs)

    def html2markdown(self,text):
        re_list = {
            '<br>': '\n',
            '</br>': '\n',
            '<i>': '*',
            '</i>': '*',
            '<b>': '**',
            '</b>': '**',
            '\n\n': '\n'
        }
        for k, v in re_list.items():
            text = text.replace(k, v)
        return text
    
    async def fetch_anilist(self,title, method):
        variables = {
            'search': title,
            'page': 1,
            'perPage': 50
        }
        async with aiohttp.ClientSession() as sesi:
            try:
                async with sesi.post('https://graphql.anilist.co', json={'query': self.anilist_query() % method.upper(), 'variables': variables}) as r:
                    try:
                        data = await r.json()
                    except IndexError:
                        return 'ERROR: Terjadi kesalahan internal'
                    if r.status != 200:
                        if r.status == 404:
                            return "Tidak ada hasil."
                        elif r.status == 500:
                            return "ERROR: Internal Error :/"
                    try:
                        query = data['data']['Page']['media']
                    except IndexError:
                        return "Tidak ada hasil."
            except aiohttp.ClientError:
                return 'ERROR: Koneksi terputus'
    
        # Koleksi translasi dan perubahan teks
        status_tl = {
            'finished': 'Tamat',
            'releasing': 'Sedang Berlangsung',
            'not_yet_released': 'Belum Rilis',
            'cancelled': 'Batal Tayang'
        }
        format_tl = {
            "TV": "Anime",
            "TV_SHORT": "Anime Pendek",
            "MOVIE": "Film",
            "SPECIAL": "Spesial",
            "OVA": "OVA",
            "ONA": "ONA",
            "MUSIC": "MV",
            "NOVEL": "Novel",
            "MANGA": "Manga",
            "ONE_SHOT": "One-Shot",
            None: "Lainnya"
        }
        source_tl = {
            "ORIGINAL": "Original",
            "MANGA": "Manga",
            "VISUAL_NOVEL": "Visual Novel",
            "LIGHT_NOVEL": "Novel Ringan",
            "VIDEO_GAME": "Gim",
            "OTHER": "Lainnya",
            None: "Lainnya"
        }
    
        if not query:
            return "Tidak ada hasil."
    
        full_query_result = []
        for entry in query:
            start_y = entry['startDate']['year']
            end_y = entry['endDate']['year']
            if not start_y:
                start = 'Belum Rilis'
            else:
                start = '{}'.format(start_y)
                start_m = entry['startDate']['month']
                if start_m:
                    start = '{}/{}'.format(start, start_m)
                    start_d = entry['startDate']['day']
                    if start_d:
                        start = '{}/{}'.format(start, start_d)
            
            if not end_y:
                end = 'Belum Berakhir'
            else:
                end = '{}'.format(end_y)
                end_m = entry['endDate']['month']
                if end_m:
                    end = '{}/{}'.format(end, end_m)
                    end_d = entry['endDate']['day']
                    if end_d:
                        end = '{}/{}'.format(end, end_d)
    
            title = entry['title']['romaji']
            ani_id = str(entry['id'])
            try:
                mal_id = str(entry['idMal'])
            except:
                mal_id = None
    
            other_title = entry['title']['native']
            english_title = entry['title']['english']
            if english_title:
                if other_title:
                    other_title += '\n' + english_title
                else:
                    other_title = english_title
    
            score_rate = None
            score_rate_anilist = entry['averageScore']
            if score_rate:
                score_rate = '{}/10'.format(score_rate_anilist/10)
     
            description = entry['description']
            if description is not None:
                description = self.html2markdown(description)
                if len(description) > 1023:
                    description = description[:1020] + '...'
    
            genres = ', '.join(entry['genres']).lower()
            status = entry['status'].lower()
            img = entry['coverImage']['large']
            ani_link = 'https://anilist.co/{m}/{id}'.format(m=method, id=ani_id)
    
            dataset = {
                'title': title,
                'title_other': other_title,
                'start_date': start,
                'end_date': end,
                'poster_img': img,
                'synopsis': description,
                'status': status.capitalize(),
                'format': entry['format'].capitalize(),
                'source_fmt': entry['source'].capitalize(),
                'link': ani_link,
                'score': score_rate,
                'footer': "ID: {} | {}".format(ani_id, genres)
            }
    
            if method == 'manga':
                vol = entry['volumes']
                ch = entry['chapters']
                ch_vol = '{c} chapterXXC/{v} volumeXXV'.format(c=ch, v=vol).replace('None', '??')
                if ch:
                    if ch > 1:
                        ch_vol = ch_vol.replace('XXC', 's')
                ch_vol = ch_vol.replace('XXC', '')
                if vol:
                    if vol > 1:
                        ch_vol = ch_vol.replace('XXV', 's')
                ch_vol = ch_vol.replace('XXV', '')
                dataset['ch_vol'] = ch_vol
            if method == 'anime':
                dataset['episodes'] = entry["episodes"]
                if status in ['releasing', 'not_yet_released']:
                    ne_data = entry['nextAiringEpisode']
                    if ne_data:
                        airing_time = ne_data['airingAt']
                        d_airing_time = timedelta(seconds=abs(airing_time))
                        time_tuple = datetime(1,1,1) + d_airing_time
    
                        dataset['airing_date'] = '{d} {m} {y}'.format(d=time_tuple.day, m=self.monthintext(time_tuple.month), y=time.strftime('%Y'))
                        dataset['next_episode'] = ne_data['episode']
                        dataset['time_remain'] = self.create_time_format(ne_data['timeUntilAiring'])
    
            for k, v in dataset.items():
                if not v:
                    dataset[k] = 'No Data'
    
            full_query_result.append(dataset)
        return {'result': full_query_result, 'data_total': len(full_query_result)}        

    @commands.guild_only()
    @commands.command()
    #async def anime (self, ctx):
    async def manga(self, ctx):
        """Search anime information using Anilist GraphQL API."""
        title = ctx.message.content[7:]
        #print('[@] Searching manga: {}'.format(title))
        aqres = await self.fetch_anilist(title, 'manga')
        if isinstance(aqres, str):
            return await ctx.send(aqres)
    
        max_page = aqres['data_total']
        resdata = aqres['result']
        #print(resdata)
        #print('\t>> Total result: {}'.format(max_page))
    
        first_run = True
        num = 1
        while True:
            if first_run:
                #print('\t>> Showing result')
                data = resdata[num - 1]
                embed = discord.Embed(color=0x19212d)
    
                embed.set_thumbnail(url=data['poster_img'])
                embed.set_author(name="teste", url=data['link'], icon_url="https://anilist.co/img/icons/apple-touch-icon-152x152.png")
                embed.set_footer(text=data['footer'])
    
                embed.add_field(name="Other Names", value=data['title_other'], inline=True)
                embed.add_field(name="Chapter/Volume", value=data['ch_vol'], inline=True)
                embed.add_field(name="Status", value=data['status'], inline=True)
                embed.add_field(name="Scores", value=data['score'], inline=True)
                embed.add_field(name="Released", value=data['start_date'], inline=True)
                embed.add_field(name="Ended", value=data['end_date'], inline=True)
                embed.add_field(name="Format", value=data['format'], inline=True)
                embed.add_field(name="Source Material", value=data['source_fmt'], inline=True)
                embed.add_field(name="Synopsis", value=data['synopsis'], inline=False)
    
                first_run = False
                msg = await ctx.send(embed=embed)
    
            reactmoji = []
            if max_page == 1 and num == 1:
                pass
            elif num == 1:
                reactmoji.append('⏩')
            elif num == max_page:
                reactmoji.append('⏪')
            elif num > 1 and num < max_page:
                reactmoji.extend(['⏪', '⏩'])
            reactmoji.append('✅')
    
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
            elif '⏪' in str(res.emoji):
                #print('<< Going backward')
                num = num - 1
                data = resdata[num - 1]
    
                embed = discord.Embed(color=0x19212d)
    
                embed.set_thumbnail(url=data['poster_img'])
                embed.set_author(name="teste", url=data['link'], icon_url="https://anilist.co/img/icons/apple-touch-icon-152x152.png")
                embed.set_footer(text=data['footer'])
    
                embed.add_field(name="Other Names", value=data['title_other'], inline=True)
                embed.add_field(name="Chapter/Volume", value=data['ch_vol'], inline=True)
                embed.add_field(name="Status", value=data['status'], inline=True)
                embed.add_field(name="Scores", value=data['score'], inline=True)
                embed.add_field(name="Released", value=data['start_date'], inline=True)
                embed.add_field(name="Ended", value=data['end_date'], inline=True)
                embed.add_field(name="Format", value=data['format'], inline=True)
                embed.add_field(name="Source Material", value=data['source_fmt'], inline=True)
                embed.add_field(name="Synopsis", value=data['synopsis'], inline=False)
    
                await msg.clear_reactions()
                await msg.edit(embed=embed)
            elif '⏩' in str(res.emoji):
                #print('\t>> Going forward')
                num = num + 1
                data = resdata[num - 1]
    
                embed = discord.Embed(color=0x19212d)
    
                embed.set_thumbnail(url=data['poster_img'])
                embed.set_author(name="teste", url=data['link'], icon_url="https://anilist.co/img/icons/apple-touch-icon-152x152.png")
                embed.set_footer(text=data['footer'])
    
                embed.add_field(name="Other Names", value=data['title_other'], inline=True)
                embed.add_field(name="Chapter/Volume", value=data['ch_vol'], inline=True)
                embed.add_field(name="Status", value=data['status'], inline=True)
                embed.add_field(name="Scores", value=data['score'], inline=True)
                embed.add_field(name="Released", value=data['start_date'], inline=True)
                embed.add_field(name="Ended", value=data['end_date'], inline=True)
                embed.add_field(name="Format", value=data['format'], inline=True)
                embed.add_field(name="Source Material", value=data['source_fmt'], inline=True)
                embed.add_field(name="Synopsis", value=data['synopsis'], inline=False)
    
                await msg.clear_reactions()
                await msg.edit(embed=embed)
            elif '✅' in str(res.emoji):
                await ctx.message.delete()
                return await msg.delete()
        self.client.counter += 1

    @commands.guild_only()
    @commands.command()
    #async def anime (self, ctx):
    async def anime(self, ctx):
        # começo
        reply_menssagen = ctx.message.content[7:]
        #print(reply_menssagen)
        jikan = Jikan()
        anime_name = []
        episodios = []
        rank_anime = []
        synopsis_anime =[]
        start_date_anime =[]
        end_date_anime =[]
        type_anime  =[]
        image_url = []
        try:
            search_result = jikan.search('anime', '{}'.format(reply_menssagen))
            for animes in search_result['results']:
                anime_name.append([animes['title']])
                episodios.append([animes['episodes']])
                rank_anime.append([animes['score']])
                synopsis_anime.append([animes['synopsis']])
                start_date_anime.append([animes['start_date']])
                end_date_anime.append([animes['end_date']])
                type_anime.append([animes['type']])
                image_url.append([animes['image_url']])
        except (Exception,UnicodeEncodeError):
            await ctx.send("Anime not found")
        max_page = len(anime_name)
        resdata = len(anime_name)
        first_run = True
        num = 1
        contador = 0
        while True:
            if first_run:
                try:
                    # end_date_anime[contador][0][:10] is None:
                    #    end_date_anime[contador][0][:10] = "..."
                    icon = 'https://images-ext-2.discordapp.net/external/wEvP_GFZMlpWDdjkvr465GPbDL7I3vIU7YmG-o2hl6A/https/www.animestc.com/wp-content/uploads/2016/01/Logo-Tele23-50x50.png'
                    embed = discord.Embed(color=0x19212d)
                    embed.set_thumbnail(url=image_url[contador][0])
                    embed.set_author(name=anime_name[contador][0], icon_url=icon)
                    embed.set_footer(text="Athus V1.0")
                    embed.add_field(name="Tile:", value=anime_name[contador][0], inline=True)
                    embed.add_field(name="Episodes", value=episodios[contador][0], inline=True)
                    embed.add_field(name="launch", value=start_date_anime[contador][0][:10], inline=True)
                    embed.add_field(name="rank", value=rank_anime[contador][0], inline=True)
                    embed.add_field(name="Tye", value=type_anime[contador][0], inline=True)
                    embed.add_field(name="Synopsis", value=synopsis_anime[contador][0], inline=False)
                    first_run = False
                    msg = await ctx.send(embed=embed)
                except Exception as e:
                    pass
                    #print(e)

            reactmoji = []
            if max_page == 1 and num == 1:
                pass
            elif num == 1:
                reactmoji.append('⏩')
            elif num == max_page:
                reactmoji.append('⏪')
            elif num > 1 and num < max_page:
                reactmoji.extend(['⏪', '⏩'])
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
            elif '⏪' in str(res.emoji):
                #print('<< Going backward')
                num = num - 1
                contador -= 1

                if end_date_anime[contador][0] is None:
                    end_date_anime[contador][0] = "..."
                icon = 'https://images-ext-2.discordapp.net/external/wEvP_GFZMlpWDdjkvr465GPbDL7I3vIU7YmG-o2hl6A/https/www.animestc.com/wp-content/uploads/2016/01/Logo-Tele23-50x50.png'
                embed = discord.Embed(color=0x19212d)
                embed.set_thumbnail(url=image_url[contador][0])
                embed.set_author(name=anime_name[contador][0], icon_url=icon)
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="Tile:", value=anime_name[contador][0], inline=True)
                embed.add_field(name="Episodes", value=episodios[contador][0], inline=True)
                embed.add_field(name="launch", value=start_date_anime[contador][0][:10], inline=True)
                embed.add_field(name="rank", value=rank_anime[contador][0], inline=True)
                embed.add_field(name="Tye", value=type_anime[contador][0], inline=True)
                embed.add_field(name="Synopsis", value=synopsis_anime[contador][0], inline=False)
                await msg.clear_reactions()
                await msg.edit(embed=embed)



            elif '⏩' in str(res.emoji):
                #print('\t>> Going forward')
                num = num + 1
                contador += 1
                if end_date_anime[contador][0] is None:
                    end_date_anime[contador][0] = "..."
                icon = 'https://images-ext-2.discordapp.net/external/wEvP_GFZMlpWDdjkvr465GPbDL7I3vIU7YmG-o2hl6A/https/www.animestc.com/wp-content/uploads/2016/01/Logo-Tele23-50x50.png'
                embed = discord.Embed(color=0x19212d)
                embed.set_thumbnail(url=image_url[contador][0])
                embed.set_author(name=anime_name[contador][0], icon_url=icon)
                embed.set_footer(text="Athus V1.0")
                embed.add_field(name="Tile:", value=anime_name[contador][0], inline=True)
                embed.add_field(name="Episodes", value=episodios[contador][0], inline=True)
                embed.add_field(name="launch", value=start_date_anime[contador][0][:10], inline=True)
                embed.add_field(name="rank", value=rank_anime[contador][0], inline=True)
                embed.add_field(name="Tye", value=type_anime[contador][0], inline=True)
                embed.add_field(name="Synopsis", value=synopsis_anime[contador][0], inline=False)
                await msg.clear_reactions()
                await msg.edit(embed=embed)
            
            elif '❌' in str(res.emoji):
                await ctx.message.delete()
                return await msg.delete()
        self.client.counter += 1

    @commands.guild_only()
    @commands.command()
    #async def anime (self, ctx):
    async def temporada(self, ctx):
        # começo
        conect = requests.get('https://www.animestc.com')
        soup = BeautifulSoup(conect.text, "lxml")
        semanas = 7 # - Dias da semana
        anime = [] # - Array para armazenar osnomes dos animes

        for dia_semana in range(1,semanas): 
            
            #anime.clear() # - Limpa o array a cada passado do for, para armazenar só os animes do dia correspondente.
        
            #- animes_for_dia pega todos os itens h4 (tags <h4>) dentro do container do dia x
            animes_por_dia = len(list(soup.find_all('div', {'class': 'atualizacoes-semana-'+str(dia_semana)+''})[0].find_all('h4')))
            
            # - o for abaixo, insere todos os nomes de animes, com base no total de itens, em animes_por_dia
            for anime_dia in range(0,animes_por_dia):
                anime.append(soup.find_all('div', {'class': 'atualizacoes-semana-'+str(dia_semana)+''})[0].find_all('div', {'class': 'anime-transmissao-nome'})[anime_dia].find('h4').text)

        max_page = len(anime)
        resdata = len(anime)
        first_run = True
        num = 1
        contador = 0
        while True:
            if first_run:
                try:
                    conect=requests.get('https://www.animestc.com/?s={}'.format(anime[contador]))
                    soup=BeautifulSoup(conect.text,"lxml")
                    #pegando img
                    link_img=soup.find_all('div',{'class':'pag-anime-dados-esquerda'})[0].find('img')
                    #pegando nome
                    Title_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find('h1').text
                    #pegando episodios
                    ep_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find('li').text
                    #pegando genero
                    genero_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[1].text
                    #pegando classificação
                    class_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[2].text
                    #pegando ano
                    ano_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[3].text
                    #pegando estudio
                    estudio_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[4].text
                    #pegando status
                    status_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[5].text
                    #pegando sinopse
                    sinopse_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find('p').text
                    
                    icon = 'https://images-ext-2.discordapp.net/external/wEvP_GFZMlpWDdjkvr465GPbDL7I3vIU7YmG-o2hl6A/https/www.animestc.com/wp-content/uploads/2016/01/Logo-Tele23-50x50.png'
                    embed = discord.Embed(color=0x19212d)
                    embed.set_thumbnail(url=link_img['data-src'])
                    embed.set_author(name=Title_anime, icon_url=icon)
                    embed.set_footer(text="Athus V1.0")
                    embed.add_field(name="Outros Nomes:", value=Title_anime, inline=True)
                    embed.add_field(name="Episodios", value=ep_anime[10:], inline=True)
                    embed.add_field(name="Status", value=status_anime[13:], inline=True)
                    embed.add_field(name="Nota", value="...", inline=True)
                    embed.add_field(name="Lançado", value=ano_anime[4:], inline=True)
                    embed.add_field(name="Estudio", value=estudio_anime[8:], inline=True)
                    embed.add_field(name="Classificação", value=class_anime[14:], inline=True)
                    embed.add_field(name="Gênero", value=genero_anime[9:], inline=True)
                    embed.add_field(name="Synopsis", value=sinopse_anime, inline=False)
                    #embed.add_field(name="Synopsis", value="teste", inline=False)
                    first_run = False
                    msg = await ctx.send(embed=embed)
                except IndexError as e:
                    link_img = "https://i.imgur.com/rf5C3A3.png"
                    Title_anime = anime[contador]
                    ep_anime = "Erro Loading"
                    genero_anime = "Erro Loading"
                    class_anime = "Erro Loading"
                    ano_anime = "Erro Loading"
                    estudio_anime = "Erro Loading"
                    status_anime = "Erro Loading"
                    sinopse_anime = "Erro Loading"

                    icon = 'https://images-ext-2.discordapp.net/external/wEvP_GFZMlpWDdjkvr465GPbDL7I3vIU7YmG-o2hl6A/https/www.animestc.com/wp-content/uploads/2016/01/Logo-Tele23-50x50.png'
                    embed = discord.Embed(color=0x19212d)
                    embed.set_thumbnail(url=link_img)
                    embed.set_author(name=Title_anime, icon_url=icon)
                    embed.set_footer(text=e)
                    embed.add_field(name="Outros Nomes:", value=Title_anime, inline=True)
                    embed.add_field(name="Episodios", value=ep_anime, inline=True)
                    embed.add_field(name="Status", value=status_anime, inline=True)
                    embed.add_field(name="Nota", value="...", inline=True)
                    embed.add_field(name="Lançado", value=ano_anime, inline=True)
                    embed.add_field(name="Estudio", value=estudio_anime, inline=True)
                    embed.add_field(name="Classificação", value=class_anime, inline=True)
                    embed.add_field(name="Gênero", value=genero_anime, inline=True)
                    embed.add_field(name="Synopsis", value=sinopse_anime, inline=False)
                    #embed.add_field(name="Synopsis", value="teste", inline=False)
                    first_run = False
                    msg = await ctx.send(embed=embed)
    
            reactmoji = []
            if max_page == 1 and num == 1:
                pass
            elif num == 1:
                reactmoji.append('⏩')
            elif num == max_page:
                reactmoji.append('⏪')
            elif num > 1 and num < max_page:
                reactmoji.extend(['⏪', '⏩'])
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
            elif '⏪' in str(res.emoji):
                #print('<< Going backward')
                num = num - 1
                contador -= 1
                #www.animestc.com/?s=<anime name>
                try:
                    conect=requests.get('https://www.animestc.com/?s={}'.format(anime[contador]))
                    soup=BeautifulSoup(conect.text,"lxml")
                    #pegando img
                    link_img=soup.find_all('div',{'class':'pag-anime-dados-esquerda'})[0].find('img')
                    #pegando nome
                    Title_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find('h1').text
                    #pegando episodios
                    ep_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find('li').text
                    #pegando genero
                    genero_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[1].text
                    #pegando classificação
                    class_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[2].text
                    #pegando ano
                    ano_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[3].text
                    #pegando estudio
                    estudio_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[4].text
                    #pegando status
                    status_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[5].text
                    #pegando sinopse
                    sinopse_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find('p').text
                    
                    icon = 'https://images-ext-2.discordapp.net/external/wEvP_GFZMlpWDdjkvr465GPbDL7I3vIU7YmG-o2hl6A/https/www.animestc.com/wp-content/uploads/2016/01/Logo-Tele23-50x50.png'
                    embed = discord.Embed(color=0x19212d)
                    embed.set_thumbnail(url=link_img['data-src'])
                    embed.set_author(name=Title_anime, icon_url=icon)
                    embed.set_footer(text="Athus V1.0")
                    embed.add_field(name="Outros Nomes:", value=Title_anime, inline=True)
                    embed.add_field(name="Episodios", value=ep_anime[10:], inline=True)
                    embed.add_field(name="Status", value=status_anime[13:], inline=True)
                    embed.add_field(name="Nota", value="...", inline=True)
                    embed.add_field(name="Lançado", value=ano_anime[4:], inline=True)
                    embed.add_field(name="Estudio", value=estudio_anime[8:], inline=True)
                    embed.add_field(name="Classificação", value=class_anime[14:], inline=True)
                    embed.add_field(name="Gênero", value=genero_anime[9:], inline=True)
                    embed.add_field(name="Synopsis", value=sinopse_anime, inline=False)
                    #embed.add_field(name="Synopsis", value="teste", inline=False)
                    await msg.clear_reactions()
                    await msg.edit(embed=embed)

                except IndexError as e:
                    link_img = "https://i.imgur.com/rf5C3A3.png"
                    Title_anime = anime[contador]
                    ep_anime = "Erro Loading"
                    genero_anime = "Erro Loading"
                    class_anime = "Erro Loading"
                    ano_anime = "Erro Loading"
                    estudio_anime = "Erro Loading"
                    status_anime = "Erro Loading"
                    sinopse_anime = "Erro Loading"

                    icon = 'https://images-ext-2.discordapp.net/external/wEvP_GFZMlpWDdjkvr465GPbDL7I3vIU7YmG-o2hl6A/https/www.animestc.com/wp-content/uploads/2016/01/Logo-Tele23-50x50.png'
                    embed = discord.Embed(color=0x19212d)
                    embed.set_thumbnail(url=link_img)
                    embed.set_author(name=Title_anime, icon_url=icon)
                    embed.set_footer(text=e)
                    embed.add_field(name="Outros Nomes:", value=Title_anime, inline=True)
                    embed.add_field(name="Episodios", value=ep_anime, inline=True)
                    embed.add_field(name="Status", value=status_anime, inline=True)
                    embed.add_field(name="Nota", value="...", inline=True)
                    embed.add_field(name="Lançado", value=ano_anime, inline=True)
                    embed.add_field(name="Estudio", value=estudio_anime, inline=True)
                    embed.add_field(name="Classificação", value=class_anime, inline=True)
                    embed.add_field(name="Gênero", value=genero_anime, inline=True)
                    embed.add_field(name="Synopsis", value=sinopse_anime, inline=False)
                    await msg.clear_reactions()
                    await msg.edit(embed=embed)



            elif '⏩' in str(res.emoji):
                #print('\t>> Going forward')
                num = num + 1
                contador += 1

                try:
                    conect=requests.get('https://www.animestc.com/?s={}'.format(anime[contador]))
                    soup=BeautifulSoup(conect.text,"lxml")
                    #pegando img
                    link_img=soup.find_all('div',{'class':'pag-anime-dados-esquerda'})[0].find('img')
                    #pegando nome
                    Title_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find('h1').text
                    #pegando episodios
                    ep_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find('li').text
                    #pegando genero
                    genero_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[1].text
                    #pegando classificação
                    class_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[2].text
                    #pegando ano
                    ano_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[3].text
                    #pegando estudio
                    estudio_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[4].text
                    #pegando status
                    status_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find_all("li")[5].text
                    #pegando sinopse
                    sinopse_anime=soup.find_all('div',{'class':'pag-anime-dados-direita'})[0].find('p').text
                    
                    icon = 'https://images-ext-2.discordapp.net/external/wEvP_GFZMlpWDdjkvr465GPbDL7I3vIU7YmG-o2hl6A/https/www.animestc.com/wp-content/uploads/2016/01/Logo-Tele23-50x50.png'
                    embed = discord.Embed(color=0x19212d)
                    embed.set_thumbnail(url=link_img['data-src'])
                    embed.set_author(name=Title_anime, icon_url=icon)
                    embed.set_footer(text="Athus V1.0")
                    embed.add_field(name="Outros Nomes:", value=Title_anime, inline=True)
                    embed.add_field(name="Episodios", value=ep_anime[10:], inline=True)
                    embed.add_field(name="Status", value=status_anime[13:], inline=True)
                    embed.add_field(name="Nota", value="...", inline=True)
                    embed.add_field(name="Lançado", value=ano_anime[4:], inline=True)
                    embed.add_field(name="Estudio", value=estudio_anime[8:], inline=True)
                    embed.add_field(name="Classificação", value=class_anime[14:], inline=True)
                    embed.add_field(name="Gênero", value=genero_anime[9:], inline=True)
                    embed.add_field(name="Synopsis", value=sinopse_anime, inline=False)
                    #embed.add_field(name="Synopsis", value="teste", inline=False)
                    await msg.clear_reactions()
                    await msg.edit(embed=embed)
                except IndexError as e:
                    link_img = "https://i.imgur.com/rf5C3A3.png"
                    Title_anime = anime[contador]
                    ep_anime = "Erro Loading"
                    genero_anime = "Erro Loading"
                    class_anime = "Erro Loading"
                    ano_anime = "Erro Loading"
                    estudio_anime = "Erro Loading"
                    status_anime = "Erro Loading"
                    sinopse_anime = "Erro Loading"

                    icon = 'https://images-ext-2.discordapp.net/external/wEvP_GFZMlpWDdjkvr465GPbDL7I3vIU7YmG-o2hl6A/https/www.animestc.com/wp-content/uploads/2016/01/Logo-Tele23-50x50.png'
                    embed = discord.Embed(color=0x19212d)
                    embed.set_thumbnail(url=link_img)
                    embed.set_author(name=Title_anime, icon_url=icon)
                    embed.set_footer(text=e)
                    embed.add_field(name="Outros Nomes:", value=Title_anime, inline=True)
                    embed.add_field(name="Episodios", value=ep_anime, inline=True)
                    embed.add_field(name="Status", value=status_anime, inline=True)
                    embed.add_field(name="Nota", value="...", inline=True)
                    embed.add_field(name="Lançado", value=ano_anime, inline=True)
                    embed.add_field(name="Estudio", value=estudio_anime, inline=True)
                    embed.add_field(name="Classificação", value=class_anime, inline=True)
                    embed.add_field(name="Gênero", value=genero_anime, inline=True)
                    embed.add_field(name="Synopsis", value=sinopse_anime, inline=False)
                    await msg.clear_reactions()
                    await msg.edit(embed=embed)

            
            elif '❌' in str(res.emoji):
                await ctx.message.delete()
                return await msg.delete()
        self.client.counter += 1



def setup(client):
    client.add_cog(Animes_Mangas(client))

 