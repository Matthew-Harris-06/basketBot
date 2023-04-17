import requests
from html.parser import HTMLParser

d = requests.get("https://www.nba.com/stats")


class myHTMLParser(HTMLParser):
    my_s=""
    lasttag = ""
    my_pointsinfo = []
    my_reboundsinfo =[]
    my_assistsinfo = []
    my_blocksinfo = []
    my_stealsinfo =[]
    my_turnoversinfo = []
    my_threesmadeinfo =[]
    my_freethrowsinfo = []
    

    p_capture = False
    r_capture = False
    a_capture = False
    b_capture = False
    s_capture = False
    t_capture = False
    th_capture = False
    ft_capture = False

    my_caller = {"Points": p_capture, "Rebounds": r_capture, "Assists": a_capture, "Blocks": b_capture,"Steals":s_capture,"Turnovers":t_capture,"Three Pointers Made": th_capture,"Free Throws Made": ft_capture}
    totalStats = [my_pointsinfo,my_reboundsinfo,my_assistsinfo,my_blocksinfo,my_stealsinfo,my_turnoversinfo,my_threesmadeinfo,my_freethrowsinfo]
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        
        self.lasttag = tag   
    
              

        return tag
    
    def handle_endtag(self, tag: str) -> None:
        if(tag == "table"):
            
            return ("TABLE END")
        return tag
    def handle_data(self, data: str) -> None:
        
        
        if(data in self.my_caller):
            
            self.my_caller[data] = True                
            
        
        if(self.my_caller["Points"] == True and len(self.my_pointsinfo) < 26):
            self.my_pointsinfo.append(data)
        

        if(self.my_caller["Rebounds"] == True and len(self.my_reboundsinfo) < 26):
            self.my_reboundsinfo.append(data)
        
        if(self.my_caller["Assists"] == True and len(self.my_assistsinfo) < 26):
            self.my_assistsinfo.append(data)
        

        if(self.my_caller["Blocks"] == True and len(self.my_blocksinfo) < 26):
            self.my_blocksinfo.append(data)

        if(self.my_caller["Steals"] == True and len(self.my_stealsinfo) < 26):
            self.my_stealsinfo.append(data)
        

        if(self.my_caller["Turnovers"] == True and len(self.my_turnoversinfo) < 26):
            self.my_turnoversinfo.append(data)

        if(self.my_caller["Three Pointers Made"] == True and len(self.my_threesmadeinfo) < 26):
            self.my_threesmadeinfo.append(data)
        
        if(self.my_caller["Free Throws Made"] == True and len(self.my_freethrowsinfo) < 26):
            self.my_freethrowsinfo.append(data)
        

       
        return data
   
        

def furtherParse(allStats: list[list[str]]) -> list[tuple]:
    leaders = []
    totalScores=[]
    for category in allStats:
        #print(category)
        for items in category:
            if(items not in [str(i) for i in range(5)] and items !=". " and not items.isdigit() and len(items) > 3):
                leaders.append(items)
    for category in allStats:
        
        pfiltered = [x for x in category if( x not in leaders and x != ". " and not x.isalpha())]
        placemenets = []
        scores = []
        for index,num in enumerate(pfiltered):
            if(index % 2):
                scores.append(num)
            else:
                placemenets.append(num)
                
        #print(pfiltered)
        #print(placemenets)
        #print(scores)
        totalScores.append(scores)
    formattedScores = []
    leadercategories = ["Points","Rebounds","Assists","Blocks","Steals","Turnovers","Three Pointers Made","Free Throws Made"]
    for x in leadercategories:
        formattedScores.append({x:[]})

    justLeaders = [x for x in leaders if x not in leadercategories]

    players = []
    for index, player in enumerate(justLeaders):
        #print(index)    
        #print(player)
        #print("in Array Position",index % 5)
        #print("In the ", (index // 5), "'th array or the ",leadercategories[index // 5], " Array")
        #print(totalScores[index//5][index % 5])
        players.append({player: totalScores[index//5][index % 5]})
    
    #print(totalScores)
    
    splitResults = [("Points",[]),("Rebounds",[]),("Assists",[]),("Blocks",[]),("Steals",[]),("Turnovers",[]),("Three Pointers Made",[]),("Free Throws Made",[])]
    for index, entry in enumerate(players):
        
        splitResults[index//5][1].append(entry)
    #print("       NBA DAILY LEADERBOARD")
    #for category in splitResults:
        #print("-------", category[0],"'s Leaderboard -----")
        #for player in category[1]:
            #print(str(player).replace("{","").replace("}","").replace("'",""))
    
    return splitResults 
   
   
def getData() -> list[tuple[str,list]]:


    my_parser = myHTMLParser()
    my_parser.feed(str(d.content))

    return furtherParse(my_parser.totalStats)
#print(my_parser.my_s)