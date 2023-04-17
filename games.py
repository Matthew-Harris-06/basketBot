import requests



from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):


    games=[]
    startcount = False
    count = 0;
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        pass

    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        pass
    def handle_data(self, data):
        #print("Encountered some data  :", data)
        
        
        
        if(data == "East" or data =="West"):
            
            self.startcount = True
            
        if(self.startcount):
            self.count+=1
            self.games.append(data)

        
        if(self.count ==8):
            self.games.append("\n")
            self.startcount = False
            self.count = 0
       
def getData():
    data = requests.get('https://www.nba.com/games')
    parser = MyHTMLParser()
    parser.feed(str(data.content))
    return parseData(parser.games)

def parseData(games: list[str]):
    games = "/".join(games)
    games = games.split("\n")
    parsedGames = []
    for game in games:
        gamelist = game.split("/")
        
        while("" in gamelist):
            gamelist.remove("")
        while(" - " in gamelist):
            gamelist.remove(" - ")
        
        parsedGames.append(gamelist)
    if([] in parsedGames):
        parsedGames.remove([])
    ret = []
    for game in parsedGames:
        gameInfo = {
            "Division":game[0],
            "Round": game[1],
            "Game": game[2],
            "Team-1": game[3],
            "Time": game[4],
            "Team-2": game[6]
        }
        ret.append(gameInfo)
    return ret


