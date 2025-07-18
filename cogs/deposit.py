import discord
from discord.ext import commands


class Deposit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deposit")
    async def deposit(self, ctx, coin: str, amount: float):
        """Manually add coins (simulated deposit)"""
        if amount <= 0:
            await ctx.send("🚫 Amount must be positive.")
            return

        user_id = ctx.author.id
        coin = coin.upper()

        # Add to balance
        add_q = """
        INSERT INTO balances (user_id, coin, amount)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE amount = amount + %s
        """
        await self.bot.db.execute(add_q, (user_id, coin, amount, amount))

        # Log transaction
        tx_q = """
        INSERT INTO transactions (user_id, type, coin, amount)
        VALUES (%s, 'deposit', %s, %s)
        """
        await self.bot.db.execute(tx_q, (user_id, coin, amount))

        await ctx.send(f"✅ Deposited {amount:.8f} {coin} to your account.")


async def setup(bot):
    await bot.add_cog(Deposit(bot))
