import discord, re
from discord.ext import commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member} has been banned from the server.")

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked from the server.")

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute_member(self, ctx, member: discord.Member, *, reason=None):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)

        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"{member} has been muted.")

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute_member(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            await ctx.send("There is no Muted role.")
            return

        await member.remove_roles(muted_role)
        await ctx.send(f"{member} has been unmuted.")

    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge_messages(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit+1)
        await ctx.send(f"{limit} messages have been deleted.")

    @commands.command(name="warn")
    @commands.has_permissions(kick_members=True)
    async def warn_member(self, ctx, member: discord.Member, *, reason=None):
        warn_role = discord.utils.get(ctx.guild.roles, name="Warned")
        if not warn_role:
            warn_role = await ctx.guild.create_role(name="Warned")

        await member.add_roles(warn_role, reason=reason)
        await ctx.send(f"{member} has been warned.")
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def membercount(self, ctx):
        guilds = self.bot.guilds
    
        if len(guilds) == 1:
            guild = guilds[0]
        else:
            guild_names = [g.name for g in guilds]
            embed = discord.Embed(title="Select a guild", description="React to select a guild:")
            embed.add_field(name="Guilds", value="\n".join(guild_names), inline=False)
            
            msg = await ctx.send(embed=embed)
        
            for i in range(len(guilds)):
                await msg.add_reaction(chr(127462 + i))
            
            reaction, user = await self.bot.wait_for('reaction_add', check=lambda r, u: u == ctx.author and r.message == msg)
          
            index = ord(reaction.emoji) - 127462
            guild = guilds[index]

            for reaction in msg.reactions:
                await reaction.remove(ctx.author)
        
        member_count = guild.member_count
        channel_regex = re.compile(r'member-count-\d+')
        channel = discord.utils.find(lambda c: channel_regex.match(c.name), guild.channels)
        if not channel:
            category = discord.utils.get(guild.categories, name='General')
            channel = await guild.create_text_channel('member count:', category=category)

        await channel.edit(name=f"member count: {member_count}")
        await ctx.send(f"Member count channel updated for {guild.name}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Utils(bot))