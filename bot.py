import os, asyncio, discord, json, logging, datetime, aiohttp

from discord import Embed
from discord.ext import commands

from utils.help import EmbedHelpCommand

log = logging.getLogger("titanium.core")
logging.basicConfig(level=logging.INFO, datefmt="%I:%M %p on %B %d %Y", format="%(asctime)s:%(levelname)s: %(name)s: %(message)s")

# support stuff

supportchnlids = []
supportathrids = []

# config
tokenFile = "utils/config.json"
with open(tokenFile) as f:
    data = json.load(f)
token = data["TOKEN"]

prefixFile = "utils/tools.json"
with open(prefixFile) as f:
    data = json.load(f)
prefixes = data["PREFIXES"]

intents = discord.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix = prefixes, intents=intents)
bot.help_command = EmbedHelpCommand()

bot.owner_ids = {555709231697756160}
#bot.remove_command("help")

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

# also 
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"


@bot.event
async def on_ready():
    log.info("{0.user} is up and running".format(bot))
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if message.content.endswith("<@!751447995270168586>"):
        embed = discord.Embed(title="Titanum", description="Hey there :wave: Seems like you mentioned me.\n\nMy prefixes are: \nIf you would like to see my commands type `[prefix]help`", color=0x2F3136)
        await message.channel.send(embed=embed)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        log.info(f"Loaded cog {filename[:-3]}")

@bot.command()
async def supportrequest(ctx, *, msg: str):
    """Send a message to my support team!"""
    emb = discord.Embed(
        title = "Support Request!",
        description = f"Message: {msg}\nAuthor ID to reply: {ctx.author.id}",
            )
    time = datetime.datetime.now()
    time = time.strftime("%b %d at %I:%M %p")
    emb.set_author(name = f"{ctx.author}", icon_url = ctx.author.avatar_url)
    emb.set_footer(text = f"New support request by {ctx.author} on {time}")
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url("https://canary.discord.com/api/webhooks/764934046940659762/sJOO0N6O2MHqRxpr1LyWRfPgBFzcyBFe1CnXV4gJ4OqmWWcx-Z49DZBAPceiixOZjDkA", adapter=discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = emb, username = ctx.author.name, avatar_url = ctx.author.avatar_url)
    await ctx.send("Message sent!")
    supportathrids.append(ctx.author.id)
    supportchnlids.append(ctx.channel.id)

@bot.command()
@commands.has_role(764306292675969029)
async def replysupport(ctx, userid: int, *, msg: str):
    for id in supportathrids:
        if id == userid:
            channel = bot.get_channel(supportchnlids[supportathrids.index(id)])
            emb = discord.Embed(
                title = "Support Message!",
                description = f"My support team has asked me to send you this message:\n{msg}",
            )
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await channel.send(f"<@!{userid}>")
            await channel.send(embed=emb)
            supportathrids.remove(id)
            supportchnlids.pop(supportathrids.index(id))
    await ctx.send(f"📤 Message sent!")

@bot.command(aliases=["shutdown"])
@commands.is_owner()
async def restart(ctx):
    await ctx.send("👋 Bye!")
    await bot.logout()
    log.info("Protecc exited with exit code 0 (intentional)")

bot.load_extension("jishaku")

bot.run(token)