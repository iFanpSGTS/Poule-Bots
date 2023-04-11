import os
import discord
from discord.ext import commands
from config import bot_token

TOKEN = bot_token

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command("help")

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully loaded {extension} cog")

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully unloaded {extension} cog")

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully reloaded {extension} cog")

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"iFanpS - Owner"),
    )
    for root, _, files in os.walk("commands"):
        for file in files:
            if file.endswith(".py"):
                await bot.load_extension(root.replace("\\", ".") + "." + file[:-3])
    print(f"{bot.user.name} is connected to the following guilds:")
    for guild in bot.guilds:
        print(f"- {guild.name}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Commands not found -> !help")
    elif isinstance(error, commands.errors.CheckFailure):
        return
    print(f"Error: {error}")
    
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="List of available commands:", color=0x00ff00)
    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)
    await ctx.send(embed=embed)

bot.run(TOKEN)
