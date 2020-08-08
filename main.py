import cassiopeia as cass
from cassiopeia import Summoner 
import csv
import collections
import pandas as pd
import random
with open("api_key.txt","r") as f:
    api_key=f.read()


class matchData:
    def __init__(self,match):
        self.match=match
        self.participants = self.match.participants
        self.summonerData=[summonerData(x.summoner) for x in self.participants]


class summonerData:
    cachedSummonerNames=set()
    def __init__(self,summoner):
        if not summoner.name in cachedSummonerNames:
            cachedSummonerNames.add(summoner.name)
        self.summoner=summoner
        self.league_entry= cass.get_league_entries(self.summoner)[0].to_dict()
        assert(self.league_entry)["queue"]=="RANKED_SOLO_5x5"
        self.winrate = self.league_entry["wins"]/(self.league_entry["wins"]+self.league_entry["losses"])
        self.hotstreak=self.league_entry["hotstreak"]
        self.tier=self.league_entry["tier"]
        self.division=self.league_entry["division"]
        self.championMasteries = [cm.points for cm in self.summoner.champion_masteries]

#settings

settings = cass.get_default_config()
settings["pipeline"]["RiotAPI"]["api_key"]=api_key
settings["logging"]["print_calls"]=False
cass.apply_settings(settings)
cass.set_default_region("EUW")


#use previously collected data to avoid duplicates
dfSoFar = pd.read_csv("mainData.csv")
seenSummoners=set(dfSoFar["summoner"])

seedName = dfSoFar["summoner"].iloc[-1]

summoner_seed = cass.get_summoner(name=seedName,region="EUW")



#sort alphabetically for column labels
try:
    columnLabels = [cm.champion.name for cm in summoner_seed.champion_masteries]
except: 
    seedName = dfSoFar["summoner"].iloc[-2]
    summoner_seed = cass.get_summoner(name=seedName,region="EUW")
    columnLabels = [cm.champion.name for cm in summoner_seed.champion_masteries]
columnLabels = sorted(columnLabels)
columnLabels.insert(0,"summoner")



with open('championMasteries2.csv', mode='w',encoding="utf-8",newline='') as dataCSV:
    dataCSVWriter = csv.writer(dataCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    dataCSVWriter.writerow(columnLabels)


    summoner=summoner_seed
    while True:
        print(summoner.name)
        
        nextMatchSeed= 1
        nextParticipantSeed = random.randint(0,5)
        for index,match  in enumerate(summoner.match_history):


            try:
                participants = match.participants
            except:
                continue
   
             

            
            for participant in participants:
           
                summonerFromHist = participant.summoner
                summonerFromHistName = summonerFromHist.name
            
                if not summonerFromHistName in seenSummoners:  #make sure not taking duplicate summoners
                    seenSummoners.add(summonerFromHistName)
                    try:
                        sortedMasteries= sorted(summonerFromHist.champion_masteries,key = lambda x: x.champion.name)
                        sortedPoints = [cm.points for cm in sortedMasteries]
                    except:
                        continue
                    csvRow = sortedPoints
                    csvRow.insert(0,summonerFromHistName)
                    try:
                        dataCSVWriter.writerow(csvRow)
                    except:
                        print(f"Failed to write to csv for summoner {summonerFromHistName}") #rare api call fails for some summoners
            summoner = participants[-1].summoner     #get summoner for next run
                   
print("done")
