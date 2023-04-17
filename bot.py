
import discord
import nbaLeaders
import dailylineups
import rosters
import games
import os
import time





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
    if message.content.startswith("$getCommands"):
        ret = """ 

        $daily -> returns Daily NBA Stats
        $teamRoster (SYM) -> returns Team Roster Information for Symbol
        $symbols -> Returns a list of Team Symbols
        $games -> Returns a list of Games playing Today
        $lineups -> Returns all Daily Lineups for Today

        """
        await message.channel.send(ret)
    if message.content.startswith("$symbols"):
        ret = ""
        for team in list(rosters.teamKeys.keys()):
            ret += team + " : "  + rosters.teamKeys[team] + "\n"

        await message.channel.send(ret)
        
    if message.content.startswith('$daily'):
        data = nbaLeaders.getData()
        ret = "-----DAILY LEADERS-----"+ "\n"
        for item in data: 
            ret += "-----"+item[0]+"-----" + "\n"
            for player in item[1]:
                ret += list(player.keys())[0]  + " : " + player.get(list(player.keys())[0]) +"\n"
                
        await message.channel.send(ret)

    
    if message.content.startswith('$teamRoster'):
        #I really hope nobody sees this
        team = []
        rep1 = ""
        rep2 = ""
        

        team.append(message.content[-3])
        team.append(message.content[-2])
        team.append(message.content[-1])    
        team = "".join(team)
        team = team.lstrip()  
        ##################################

        data = rosters.getData(team)
        print(data)
        #print(message.content)
        ret = "----TEAM ROSTER {}---- \n".format(team)
        for player in data:
            playerstr = ""
            keys = player.keys()
            values = list(player.values())
            for index, field in enumerate(keys):
                playerstr += field + " : " + values[index] + " \n"

            ret += playerstr
        lines = ret.split("\n")
        rep1 = lines[0:len(lines)//2]
        rep2 = lines[len(lines)//2: len(lines)]
        #print(rep1)
        #print(rep2)
        rep1= "\n".join(rep1)
        rep2 = "\n".join(rep2)
        await message.channel.send(rep1)
        
        await message.channel.send(rep2)
    if message.content.startswith("$games"):

        data = games.getData()
        sendgames = ""
        for game in data:
            sendgames += "Division: {} \n Round: {} \n Game: {}\n {} vs {} \n  {} \n".format(game["Division"],game["Round"],game["Game"],game["Team-1"],game["Team-2"],game["Time"])
        await message.channel.send(sendgames)
    if message.content.startswith("$lineups"):
        data = dailylineups.getData()
        
        await message.channel.send(data)
client.run(os.environ["DISCKEY"])