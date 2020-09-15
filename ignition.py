import discord as d
from discord.ext import commands

class Lighter(commands.Cog):
    
    def _init_(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('(Ignition) log is ready.')

#-----------
# IGNITION  
#-----------
    @commands.command() #burn a channel down #NOT WORKING YET
    async def burn(self,ctx, channel: d.channel):
        mbed = d.Embed(
            title = 'Channel Burned',
            description = f'Channel:{channel} has been reduced to ashes..'
            )
        if ctx.author.guild_permissions.manage_channels():
            await ctx.send(embed=mbed)
            await channel.delete()
                       
    @commands.command() #ignite a member of the server
    async def ignite(self,ctx):
        await ctx.send('A branch has been added to the fire.')

#-------
# SETUP  
#-------
    
def setup(client): 
    client.add_cog(Lighter(client))