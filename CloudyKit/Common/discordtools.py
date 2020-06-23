import asyncio
import hashlib
import random

import discord

from CloudyKit.Core.settings import Global


async def set_presence(bot: discord.Client, timer=1800, presence=0):
    presences = (
        discord.Status.online,
        discord.Status.idle,
        discord.Status.dnd,
        discord.Status.offline,
        discord.Status.invisible,
    )
    # Connect watchdog listener for file
    statuses = Global.get('bot_statuses', [])
    game = discord.Game(name=random.choice(statuses))

    while True:
        await bot.change_presence(
            status=presences[presence],
            activity=game,
        )
        await asyncio.sleep(timer)


async def get_members(ctx):
    return [m.mention for m in ctx.guild.members if not m.bot]


def hash_filename(file, cut=5, output='hash_%s.jpg'):
    """
    Args:
        file (str) - filename
        cut (int) - list slice
        output (str) - output filename
    """
    hashed = hashlib.sha1(file.encode())
    # Get slice from hash
    hashed = hashed.hexdigest()[:cut]
    hashed = output % hashed
    return hashed
