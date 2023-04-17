
import discord
import nbaLeaders
import os;





intents = discord.Intents.default()
intents.message_content = True






client = discord.Client(intents=None)

@client.event
async def on_ready():
    
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        
        return
    
    if message.content.startswith('$hello'):
        data = nbaLeaders.getData()
        ret = "-----DAILY LEADERS-----"+ "\n"
        for item in data: 
            ret += "-----"+item[0]+"-----" + "\n"
            for player in item[1]:
                ret += list(player.keys())[0]  + " : " + player.get(list(player.keys())[0]) +"\n"
                
        await message.channel.send(ret)

    

client.run(os.environ["DISCKEY"])