import discord, random, aiohttp
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll_dice", aliases=["roll"])
    async def roll_dice(self, ctx, dice: str):
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send("Format has to be in NdN!")
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(name="flip_coin", aliases=["coin"])
    async def flip_coin(self, ctx):
        await ctx.send(random.choice(["Heads!", "Tails!"]))

    @commands.command(name="say")
    async def say(self, ctx, *, message: str):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name="fact")
    async def fact(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as r:
                data = await r.json()
                await ctx.send(data["text"])

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))