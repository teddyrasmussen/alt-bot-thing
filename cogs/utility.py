from multiprocessing.connection import Client
from random import randint
import discord
from discord.ext import commands
from discord.ext.commands import context
from discord.shard import ShardInfo
from discord.user import User
from discord.utils import get
from datetime import datetime
import os
import collections
import time, datetime
from discord.ext.commands.cooldowns import BucketType
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
import random
import psutil
import json

colorfile = "utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data['COLORS'], 16)

class utility(commands.Cog):
    def __init__(self, bot):
        '''Utility commands for discord'''
        self.bot = bot

    @commands.command()
    async def server(self, ctx):
        '''Get information about the server.'''

        statuses = collections.Counter([m.status for m in ctx.guild.members])

        embed = discord.Embed(title=f"{ctx.guild.name}", color=color)
        embed.description = ctx.guild.description if ctx.guild.description else None
        embed.add_field(name='**General:**',
                        value=f'Owner: **{ctx.guild.owner}**\n'
                              f'Created on: **{datetime.datetime.strftime(ctx.guild.created_at, "%A %d %B %Y at %H:%M")}**\n'
                              f'*Total Users: **{ctx.guild.member_count}**\n'
                              f'<:online:778677538788212737>: **{statuses[discord.Status.online]:,}**\n'
                              f'I<:idle:778677538838544394>: **{statuses[discord.Status.idle]:,}**\n'
                              f'<:dnd:778677540490706955>: **{statuses[discord.Status.dnd]:,}**\n'
                              f'<:offline:778677539685007470>: **{statuses[discord.Status.offline]:,}**\n'
                              f'**Boost Tier: **{ctx.guild.premium_tier}**\n'
                              f'Region: **{ctx.guild.region}**\n'
                              f'Boosters: **{ctx.guild.premium_subscription_count}**\n'
                              f'Max File Size: **{round(ctx.guild.filesize_limit / 1048576)} MB**\n'
                              f'Bitrate: **{round(ctx.guild.bitrate_limit / 1000)} kbps**\n'
                              f'Max Emojis: {ctx.guild.emoji_limit}\n', inline=False)

        embed.add_field(name='**Channel Information:**',
                        value=f'AFK timeout: **{int(ctx.guild.afk_timeout / 60)}m**\n'
                              f'AFK channel: **{ctx.guild.afk_channel}**\n'
                              f'Text Channels: **{len(ctx.guild.text_channels)}**\n'
                              f'Voice Channels **{len(ctx.guild.voice_channels)}**\n', inline = False)

        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_image(url=ctx.guild.banner_url)
        embed.set_footer(text=f'Guild ID: {ctx.guild.id}')

        return await ctx.send(embed=embed)

    @commands.command()
    async def user(self, ctx, *, member: discord.Member = None):
        '''Get information about the mentioned user.'''
        if member is None:
            member = ctx.author

        if len(member.activities) > 0:
            for activity in member.activities:
                if isinstance(activity, discord.Spotify):
                    activity = 'Listening to `Spotify`'
                elif isinstance(activity, discord.Game):
                    activity = f'Playing `{activity.name}``'
                elif isinstance(activity, discord.Streaming):
                    activity = f'Streaming `{activity.name}`'
                else:
                    activity = '`None`'
        else:
            activity = '`None`'
        statuses = {
                    "online": "<:online:778677538788212737>",
                    "idle": "<:idle:778677538838544394>",
                    "dnd": "<:dnd:778677540490706955>",
                    "offline": "<:offline:778677539685007470>"
                    }
        embed = discord.Embed(title=f"{member}", color=color)
        embed.add_field(name='**General:**',
                        value=f'Name: `{member}`\n' 
                              f'Status: {statuses[str(member.status)]}\n'
                              f'Account Created on: `{datetime.datetime.strftime(member.created_at, "%A %d %B %Y at %H:%M")}`', inline=False)

        embed.add_field(name='**Guild related information:**',
                        value=f'Joined guild: `{datetime.datetime.strftime(member.joined_at, "%A %d %B %Y at %H:%M")}`\n'
                              f'Nickname: `{member.nick}`\n'
                              f'Top role: {member.top_role.mention}', inline=False)

        embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Member ID: {member.id}')

        return await ctx.send(embed=embed)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, member: discord.Member=None):
        '''Get the avatar of the mentioned member.'''
        if not member: # if member is no mentioned
            member = ctx.message.author # set member as the author
        avatarembed = discord.Embed( color=color)
        avatarembed.set_author(name=member, icon_url=ctx.author.avatar_url)
        avatarembed.set_image(url=member.avatar_url)
        await ctx.send(embed=avatarembed)

    @commands.command()
    async def ping(self, ctx):
        '''Get the bot ping'''                        
        pingembed = discord.Embed(title="Pong!", color=color)
        pingembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        pingembed.add_field(name="<:server:778738233310838785> Server", value=f'```autohotkey\n{round(self.bot.latency * 1000)} ms```')
                        
        start = time.perf_counter()
        message = await ctx.send("Pinging...")
        end = time.perf_counter()
        duration = (end - start) * 1000
                        
        pingembed.add_field(name="<a:typing:778738457828524032> Typing", value='```autohotkey\n{:.2f} ms```'.format(duration))
                        
        await message.edit(embed=pingembed)

    @commands.command()
    async def stats(self ,ctx):
        '''Get the bot stats'''
        await ctx.send(f'Titanium is watching for commands {len(self.bot.users)} users in {len(self.bot.guilds)} guilds!\nCPU Usage: {psutil.cpu_percent()}%\nRAM USAGE: {psutil.virtual_memory().percent}%')

def setup(bot):
    bot.add_cog(utility(bot))
