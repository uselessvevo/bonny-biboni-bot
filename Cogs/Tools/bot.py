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
from Tools.Common.i18n import tr
from Tools.Common.i18n import alias
from Tools.Common.i18n import Locales

# Discord tools
from Tools.Common.discordtools import ModifiedHelpCommand

# Base tools
from Tools.Common.discordtools import set_presence

# Managment
from Tools.Core.manager import Guilds
from Tools.Core.settings import Global


class BotManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = ModifiedHelpCommand()
        self.bot.help_command.cog = self

    @commands.command(aliases=alias('info'), pass_context=True)
    async def info(self, ctx):
        embed = discord.Embed()
        embed.colour = discord.Color.from_rgb(178, 66, 219)

        uname = platform.uname()
        embed.description = f'''
            • :snake: Python - {sys.version.split()[0]}
            • :space_invader: Discord API - {discord.__version__}
            • :pager: {uname.system}
            • :computer: {uname.machine}
            • :bulb: {uname.processor}
        '''
        embed.set_author(
            name=tr('Cogs.Tools.Bot.BotInfoTitle', ctx),
            icon_url=self.bot.get_user(self.bot.user.id).avatar_url
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=alias('restart'), pass_context=True)
    @commands.is_owner()
    async def restart(self, ctx):
        embed = discord.Embed(
            title=tr('Cogs.Tools.Bot.RebootNotification', ctx=ctx, emoji='gear'),
            color=discord.Color.from_rgb(255, 188, 64),
        )
        subprocess.call([sys.executable, 'Bot/bot.py'])
        await ctx.send(embed=embed)

    @restart.error
    async def restart_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(tr('Cogs.Tools.Admin.AccessDenied', ctx=ctx, emoji='alien'))

    @commands.command(aliases=alias('reload_module'), pass_context=True)
    @commands.is_owner()
    async def reload_module(self, ctx, *cogs):
        # "prefix *"             - each module
        # "prefix Module.module" - specific one
        # TODO: add folder (group) reboot: "?rm Tools (will reboot each module)"
        if not cogs:
            cogs = Global.get('modules_to_load', [])
        else:
            cogs = [f'Cogs.{i}' for i in cogs]

        # At first we need to reload localization files
        Locales.load_aliases(cogs)
        Locales.load_translations(module_paths=cogs)
        await ctx.send(tr('Cogs.Tools.Bot.UpdatedLocalizationFiles', ctx, 'bookmark', 1))

        message = ''
        for cog in cogs:
            if cog in self.bot.extensions:
                try:
                    self.bot.reload_extension(cog)
                    message += tr('Cogs.Tools.Bot.ModuleWasRebooted', ctx, 'wrench', 1, module=cog) + '\n'
                except ExtensionError:
                    message += tr('Cogs.Tools.Bot.FailedToRebootModule', ctx, 'fire', 1, module=cog) + '\n'
            else:
                message += tr('Cogs.Tools.Bot.ModuleNotFound', ctx, 'warning', 1, module=cog) + '\n'

        await ctx.send(message)

    @reload_module.error
    async def reload_module_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(tr('Cogs.Tools.Admin.AccessDenied', ctx))

        if isinstance(error, commands.BadArgument):
            await ctx.send('Invalid argument')

    @commands.command(aliases=alias('reload_translations'), pass_context=True)
    @commands.is_owner()
    async def reload_translations(self, ctx):
        Locales.load_aliases()
        Locales.load_translations()
        await ctx.send(tr('Cogs.Tools.Bot.UpdatedLocalizationFiles', ctx, 'bookmark', 1))

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
        embed.title = tr('Cogs.Tools.Bot.StatusHasBeenSet', ctx, status_name=presences[presence][0])
        embed.colour = discord.Color.from_rgb(*presences[presence][1])

        await ctx.send(embed=embed)
        await set_presence(self.bot, presence=presence)

    @commands.group(name='picture_atlas', aliases=alias('pictures_atlas'), pass_context=True)
    async def pictures_atlas(self, ctx):
        pass

    @pictures_atlas.command(name='pictures_atlas_get', aliases=alias('pictures_atlas_get'), pass_context=True)
    async def get(self, ctx, alias_name):
        pass

    @pictures_atlas.command(name='pictures_atlas_list', aliases=alias('pictures_atlas_list'), pass_context=True)
    async def list(self, ctx):
        pass

    @pictures_atlas.command(name='pictures_atlas_append', aliases=alias('pictures_atlas_append'), pass_context=True)
    @commands.is_owner()
    async def append(self, ctx, link, alias_name):
        pass

    @pictures_atlas.command(name='pictures_atlas_remove', aliases=alias('pictures_atlas_remove'), pass_context=True)
    @commands.is_owner()
    async def remove(self, ctx, alias_name):
        pass

    @pictures_atlas.command(name='pictures_atlas_edit', aliases=alias('pictures_atlas_edit'), pass_context=True)
    @commands.is_owner()
    async def edit(self, ctx, alias_name):
        pass

    @commands.command(aliases=alias('get_guilds_in_use'), pass_context=True)
    @commands.is_owner()
    async def get_guilds_in_use(self, ctx):
        await ctx.send([self.bot.get_guild(g) for g in Guilds.guilds if g])

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def tr(self, ctx, locale=Global.get('default_locale')):
        await ctx.send('\n'.join(f'`{k} - {v}`' for (k, v) in Locales.translations[locale].items()))


def setup(bot):
    bot.add_cog(BotManagement(bot))
