import discord, asyncio
from discord.ext import commands
import json, random;from typing import Literal, Optional

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("data\economy.json", "r") as f:
            self.economy_data = json.load(f)
        with open("data\shop.json", "r") as f:
            self.items = json.load(f)
            
    async def cog_check(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in self.economy_data:
            if ctx.message.content == "!login":
                return True
            else:
                await ctx.send("You need to join first before you can use economy commands!")
                return False
        return True
        
    @commands.command(name="login", help="Join the economy system and get a starting balance of 100 credits")
    async def join_economy(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in self.economy_data:
            self.economy_data[user_id] = {"balance": 100}
            with open("data\economy.json", "w") as f:
                json.dump(self.economy_data, f, indent=4)
            await ctx.send(f"Welcome to the economy system! You have been given a starting balance of 100 credits.")
        else:
            await ctx.send("You have already joined the economy system!")

    @commands.command(name="addcredits", aliases=["add"])
    @commands.has_permissions(administrator=True)
    async def add_credits(self, ctx, amount: int, user: discord.Member = None):
        if user is None:
            user = ctx.author
        user_id = str(user.id)
        if user_id not in self.economy_data:
            self.economy_data[user_id] = {"balance": 0}
        self.economy_data[user_id]["balance"] += amount
        with open("data\economy.json", "w") as f:
            json.dump(self.economy_data, f, indent=4)
        await ctx.send(f"{amount} credits added to {user.display_name}'s account.")

    @commands.command(name="shop")
    async def show_items(self, ctx):
        items_list = "\n".join([f"{item}: {price} credits" for item, price in self.items.items()])
        embed = discord.Embed(title="Shop", description=items_list, color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name="buy")
    async def buy_item(self, ctx, amount: int=1, *, item: str):
        user_id = str(ctx.author.id)
        if user_id not in self.economy_data:
            self.economy_data[user_id] = {"balance": 0}
        if item not in self.items:
            await ctx.send(f"{item} is not available for purchase.")
            return
        price = self.items[item] * amount
        if self.economy_data[user_id]["balance"] < price:
            await ctx.send("You do not have enough credits to purchase this item.")
            return
        self.economy_data[user_id]["balance"] -= price
        with open("data\economy.json", "w") as f:
            json.dump(self.economy_data, f)

        if item == "lottery ticket":
            await self._lottery(ctx, user_id, amount)
        elif item == "bank note":
            await self._bank(ctx, user_id, amount)
        else:
            await ctx.send(f"You have purchased {amount} {item}(s) for {price} credits.")

    async def _lottery(self, ctx, user_id, amount):
        results = []
        for i in range(amount):
            lottery_numbers = [random.randint(1, 10) for i in range(3)]
            results.append(lottery_numbers)
        results_str = "\n".join([f"{i+1}. {numbers}" for i, numbers in enumerate(results)])
        await ctx.send(f"Your lottery numbers are:\n{results_str}")
        winnings = sum([1000 if len(set(numbers)) == 1 else 0 for numbers in results])
        if winnings > 0:
            self.economy_data[user_id]["balance"] += winnings
            await ctx.send(f"Congratulations, you won a total of {winnings} credits!")
        else:
            await ctx.send("Better luck next time!")

    async def _bank(self, ctx, user_id, amount):
        bank_balance = random.randint(1000, 10000)
        self.economy_data[user_id]["balance"] += bank_balance * amount
        await ctx.send(f"Your bank balance increase {bank_balance * amount} credits.")

    @commands.command(name="balance", aliases=["bal"])
    async def view_balance(self, ctx, member: Optional[discord.Member] = None):
        user_id = str(ctx.author.id) if member is None else str(member.id)
        if user_id not in self.economy_data:
            self.economy_data[user_id] = {"balance": 0}
        balance = self.economy_data[user_id]["balance"]
        await ctx.send(f"{member.display_name if member else 'You'} have {balance} credits.")

    @commands.command(name="leaderboard", aliases=["lb"])
    async def view_leaderboard(self, ctx):
        sorted_users = sorted(
            self.economy_data.items(), key=lambda x: x[1]["balance"], reverse=True
        )
        top_users = sorted_users[:10]
        leaderboard = "```css\n"
        for user in top_users:
            member = ctx.guild.get_member(int(user[0]))
            if member is not None:
                leaderboard += f"{member.display_name: <20} {user[1]['balance']: >5}\n"
        leaderboard += "```"
        await ctx.send(f"Top 10 users by balance:\n{leaderboard}")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))