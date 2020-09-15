import discord
from discord.ext import  commands

class Add_Remove(commands.Cog):
    
    def _init_(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('(Add & Remove) log is ready.')
    
    @commands.command()
    async def addbranch(self,ctx):
        await ctx.send('A branch has been added to the fire.')

        #----------------------------
        # KICKING/BANNING/UNBANNING    
        #----------------------------

    @commands.command()
    async def kick(self,ctx, member : discord.Member, *,reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked.')
    
    @commands.command()
    async def ban(self,ctx, member : discord.Member, *,reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned.')
    
    @commands.command()
    async def unban(self,ctx,*,member):
        banned_users = await ctx.guild.bans()
        member_name,member_discriminator = member.split('#')
        
        for ban_entry in banned_users:
            user = ban_entry.user
            
            if (user.name,user.discriminator) == (member_name,member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.name}#{user.discriminator} has been unbanned.')

#-------
# SETUP  
#-------

def setup(client): 
    client.add_cog(Add_Remove(client))