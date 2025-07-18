import discord
from discord.ext import commands


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx):
        """Show your current balances for all coins"""
        user_id = ctx.author.id
        query = "SELECT coin, amount FROM balances WHERE user_id = %s"
        rows = await self.bot.db.fetch(query, (user_id,))

        if not rows:
            await ctx.send("💸 You have no balances yet.")
            return

        embed = discord.Embed(title=f"{ctx.author.display_name}'s Balances")
        for coin, amount in rows:
            embed.add_field(name=coin, value=f"{amount:.8f}", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Balance(bot))
