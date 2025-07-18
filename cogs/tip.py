import discord
from discord.ext import commands


class Tip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tip")
    async def tip(self, ctx, member: discord.Member, coin: str, amount: float):
        """Tip another user some coins"""
        sender_id = ctx.author.id
        receiver_id = member.id

        if amount <= 0:
            await ctx.send("🚫 Amount must be positive.")
            return

        # Deduct from sender
        deduct_q = "UPDATE balances SET amount = amount - %s WHERE user_id = %s AND coin = %s AND amount >= %s"
        rows = await self.bot.db.execute(deduct_q, (amount, sender_id, coin.upper(), amount))

        if rows == 0:
            await ctx.send("❌ Insufficient funds.")
            return

        # Add to receiver
        add_q = "INSERT INTO balances (user_id, coin, amount) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE amount = amount + %s"
        await self.bot.db.execute(add_q, (receiver_id, coin.upper(), amount, amount))

        # Log transaction
        tx_q = "INSERT INTO transactions (user_id, type, coin, amount, target_user_id) VALUES (%s, 'tip', %s, %s, %s)"
        await self.bot.db.execute(tx_q, (sender_id, coin.upper(), amount, receiver_id))

        await ctx.send(f"✅ {ctx.author.mention} tipped {amount:.8f} {coin.upper()} to {member.mention}.")


async def setup(bot):
    await bot.add_cog(Tip(bot))
