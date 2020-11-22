from discord.ext import commands
from pymongo import MongoClient

import discord

class welcomer(commands.Cog):
    """Welcome new members to your server"""
    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        db = mcl.titanium
        self.data = db.welcome
    
    @commands.has_permissions(kick_members = True)
    @commands.group()
    async def welcomeset(self, ctx):
        """Welcome members to your server!"""
        pass

    @welcomeset.command()
    async def channel(self, ctx, channel: discord.TextChannel = None):
        """Set the channel Titanium will welcome members in"""
        doc = self.data.find_one({"_id":ctx.guild.id})

        if not channel and not doc['chnl']:
            await ctx.send("You didn't specify a channel!")
        elif not channel and doc['chnl']:
            self.data.update_one(filter = {"_id": ctx.guild.id}, update={"$unset": {"chnl": ""}})
            await ctx.send("Channel cleared")
        elif channel and not doc['chnl']:
            self.data.update_one
        elif not doc and not doc['chnl']:
            self.data.insert_one(filter = {"_id": ctx.guild.id}, update = {"$set": {"chnl": channel.id}})
            await ctx.send(f"Successfully set the welcome channel to {channel.mention}")
    
    @welcomeset.command()
    async def joinmessage(self, ctx, msg: str = None):
        """Set the message sent upon guild join"""
        doc = self.data.find_one({"_id":ctx.guild.id})
        if not msg and not doc['joinmsg']:
            await ctx.send("You didn't specify a channel!")
        elif not msg and doc['joinmsg']:
            self.data.update_one(filter = {"_id": ctx.guild.id}, update={"$unset": {"joinmsg": None}})
            await ctx.send("Channel cleared")
        elif msg and doc['joinmsg'] or msg and doc and not doc['joinmsg']:
            self.data.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"joinmsg": msg}})
            await ctx.send(f"Successfully set the join msg to {msg}")
        elif msg and not doc:
            self.data.insert_one({"_id": ctx.guild.id, "joinmsg": msg})
            await ctx.send(f"Successfully set the join msg to {msg}")

    @welcomeset.command()
    async def togglejoin(self, ctx, toggle: bool):
        """Toggle sending join messages. Options are true and false."""
        doc = self.data.find_one({"_id":ctx.guild.id})
        if doc:
            self.data.update_one(filter={"_id": ctx.guild.id}, update={"$set": {"dojoins": toggle}})
            if toggle:
                await ctx.send("I will now send a message when someone joins this server (if the channel and message are configured")
            elif not toggle:
                await ctx.send("I will no longer send a message when someone joins this server")
        elif not doc:
            self.data.insert_one({"_id": ctx.guild.id, "dojoins": toggle})


    @commands.Cog.listener()
    async def on_member_join(self, member):
        doc = self.data.find_one({"_id": member.guild.id})
        if doc['joinmsg'] and doc['chnl'] and doc['dojoins']:
            chnl = self.bot.get_channel(doc['chnl'])
            await chnl.send(doc['joinmsg'].format(user=member))
    
def setup(bot):
    bot.add_cog(welcomer(bot))