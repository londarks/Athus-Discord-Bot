import sqlite3
import discord
from discord.ext import commands
import asyncio


class Badges(commands.Cog):
    def __init__(self,client):
        self.client = client


def setup(client):
    client.add_cog(Badges(client))