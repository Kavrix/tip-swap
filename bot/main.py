import discord, json
from discord.ext import commands
from bot.db import Database
from bot.rpc_wallet import RPCWallet

with open("bot/config.json") as f:
    conf = json.load(f)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.db = Database(conf['mysql'])
bot.wallets = {coin: RPCWallet(data['rpc_url']) for coin, data in conf['coins'].items()}
bot.exchange_rates = conf['exchange_rates']
bot.admins = conf['admins']

@bot.event
async def on_ready():
    await bot.db.connect()
    print(f"Bot connected as {bot.user}")

# Load command cogs
for cog in ['tip', 'balance', 'swap', 'deposit', 'withdraw', 'rates']:
    bot.load_extension(f'bot.commands.{cog}')

bot.run(conf['discord_token'])
