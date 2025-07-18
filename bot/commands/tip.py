import discord
from discord.ext import commands

class Tip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="tip", description="Tip a user some coins")
    async def tip(self, ctx, member: discord.Member, coin: str, amount: float):
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
        await self.bot.db.update_balance(ctx.author.id, coin, -amount)
        await self.bot.db.update_balance(member.id, coin, amount)
        await ctx.respond(f"💸 {ctx.author.mention} tipped {amount:.8f} {coin} to {member.mention}")

def setup(bot):
    bot.add_cog(Tip(bot))
