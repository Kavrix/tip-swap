import discord
from discord.ext import commands

class Rates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="rates", description="Show current exchange rates")
    async def rates(self, ctx):
        rates = "\n".join([f"{k}: {v}" for k, v in self.bot.exchange_rates.items()])
        await ctx.respond(f"💱 Current exchange rates:\n{rates}", ephemeral=True)

    @commands.slash_command(name="setrate", description="Admin: Set exchange rate between two coins")
    async def setrate(self, ctx, from_coin: str, to_coin: str, rate: float):
        if ctx.author.id not in self.bot.admins:
            await ctx.respond("❌ You are not authorized.", ephemeral=True)
            return
        key = f"{from_coin.upper()}->{to_coin.upper()}"
        self.bot.exchange_rates[key] = rate
        await ctx.respond(f"✅ Set exchange rate: {key} = {rate}")

def setup(bot):
    bot.add_cog(Rates(bot))
