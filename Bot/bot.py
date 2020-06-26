"""
Description: main bot module
Version: 0620/prototype
Author: useless_vevo
TODO: check channels on start
"""
# Standard libraries
import asyncio
import time
import datetime

# Discord
import discord
from discord.ext import commands

# Common
from CloudyKit.Common.i18n import tr
from CloudyKit.Common.discordtools import set_presence

# Management
from CloudyKit.Core.settings import Global
from CloudyKit.Core.manager import Guilds


class Bot(commands.Bot):
    def __init__(self):
        # Prepare bot
        token = Global.get('bot_token')
        description = 'info'.format('Hello?')
        self.pass_mods = Global.get('modules_to_pass', [])

        # Init bot
        super().__init__(
            command_prefix=self._get_prefix,
            case_insensitive=Global.get('bot_case_sensitive', False),
            description=description
        )

        for module in Global.get('modules_to_load', []):
            try:
                self.load_extension(module)
                message = 'Mod was loaded - {}'.format(module)
            except discord.ext.commands.errors.ExtensionNotLoaded as err:
                message = 'Failed to load {}\n{}: {}'.format(module, type(module).__name__, err)
            print(message)

        self.run(token)

    async def _get_prefix(self, bot, ctx):
        """ Get guild (by guild id) and default prefixes """
        if ctx.guild:
            return [
                Guilds.get_guild_info(ctx.guild.id, 'prefix'),
                Global.get('bot_default_prefix')
            ]
        else:
            return Global.get('bot_default_prefix')

    # Guild events

    async def on_guild_join(self, guild):
        """ If bot join. Add guild to Guilds table and cached dictionary """
        Guilds.insert_guild(
            gid=guild.id,
            locale=Global.get('default_locale'),
            prefix=Global.get('bot_default_prefix')
        )

        logs_channel = self.get_channel(Global.get('bot_default_message_logs_channel'))
        embed = discord.Embed()
        embed.set_author(name='New guild')
        embed.colour = discord.Color.from_rgb(169, 245, 110)
        embed.description = f'Bot added in the new channel {guild.name}/{guild.id}'

        await logs_channel.send(embed=embed)
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send('Hello!  :tennis:')
            break

    async def on_guild_remove(self, guild):
        """ If bot was removed from the server """
        Guilds.delete_guild(guild.id)

        logs_channel = self.get_channel(Global.get('bot_default_message_logs_channel'))
        embed = discord.Embed()
        embed.set_author(name='Guild removed')
        embed.colour = discord.Color.from_rgb(245, 110, 110)
        embed.description = f'Bot has been deleted from the guild {guild.name}/{guild.id}'

        await logs_channel.send(embed=embed)

    # User events

    async def on_member_join(self, member):
        """ If user join """

    async def on_member_remove(self, member):
        """ If user leave from the server """

    async def on_message(self, ctx: discord.Message):
        if not ctx.author.bot:
            logs_channel = self.get_channel(Global.get('bot_default_message_logs_channel', None))

            message = f'{ctx.author.mention} in #{ctx.guild.name}' if ctx.guild else f'{ctx.author.mention} in DM'
            if ctx.content:
                message += f'\n{tr("Text", ctx)}: {ctx.content}'
            if ctx.attachments:
                message += f'\n{tr("File", ctx)}: {ctx.attachments[0].proxy_url}'

            embed = discord.Embed()
            embed.set_author(
                name=tr('Message', ctx),
                icon_url=ctx.author.avatar_url
            )
            embed.colour = discord.Color.from_rgb(110, 162, 245)
            embed.description = message

            await logs_channel.send(embed=embed)
            await self.process_commands(ctx)

    async def on_message_edit(self, ctx_before, ctx_after):
        if not ctx_before.author.bot:
            logs_channel = self.get_channel(Global.get('bot_default_message_logs_channel'))
            embed = discord.Embed()
            embed.set_author(
                name=tr('Edit', ctx_before),
                icon_url=ctx_before.author.avatar_url
            )
            embed.colour = discord.Color.from_rgb(245, 124, 110)
            embed.description = (
                f'{ctx_before.author.mention} edited message in #{ctx_before.guild.name}'
                f'\nBefore: {ctx_before.content}'
                f'\nAfter: {ctx_after.content}'
            )

            await logs_channel.send(embed=embed)

    async def on_message_delete(self, ctx):
        if not ctx.author.bot:
            logs_channel = self.get_channel(Global.get('bot_default_message_logs_channel'))
            embed = discord.Embed()
            embed.set_author(
                name=tr('Delete', ctx),
                icon_url=ctx.author.avatar_url
            )
            embed.colour = discord.Color.from_rgb(245, 124, 110)
            embed.description = f'{ctx.author.mention} deleted message in #{ctx.guild.name}\n{ctx.content}'

            await logs_channel.send(embed=embed)

    # Commands

    async def on_command(self, ctx):
        await ctx.trigger_typing()

    async def on_command_error(self, ctx, error):
        logs_channel = self.get_channel(Global.get('bot_default_error_logs_channel', None))
        message = tr('Error', ctx)

        if isinstance(error, commands.CommandOnCooldown):
            member = ctx.message.author.mention
            message = tr('Please, wait {member}', ctx, member=member)

        elif isinstance(error, commands.UserInputError):
            message = tr('Invalid input in {arg}', ctx, arg=ctx.command)

        elif isinstance(error, commands.BadArgument):
            message = tr('Bad command argument in {arg}', arg=ctx.command.content)

        elif isinstance(error, commands.CommandNotFound):
            message = tr('Command `{arg}` not found', ctx, arg=ctx.message.content)

        elif isinstance(error, commands.CommandInvokeError):
            message = f'{tr("Command invoke error", ctx)}: {error.original}'

        elif isinstance(error, UnboundLocalError):
            message = f'{tr("Local error", ctx)}: {error}'

        title = tr('Error', ctx)
        embed_logs = discord.Embed()
        embed_logs.set_author(
            name=title,
            icon_url=ctx.message.author.avatar_url
        )
        embed_logs.colour = discord.Color.from_rgb(252, 197, 114)
        channel = ctx.guild.id if ctx.guild else 'DM'
        embed_logs.description = f'{ctx.message.author.mention} in {channel}\n{message}'
        embed_logs.set_footer(text=f'{datetime.datetime.fromtimestamp(time.time())}')

        await ctx.send(message)
        await logs_channel.send(embed=embed_logs)

    # Tasks

    async def check_database(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await asyncio.sleep(60)

    async def on_ready(self):
        message = 'Login: {}\nID: {}\n'.format(
            self.user.name,
            self.user.id
        )
        print(message)

        self.loop.create_task(set_presence(bot=self, presence=int(Global.get('presence', 0))))
        # self.loop.create_task(self.check_database)

        print('Ready')
