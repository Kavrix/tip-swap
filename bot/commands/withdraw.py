import discord
from discord.ext import commands

class Withdraw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="withdraw", description="Withdraw coins to an external address")
    async def withdraw(self, ctx, coin: str, amount: float, address: str):
        coin = coin.upper()
        if coin not in self.bot.wallets:
            await ctx.respond("❌ Unsupported coin.", ephemeral=True)
            return
        if amount <= 0:
            await ctx.respond("❌ Amount must be positive.", ephemeral=True)
            return
        user_balance = await self.bot.db.get_balance(ctx.author.id, coin)
        if user_balance < amount:
            await ctx.respond(f"❌ Insufficient balance ({user_balance:.8f} {coin})", ephemeral=True)
            return
        txid = self.bot.wallets[coin].send_to_address(address, amount)
        await self.bot.db.update_balance(ctx.author.id, coin, -amount)
        await ctx.respond(f"✅ Sent {amount:.8f} {coin} to `{address}`\nTransaction ID: `{txid}`")

def setup(bot):
    bot.add_cog(Withdraw(bot))
