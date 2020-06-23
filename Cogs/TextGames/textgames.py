"""
Description: text games (rps, guess, etc.)
Version: 0620/prototype
Author: useless_vevo
"""
# Standard libraries
import datetime
import random

# Discord
from discord.ext import commands

# Common
from CloudyKit.Common.i18n import tr
from CloudyKit.Common.i18n import alias
from CloudyKit.Common.discordtools import get_members


class TextGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=alias('who'), pass_context=True)
    async def who(self, ctx, *text):
        member = random.choice(await get_members(ctx))
        await ctx.send(tr('I think {member} {action}', ctx, True, member=member, action=' '.join(text)))

    @commands.command(aliases=alias('when'), pass_context=True)
    async def when(self, ctx):
        # the day of soviet union death. no commo
        min_year = 1991
        max_year = datetime.datetime.now().year

        start = datetime.datetime(min_year, 1, 1)
        years = max_year - min_year + 1
        end = start + datetime.timedelta(days=365 * years)
        result_date = start + (end - start) * random.random()

        if result_date > datetime.datetime.now():
            await ctx.send(tr(
                'It will happen in {date} at {time}',
                ctx=ctx,
                date=datetime.datetime.strftime(result_date, '%D'),
                time=datetime.datetime.strftime(result_date, '%d:%m:%y')
            ))
        elif result_date <= datetime.datetime.now():
            await ctx.send(tr(
                'It happened {date} at {time}',
                ctx=ctx,
                date=datetime.datetime.strftime(result_date, '%D'),
                time=datetime.datetime.strftime(result_date, '%d:%m:%y')
            ))
        else:
            await ctx.send('huh? what happened?')

    @commands.command(aliases=alias('rtd'), pass_context=False)
    async def rtd(self, ctx):
        pass

    @commands.command(aliases=alias('rock-paper-scissors'), pass_context=False)
    async def rock_paper_scissors(self, ctx):
        pass

    @commands.group(aliases=alias('rock-paper-scissors'), pass_context=False)
    async def russian_roulette(self, ctx, select=None):
        if not select:
            await ctx.send(tr('Info', ctx))

    @russian_roulette.command(name='set_bullets_amount')
    async def set_bullets_amount(self, ctx, amount=8):
        await ctx.send(tr('set_bullets_amount', ctx))

    @russian_roulette.command(name='enter')
    async def enter(self, ctx):
        await ctx.send(tr('enter', ctx))

    @russian_roulette.command(name='leave')
    async def leave(self, ctx):
        await ctx.send(tr('leave', ctx))

    @russian_roulette.command(name='roll')
    async def roll(self, ctx):
        await ctx.send(tr('roll', ctx))


def setup(bot):
    bot.add_cog(TextGames(bot))
