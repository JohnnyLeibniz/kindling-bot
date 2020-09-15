import os
import discord
import pip
import time
import discord.client
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from itertools import cycle
import random

load_dotenv()
GUILD = os.getenv('The Forge') #Confirming the name of my chosen server, if we want it for something specific.
client = commands.Bot(command_prefix = ">") #This bot uses > to do commands.

token = 'NzU0NDc4NzA3NDE4MDcxMDQx.X11VDQ.WgvrENgVDZuV7rLWqjjYT96BF4w'

#-----------
# ON READY
#-----------

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game('with matches.'))
    change_status.start()
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

#-----------------
# CHECKS
#-----------------

def creator_check(ctx):
    return ctx.author.id == 402231397445664779

#---------
# SET UP
#---------

@client.command()
@commands.check(creator_check)
async def startkindling(ctx): #create the channel used for most unique bot commands. Not yet fully functional.
    guild = ctx.guild
    channel = discord.utils.get(guild.text_channels, name='the-bonfire')
    if channel is None:
        channel = await ctx.guild.create_text_channel('the-bonfire')
        channel = discord.utils.get(guild.text_channels, name='the-bonfire')
        channelID = discord.abc.GuildChannel.mention(channel)
        await ctx.send("f'The bonfire has been lit - :fire: **KINDLING** :fire: is ready for use on this server! Please check the new {channel.mention} channel for more information.'")
    else: 
        await ctx.send(f'The bonfire has already been lit.')

client.remove_command('help')
@client.command()
async def help(ctx): #prettier version of help? Maybe later.
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )
    embed.set_author(name = '━━━━━━━━━\n ━━━ HELP ━━━\n━━━━━━━━━')
    embed.add_field(name = '>startkindling',value = 'Start the bot. Only usable by bot author (Johnny)', inline=False)
    embed.add_field(name = '>ping',value = 'Return current bot latency', inline=False)
    embed.add_field(name = '>clear #',value = 'Clear messages from current channel, where # = number of messages you wish to delete', inline=False)
    embed.add_field(name = '>kick @user',value = 'Kicks the chosen user', inline=False)
    embed.add_field(name = '>ban @user',value = 'Bans the chosen user', inline=False)
    embed.add_field(name = '>unban user',value = 'Unbans the user. Note that mentions are not necessary', inline=False)
    embed.add_field(name = '>ruhacks',value = 'Gives info about RU Hacks', inline=False)

    await ctx.send(embed=embed)
    
#------
# COGS
#------

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        
#-------
# TASKS
#-------
botStatus = cycle(['with matches','with fire'])

@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity = discord.Game(next(botStatus)))

#------------------
# RANDOM COMMANDS  
#------------------

@client.command() #Find the current latency of the bot
async def ping(ctx):
    await ctx.send(f'Bot ping is {round(client.latency * 1000)} ms') #latency in milliseconds

@client.command() #clear a channels messages.
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount = 1): #default 1 message if not specified
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f'**[ {amount} ] messages have been deleted.**')
    time.sleep(2) #5 second delay for message above.
    await ctx.channel.purge(limit=1)

@client.command()
async def ruhacks(ctx):
    embed=discord.Embed(title="RU Hacks", url="https://www.ruhacks.com", color=0xf440ff)
    embed.set_author(name="Ryerson's Official Hackathon")
    embed.set_thumbnail(url="https://www.ruhacks.com/images/RU_White_RU.png")
    embed.add_field(name="LinkTree: ", value="https://linktr.ee/ruhacks", inline=False)
    await ctx.send(embed=embed)

@client.command(aliases=['ash','ashes'])
async def _8ash(ctx):
    responses = ['It burns',
                 'We burn',
                 'I am burning',
                 'Burn away',
                 'Burn, baby, burn']
    await ctx.send(f'{random.choice(responses)}')

#----------------
# REACTION ROLES
#----------------

@client.event
async def on_raw_react_add(payload): #NOT WORKING YET
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id,client.guilds)
    if payload.emoji.name == 'twig':
        role = discord.utils.get(guild.roles,name='one')
    elif payload.emoji.name == 'branch':
        role = discord.utils.get(guild.roles,name='two')
    else: 
        role = discord.utils.get(guild.roles,name = payload.emoji.name)
    
    if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user.id,guild.members)
        if member is not None:
            await member.add_roles(role)
            print ("Role added")
        else:
            print ("Member not found")
    else: 
        print ("Role not found")

@client.event
async def on_raw_react_remove(payload):
    pass

#-------------
# VOICE
#-------------

@client.command()
async def joinvoice(ctx):
    connected = ctx.author.voice
    if connected:
        await connected.channel.connect()
        
@client.command(pass_context=True)
async def leavevoice(ctx):
    connected = ctx.author.voice
    if connected:
        await connected.channel.disconnect()

#-------------
# ON MESSAGE
#-------------

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user:
        return

    if message.content == 'hot?':
        response = 'It is hot.'
        await message.channel.send(response)
    
    if message.content == 'ah' or message.content == 'Ah':
        response = 'Ahh.'
        await message.channel.send(response)
        
    if message.content == 'ahh' or message.content == 'Ahh':
        response = 'Ahhh.'
        await message.channel.send(response)
        
    if message.content == 'ahhh' or message.content == 'Ahhh':
        response = 'AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH'
        await message.channel.send(response)
    
#-----------------
# ERROR HANDLING
#-----------------
 
@client.event      
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('You did not use a valid command.')
        
@load.error        
async def load_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please state the specific cog you would like to load.')

@unload.error        
async def unload_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please state the specific cog you would like to unload.')

#Run the client
client.run(token)