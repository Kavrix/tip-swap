import discord
from discord.ext import commands

class Swap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="swap", description="Swap one coin for another at fixed rates")
    async def swap(self, ctx, from_coin: str, to_coin: str, amount: float):
        from_coin, to_coin = from_coin.upper(), to_coin.upper()
        if from_coin == to_coin:
            await ctx.respond("❌ Can't swap a coin for itself.", ephemeral=True)
            return
        if from_coin not in self.bot.wallets or to_coin not in self.bot.wallets:
            await ctx.respond("❌ Unsupported coin.", ephemeral=True)
            return
        key = f"{from_coin}->{to_coin}"
        if key not in self.bot.exchange_rates:
            await ctx.respond("❌ No exchange rate available.", ephemeral=True)
            return
        rate = self.bot.exchange_rates[key]
        to_amount = amount * rate
        from_balance = await self.bot.db.get_balance(ctx.author.id, from_coin)
        if from_balance < amount:
            await ctx.respond(f"❌ Insufficient {from_coin} balance ({from_balance:.8f})", ephemeral=True)
            return
        await self.bot.db.update_balance(ctx.author.id, from_coin, -amount)
        await self.bot.db.update_balance(ctx.author.id, to_coin, to_amount)
        await ctx.respond(f"🔄 Swapped {amount:.8f} {from_coin} for {to_amount:.8f} {to_coin}")

def setup(bot):
    bot.add_cog(Swap(bot))
