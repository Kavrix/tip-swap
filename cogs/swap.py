import discord
from discord.ext import commands


# Fixed exchange rates (mock)
EXCHANGE_RATES = {
    ("DOGE", "AUS"): 0.05,
    ("AUS", "DOGE"): 20,
    ("DOGE", "DINGO"): 1.5,
    ("DINGO", "DOGE"): 0.6667,
    ("AUS", "terraAUS"): 1.2,
    ("terraAUS", "AUS"): 0.8333
}


class Swap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="swap")
    async def swap(self, ctx, from_coin: str, to_coin: str, amount: float):
        """Swap between coins at fixed rates"""
        from_coin = from_coin.upper()
        to_coin = to_coin.upper()

        if from_coin == to_coin:
            await ctx.send("🚫 Can't swap to the same coin.")
            return

        rate = EXCHANGE_RATES.get((from_coin, to_coin))
        if rate is None:
            await ctx.send("❌ No exchange rate for that pair.")
            return

        new_amount = amount * rate
        user_id = ctx.author.id

        # Deduct from original balance
        deduct_q = "UPDATE balances SET amount = amount - %s WHERE user_id = %s AND coin = %s AND amount >= %s"
        rows = await self.bot.db.execute(deduct_q, (amount, user_id, from_coin, amount))

        if rows == 0:
            await ctx.send("❌ Insufficient funds.")
            return

        # Add to new coin balance
        add_q = "INSERT INTO balances (user_id, coin, amount) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE amount = amount + %s"
        await self.bot.db.execute(add_q, (user_id, to_coin, new_amount, new_amount))

        # Log transaction
        tx_q = "INSERT INTO transactions (user_id, type, coin, amount) VALUES (%s, 'swap', %s, %s)"
        await self.bot.db.execute(tx_q, (user_id, to_coin, new_amount))

        await ctx.send(f"🔄 Swapped {amount:.8f} {from_coin} to {new_amount:.8f} {to_coin} at rate {rate:.4f}")


async def setup(bot):
    await bot.add_cog(Swap(bot))
