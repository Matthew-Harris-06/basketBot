import requests
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    
    startcount = False
    count = 0
    lineups = []
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        pass

    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        pass

    def handle_data(self, data):
        
        if(data == "PG"):
            self.startcount = True
            self.count = 0
        if(self.startcount and self.count < 65):
            self.count +=1
            data = data.strip()
            if not ("\\r\\n" in data):
                
                self.lineups.append(data)
            
        
        
def parseData(data: list[str])->str:
    
    data = "NEWPLAYER".join(data)
    data = data.split("PG")
    data.remove("")
    gameString = "TODAYS LINEUPS \n"
    for index,game in enumerate(data):
        gameString += "Game {} \n".format(index +1)
        game = game.split("NEWPLAYER")
        for index,entry in enumerate(game):
            if(entry !="" and entry != "SG" and entry !="SF" and entry !="PF" and entry !="C"):
                gameString += entry + "\n"
                
    return gameString

def getData():
    data = requests.get("https://basketballmonster.com/nbalineups.aspx");
    parser = MyHTMLParser()
    parser.feed(str(data.content))
    return parseData(parser.lineups)

