import discord
from discord.ext import commands


class Withdraw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="withdraw")
    async def withdraw(self, ctx, coin: str, amount: float, address: str):
        """Withdraw coins to an external wallet"""
        if amount <= 0:
            await ctx.send("🚫 Amount must be positive.")
            return

        user_id = ctx.author.id
        coin = coin.upper()

        # Deduct from balance
        deduct_q = """
        UPDATE balances
        SET amount = amount - %s
        WHERE user_id = %s AND coin = %s AND amount >= %s
        """
        rows = await self.bot.db.execute(deduct_q, (amount, user_id, coin, amount))

        if rows == 0:
            await ctx.send("❌ Insufficient funds.")
            return

        # Log transaction
        tx_q = """
        INSERT INTO transactions (user_id, type, coin, amount)
        VALUES (%s, 'withdraw', %s, %s)
        """
        await self.bot.db.execute(tx_q, (user_id, coin, amount))

        # Placeholder for RPC send
        await ctx.send(f"📤 Withdrew {amount:.8f} {coin} to `{address}` (mocked).")


async def setup(bot):
    await bot.add_cog(Withdraw(bot))
