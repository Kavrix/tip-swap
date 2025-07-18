import discord
from discord.ext import commands

class Deposit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="deposit", description="Get your deposit address for a coin")
    async def deposit(self, ctx, coin: str):
        coin = coin.upper()
        if coin not in self.bot.wallets:
            await ctx.respond("❌ Unsupported coin.", ephemeral=True)
            return
        addr = self.bot.wallets[coin].get_new_address()
        await ctx.respond(f"📥 Deposit address for {coin}: `{addr}`", ephemeral=True)

def setup(bot):
    bot.add_cog(Deposit(bot))
