import cassiopeia as cass
from cassiopeia import Summoner 
import csv
import collections
import pandas as pd
import random
with open("api_key.txt","r") as f:
    api_key=f.read()


# cass.set_riot_api_key(api_key)


settings = cass.get_default_config()
settings["pipeline"]["RiotAPI"]["api_key"]=api_key
settings["logging"]["print_calls"]=False
cass.apply_settings(settings)
cass.set_default_region("EUW")

dfSoFar = pd.read_csv("championMasteries.csv")
seenSummoners=set(dfSoFar["summoner"])

seedName = dfSoFar["summoner"].tolist()[-1]
summoner_seed = cass.get_summoner(name=seedName,region="EUW")
column_labels = ["summoner"] + [cm.champion.name for cm in summoner_seed.champion_masteries]

dataDict={}
summonerDataCalls = 0





def get_summoner_data(summoner):  #Not used due to python reccursion limit and uncertainty of stack frames if removing limit
    global summonerDataCalls
    global dataCSVWriter
    summonerDataCalls+=1
    
   
    if summonerDataCalls>10000:
        return
    if summonerDataCalls % 100 == 0:
        print(f"Call with counter: {summonerDataCalls}")
    currentName=summoner.name
    seenSummoners.add(currentName)
    # dataDict[current_name] = [cm.points for cm in summoner.champion_masteries]
    dataCSVWriter.writerow(  [currentName] + [cm.points for cm in summoner.champion_masteries])
    for match in summoner.match_history:
        for participant in match.participants:
            summonerFromHist = participant.summoner
            summonerFromHistName = summonerFromHist.name
            if not summonerFromHistName in seenSummoners:  #make sure not taking duplicate summoners
                get_summoner_data(summonerFromHist)


summonersDeque = collections.deque([summoner_seed])   
def nonRecursiveSummonerData(summoner):
    global summonersDeque
    global dataCSVWriter
    global summonerDataCalls

    summonerDataCalls+=1
    

    if summonerDataCalls % 100 == 0:
        print(f"Call with counter: {summonerDataCalls}")
    currentName=summoner.name
    seenSummoners.add(currentName)
    # dataDict[current_name] = [cm.points for cm in summoner.champion_masteries]
    
    for match in summoner.match_history:
        for participant in match.participants:
            summonerFromHist = participant.summoner
            summonerFromHistName = summonerFromHist.name
            if not summonerFromHistName in seenSummoners:  #make sure not taking duplicate summoners
                seenSummoners.add(summonerFromHistName)
                dataCSVWriter.writerow(  [summonerFromHistName] + [cm.points for cm in summonerFromHist.champion_masteries])
                summonersDeque.append(summonerFromHist)


with open('championMasteries2.csv', mode='w',encoding="utf-8",newline='') as dataCSV:
    dataCSVWriter = csv.writer(dataCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    dataCSVWriter.writerow(column_labels)

    # get_summoner_data(summoner_seed)
    # for summoner in summonersDeque:
    #     print(summoner.name)
    #     nonRecursiveSummonerData(summoner)
    

    summoner=summoner_seed
    while True:
        print(summoner.name)
      
        nextMatchSeed= random.randint(0,len(summoner.match_history))
        nextParticipantSeed = random.randint(0,9)
        for index,match  in enumerate(summoner.match_history):
            
            if index == nextMatchSeed:
                summoner=match.participants[nextParticipantSeed].summoner #get summoner for next run
              
            for participant in match.participants:
                summonerFromHist = participant.summoner
                summonerFromHistName = summonerFromHist.name
            
                if not summonerFromHistName in seenSummoners:  #make sure not taking duplicate summoners
                    seenSummoners.add(summonerFromHistName)
                    try:
                        dataCSVWriter.writerow(  [summonerFromHistName] + [cm.points for cm in summonerFromHist.champion_masteries])
                    except:
                        print(f"Failed to write to csv for summoner {summonerFromHistName}") #rare api call fails for some summoners
                   
print("done")
