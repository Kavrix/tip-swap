import discord
from discord.ext import commands
from bot.utils import format_balance

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="balance", description="Check your coin balances")
    async def balance(self, ctx):
        balances = {}
        for coin in self.bot.wallets:
            bal = await self.bot.db.get_balance(ctx.author.id, coin)
            balances[coin] = bal
        await ctx.respond(f"📊 Your balances:\n{format_balance(balances)}", ephemeral=True)

def setup(bot):
    bot.add_cog(Balance(bot))
