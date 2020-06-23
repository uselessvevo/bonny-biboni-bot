"""
Description: useful tools (administration, module management, etc.)
Version: 0620/prototype
Author: useless_vevo
"""
# Standard libraries
import re

# Discord
import discord
from discord.ext import commands

# i18n module
from CloudyKit.Common.i18n import tr, Locales
from CloudyKit.Common.i18n import alias

# Management
from CloudyKit.Core.manager import Guilds
from CloudyKit.Core.settings import Global


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=alias('set_guild_prefix'), pass_context=True)
    @commands.has_permissions(administrator=True)
    async def set_guild_prefix(self, ctx, prefix):
        # if prefix is a word then add space
        if not re.match(r'[@_!#$%^&*()<>?/\|}{~:]', prefix):
            prefix += ' '

        Guilds.update_guild(ctx.message.guild.id, prefix=prefix)
        await ctx.send(tr('Done. Prefix is: **{prefix}**', ctx, prefix=prefix))

    @commands.command(aliases=alias('set_guild_locale'), pass_context=True)
    @commands.has_permissions(administrator=True)
    async def set_guild_locale(self, ctx, locale: str = None):
        """
        Set guild locale
        Args:
            ctx (discord.Message) - context
            locale (str) - locale key code in lower case
        """
        locale = locale.lower()
        if re.match(r'[a-z]{3}', locale):
            if locale == Guilds.get_guild_info(ctx.message.guild.id, 'locale'):
                await ctx.send(tr('It\'s the same locale', ctx))
            else:
                Guilds.update_guild(ctx.message.guild.id, locale=locale)
                Locales.load_translations(locale)

                await ctx.send(tr('Done. Locale is: **{locale}**', ctx, locale=locale))
        else:
            await ctx.send(tr('Locale format must be look like: lc', ctx))

    @commands.command(aliases=alias('set_guild_message_log_channel'), pass_context=True)
    async def set_guild_message_log_channel(self, ctx, channel: int):
        """
        Set guild message log channel.
        Global -> bot_default_message_logs_channel is the default channel
        """
        if channel:
            channel = self.bot.get_channel(channel)
        else:
            # I'm not a spy. Trust me.
            channel = Global.get('bot_default_message_logs_channel')

    @commands.command(aliases=alias('set_guild_error_log_channel'), pass_context=True)
    async def set_guild_error_log_channel(self, ctx, gid: int):
        if isinstance(gid, int) and self.bot.get_channel(gid):
            ctx.send(True)

    @commands.command(aliases=alias('guild_info'), pass_context=True)
    async def guild_info(self, ctx):
        info = Guilds.get_guild_info(ctx.message.guild.id)
        embed = discord.Embed()
        embed.title = tr('Guild info', ctx)
        embed.description = (
            f'\n• {tr("Locale", ctx)}: {info.get("locale")}'
            f'\n\n• {tr("Prefix", ctx)}: {info.get("prefix")}'
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=alias('purge_message'), pass_context=True)
    @commands.has_permissions(administrator=True)
    async def purge_message(self, ctx, amount: int, channel: int = None):
        if channel:
            pass
        else:
            await ctx.channel.purge(limit=amount)


def setup(bot):
    bot.add_cog(Administration(bot))
