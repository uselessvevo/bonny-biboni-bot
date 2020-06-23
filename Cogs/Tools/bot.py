"""
Description: useful tools (administration, module management, etc.)
Version: 0620/prototype
Author: useless_vevo
"""
# Standard libraries
import sys
import platform
import subprocess

# Discord
import discord
from discord.ext import commands
from discord.ext.commands import ExtensionError

# i18n module
from CloudyKit.Common.i18n import tr, Locales
from CloudyKit.Common.i18n import alias

# Base tools
from CloudyKit.Common.discordtools import set_presence

# Managment
from CloudyKit.Core.manager import Guilds
from CloudyKit.Core.settings import Global


class BotManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=alias('info'), pass_context=True)
    async def info(self, ctx):
        embed = discord.Embed()
        embed.colour = discord.Color.from_rgb(178, 66, 219)

        uname = platform.uname()
        embed.description = f'''
            • :snake: Python - {sys.winver}
            • :space_invader: Discord API - {discord.__version__}
            • :pager: {uname.system}
            • :computer: {uname.machine}
            • :bulb: {uname.processor}
        '''
        embed.set_author(
            name=tr('The best bot in the world', ctx),
            icon_url=self.bot.get_user(self.bot.user.id).avatar_url
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=alias('restart'), pass_context=True)
    @commands.is_owner()
    async def restart(self, ctx):
        embed = discord.Embed(
            title=tr('Rebooting', ctx=ctx, emoji='gear'),
            color=discord.Color.from_rgb(255, 188, 64),
        )
        subprocess.call([sys.executable, 'Bot/bot.py'])
        await ctx.send(embed=embed)

    @restart.error
    async def restart_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(tr('Access denied', ctx=ctx, emoji='alien'))

    @commands.command(aliases=alias('reload_module'), pass_context=True)
    @commands.is_owner()
    async def reload_module(self, ctx, *cogs):
        # "prefix *"             - each module
        # "prefix Module.module" - specific one
        if cogs:
            if '*' in cogs:
                cogs = Global.get('modules_to_load', [])
            else:
                cogs = [f'Cogs.{i}' for i in cogs]

            for cog in cogs:
                if cog in self.bot.extensions:
                    try:
                        self.bot.reload_extension(cog)
                        await ctx.send(tr(
                            'Module was rebooted - `{module}`', ctx, 'wrench', 1, module=cog
                        ))
                    except ExtensionError:
                        await ctx.send(tr(
                            'Failed to reboot module - `{module}`', ctx, 'fire', 1, module=cog
                        ))
                else:
                    await ctx.send(tr(
                        'Module doesn\'t exist - `{module}`', ctx, 'warning', 1, module=cog
                    ))

            # Add guild id check
            Locales.load_aliases(cogs)
            Locales.load_translations(modules=cogs)
            await ctx.send(tr('Updated localization files', ctx, 'bookmark', 1))

    @reload_module.error
    async def reload_module_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(tr('Access denied', ctx=ctx))

        if isinstance(error, commands.BadArgument):
            await ctx.send('Invalid argument')

    @commands.command(aliases=alias('set_presence'), pass_context=True)
    @commands.is_owner()
    async def set_presence(self, ctx, presence: int = None):
        presences = (
            ('online', (157, 245, 110)),  # online/green
            ('idle', (252, 219, 3)),  # idle/orange
            ('dnd', (219, 66, 74)),   # dnd/red
            ('offline', (158, 158, 158)),   # offline/white
            ('invisible', (158, 158, 158)),   # invisible/white
        )

        embed = discord.Embed()
        embed.title = tr('Status set to **{status_name}**', ctx, status_name=presences[presence][0])
        embed.colour = discord.Color.from_rgb(*presences[presence][1])

        await ctx.send(embed=embed)
        await set_presence(self.bot, presence=presence)

    @commands.command(aliases=alias('get_guilds_in_use'), pass_context=True)
    @commands.is_owner()
    async def get_guilds_in_use(self, ctx):
        await ctx.send([self.bot.get_guild(g) for g in Guilds.guilds if g])

    @commands.command(aliases=alias('tr'), pass_context=True)
    @commands.is_owner()
    async def tr(self, ctx):
        await ctx.send([f'{k} - {v}' for (k, v) in Locales.translations["alias"].items()])


def setup(bot):
    bot.add_cog(BotManagement(bot))
