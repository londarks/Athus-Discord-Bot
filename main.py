import json
import sqlite3
import discord
from discord.ext.commands import AutoShardedBot, when_mentioned_or
import key




modulos = ["cogs.lojinha","cogs.imgur","cogs.translation","cogs.role",
           "cogs.animes_mangas","cogs.lol","cogs.status",
           "cogs.backpack","cogs.teste_background","cogs.fedback",
           "cogs.levelling","cogs.buy_item","cogs.rank",
           "cogs.meme","cogs.admin"]

client = AutoShardedBot(command_prefix="$", case_insensitive=True)
client.remove_command('help')
token = key.seu_token()
client.counter = 0

@client.event
async def on_ready():
    print(client.user.name)
    game = discord.Game("$Help...")
    await client.change_presence(status=discord.Status.idle, activity=game)


@client.event
async def on_member_join(member):
  if member.bot:
    return
  user_id = member.id
  user = member.name
  icon_bot = "https://i.imgur.com/Gvcsoz9.jpg"
  embed = discord.Embed(color=0x1ccc09)
  embed.set_author(name="Welcome",icon_url=icon_bot)
  embed.add_field(name="Bem-Vindo", value="<@!{}> Seja Bem vindo :)".format(user_id),inline=True)
  embed.add_field(name="Aviso", value="```yaml\n"
                                        "Seja Bem-vindo {}, Leias as regras do Servidor para interagir melhore.!"
                                        "```".format(user),inline=False)
  channel = client.get_channel("ID DA SALA DE BOAS VINDAS")
  await channel.send(embed=embed)

@client.event
async def on_member_remove(member):
  user = member.name
  icon_bot = "https://i.imgur.com/LnBRmHo.png"
  embed = discord.Embed(color=0x1ccc09)
  embed.set_author(name="Leave",icon_url=icon_bot)
  embed.add_field(name="Saiu do Servidor", value="```yaml\n"
                                        "-Delete {}... Usuario Deletado com Sucesso....De tchauzinho!"
                                        "```".format(user),inline=True)
  channel = client.get_channel("ID DA SALA DE BOAS VINDAS")
  await channel.send(embed=embed)

@client.command(pass_context=True)
async def help(ctx):
  author = ctx.author.id

  #icon_master = "https://i.imgur.com/nUPN1Pj.png"
  icon_bot = "https://i.imgur.com/4Jtk29h.jpg"
  embed = discord.Embed(color=0xffffff)
  #embed.set_thumbnail(url=icon_bot)
  embed.set_author(name="Athus", icon_url=icon_bot)
  embed.set_footer(text="Athus V1.0")
  embed.add_field(name="🔴Ajuda", value="Olá Bem vindo ao Bot Athus Clique aqui para ir no [Repositorio](https://github.com/londarks/Athus-Discord-Bot).", inline=False)
  await ctx.send(embed=embed)
  client.counter += 1

if __name__ == "__main__":
    for module in modulos:
        client.load_extension(module)
        print(f"modulo {module} carregado")
    client.run(token)
