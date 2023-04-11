import discord, random, asyncio
from discord.ext import commands

class Authenticator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.challenges = {}
        self.attempts = {}

    @commands.command(name="verify")
    async def verify_user(self, ctx):
        user_id = str(ctx.author.id)
        challenge = random.randint(1000, 9999)
        self.challenges[user_id] = challenge
        self.attempts[user_id] = 0
        await ctx.send(f"Please solve the challenge: {challenge}")
        
        def check(msg):
            return msg.author.id == ctx.author.id and msg.content.isdigit()

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            del self.challenges[user_id]
            del self.attempts[user_id]
            return await ctx.send("You didn't solve the challenge in time. Please try again.")

        if int(msg.content) == challenge:
            del self.challenges[user_id]
            del self.attempts[user_id]
            await ctx.send("You have successfully verified your account!")
            role = discord.utils.get(ctx.guild.roles, name="Verified")
            await ctx.author.add_roles(role)
        else:
            self.attempts[user_id] += 1
            attempts_left = 3 - self.attempts[user_id]
            if attempts_left == 0:
                del self.challenges[user_id]
                del self.attempts[user_id]
                await ctx.send("You have exceeded the maximum number of attempts. Please try again later.")
            else:
                await ctx.send(f"The challenge you entered is incorrect. Please try again. You have {attempts_left} attempts left.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Authenticator(bot))