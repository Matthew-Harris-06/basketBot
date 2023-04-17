from html.parser import HTMLParser
import requests



class MyHTMLParser(HTMLParser):
    startCount = False
    count =0
    rosterData = []
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        pass
    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        pass
    def handle_data(self, data):
        #print("Encountered some data  :", data)

        if(data == "Team Roster"):
            self.startCount = True
            
        #accumulator
        if(self.startCount):
            self.count+=1
        if(9 <= self.count < 148):
            self.rosterData.append(data)

    def returnRoster(self) -> list[str]:
        return self.rosterData
    
teamKeys = {
"atl":"atlanta-hawks",
"bkn":"brooklyn-nets",
"cha":"charlotte-hornets",
"chi":"chicago-bulls",
"den":"denver-nuggets",
"dal":"dallas-mavericks",
"tor":"toronto-raptors",
"cle":"cleveland-cavaliers",
"gs":"golden-state-warriors",
"det":"detroit-pistons",
"hou":"houston-rockets",
"ind":"indiana-pacers",
"lal":"los-angeles-lakers",
"mem":"memphis-grizzlies",
"lac":"la-clippers",
"mia":"miami-heat",
"mil":"milwaukee-bucks",
"min":"minnesota-timberwolves",
"no":"new-orleans-pelicans",
"ny":"new-york-knicks",
"okc":"oklahoma-city-thunder",
"orl":"orlando-magic",
"phi":"philadelphia-76ers",
"phx":"phoenix-suns",
"por":"portland-trail-blazers",
"sac":"sacramento-kings",
"san":"san-antonio-spurs",
"utah":"utah-jazz",
"wsh":"washington-wizards"
}




def formatData(data: list[str]) -> list[dict[str:str]]:
    
    players = []
    currentArray = []
    for index,data in enumerate(data):
        if(index % 8 == 0) and( index != 0):
            players.append(currentArray)
            currentArray = []
            currentArray.append(data)
        else:
            currentArray.append(data)
    playersFormatted = []
    for player in players:
        player = {
            "NAME": player[0],
            "NUM": player[1],
            "POS": player[2],
            "AGE": player[3],
            "HT": player[4],
            "WT": player[5],
            "SALARY": player[7]
        }
        playersFormatted.append(player)

    return playersFormatted

def getData(team: str) -> list[dict[str:str]]:

    data = requests.get("https://www.espn.com/nba/team/roster/_/name/{}/{}".format(team,teamKeys[team]))
    parser = MyHTMLParser()
    
    parser.feed(str(data.content))
    
    return formatData(parser.returnRoster())

