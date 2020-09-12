# bot.py
import os
import time
import discord
import asyncio
import random
from dotenv import load_dotenv
from discord.utils import find

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL= os.getenv('CHANNEL_TEST')
HEADERTEXT=os.getenv('HEADER_TEXT')

i = 0
gatherq=list() # player queue list, name-discord id pair
maxcount=6 # max players in a queue


header = 0
channel = 0



from discord.ext import commands



bot = commands.Bot(command_prefix='!')


#async def fread(MAPLIST, headerctt):  
#		 
#	for line in MAPLIST:
#		await header.edit(content=headerctt+"\n"+line)
#		headerctt=header.content



@bot.command(name='join')
async def join(ctx):
	
	global i
	global gatherq
	global header
	global channel
	global maxcount
	
	
	i +=1
	if ctx.message.author.id in gatherq:
		
		print(f'DEBUG: {ctx.message.author.name} tried to join twice')
		await ctx.message.delete()
		return
	
	
	channel=ctx.message.channel
	print(channel.id)
	print(CHANNEL)
	if (str(channel.id)!=CHANNEL):
		return
	gatherq.append(ctx.message.author.name)
	gatherq.append(ctx.message.author.id)
	await ctx.message.delete()
	print("DEBUG: QUEUE "+str(gatherq))


	
	
	header = await channel.history().get(author__name='NT-PUGBOT')
	#print(header)
	#header = await channel.fetch_message(channel.last_message_id)
	headerctt = header.content
	await header.edit(content=headerctt+"\n"+str(i)+". "+str(gatherq[(i-1)*2]))
	headerctt = header.content
	if (i==maxcount):
		slap=""
		for j in range(i):
			slap += "<@" +str(gatherq[(i-1)*2+1])+"> "
		await header.edit(content=headerctt+"\n"+"PUG STARTED PICK CAPTAINS " + slap + "\n")
	
		

		

		


		

@bot.command(name='leave')
async def leave(ctx):
	

		

	
	global i
	global gatherq
	global header
	global channel
   
	
	if (str(channel.id)!=CHANNEL):
		return
	
	if (ctx.message.author.id  not in gatherq):
		
		print(f'DEBUG: {ctx.message.author.name} tried to leave without joining')
		await ctx.message.delete()
		return	
	i -=1
	gatherq.remove(ctx.message.author.name)
	gatherq.remove(ctx.message.author.id)
	print(gatherq)
	await ctx.message.delete()
 
	headerctt=""
	if not gatherq:
		await header.edit(content=HEADERTEXT)

		return
	for j in range (i):
		headerctt+= ""+str(j)+". "+str(gatherq[(j-1)*2])+"\n"
	await header.edit(content=HEADERTEXT+"\n"+headerctt)

@bot.command(name='refresh')
async def refresh(ctx):
	
	global i
	global gatherq
	global header
	
	if (str(channel.id)!=CHANNEL):
		return
	if not gatherq:
	   
		print(f'DEBUG: {ctx.message.author.name} tried to refresh empty queue')
		await ctx.message.delete()
		return
	print(ctx.message.author.roles)
	role_names = [role.name for role in ctx.message.author.roles]
	if ("PUGAdmin" in role_names)or("PUGMod" in role_names)or("Puggers" in role_names):

		gatherq=list()
		i=0
		deleted = await channel.purge(limit=100, check=None)
		await channel.send(HEADERTEXT)
		print("DEBUG: Gather got refreshed")
	else:
		print("DEBUG: No sufficient rights for " + ctx.message.author.name)
	

@bot.command(name='kick')
async def kick(ctx, arg):
	if (str(channel.id)!=CHANNEL):
		return
	print (arg)
	arg=int(arg[3:len(arg)-1])
	print (arg)
	global i
	global gatherq
	global header
	await ctx.message.delete()
	role_names = [role.name for role in ctx.message.author.roles]
	if not ("PUGAdmin" in role_names)and not ("PUGMod" in role_names):
		print("DEBUG: No sufficient rights for " + ctx.message.author.name)
		await ctx.message.delete()
		return

	
	if not gatherq:
		print(f'DEBUG :{ctx.message.author.name} tried kicking from an empty queue')
		return
	if arg not in gatherq:
		return
	else:
		i -= 1
		
		print (arg)
		q = gatherq.index(arg)
		name = gatherq.pop(q-1)
		gatherq.pop(q-1)
		print("DEBUG: Player " + name+ " was kicked off the queue")
		print(gatherq)
	headerctt=""
	if not gatherq:
		await header.edit(content=HEADERTEXT)

		return
	for j in range (i):
		headerctt+= ""+str(j)+". "+str(gatherq[(j-1)*2])+"\n"
	await header.edit(content=HEADERTEXT+"\n"+headerctt)
	await ctx.message.delete()

@bot.command(name='pugmode')
async def pugmode(ctx):
	global i
	global gatherq
	global header
	global channel
	global maxcount
	if (str(channel.id)!=CHANNEL):
		return
	
	
	
	await ctx.message.delete()
	role_names = [role.name for role in ctx.message.author.roles]
	if not ("Admin" in role_names)and not ("Moderator" in role_names):
		print("DEBUG: No sufficient rights for " + ctx.message.author.name)
		await ctx.message.delete()
		return
	elif (maxcount==6):
		maxcount = 10
		await header.remove_reaction("3⃣",bot.user)
		await header.add_reaction("5️⃣")
	else:
		maxcount = 6
		await header.remove_reaction("5️⃣",bot.user)
		await header.add_reaction("3⃣")


	

	
	


@bot.event
async def on_ready():
	global header
	global channel
	print(f'{bot.user.name} has connected to Discord!')
	for guild in bot.guilds:
		print(f'{bot.user.name} is connected to {guild.name}')
		for channel in guild.channels:
			if channel.id==int(CHANNEL):
				deleted = await channel.purge(limit=100, check=None)
				await channel.send(HEADERTEXT)
				header = await channel.history().get(author__name='NT-PUGBOT')
				await header.add_reaction("3⃣")
 



	

bot.run(TOKEN)


