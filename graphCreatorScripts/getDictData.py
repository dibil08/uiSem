import networkx as nx
import pickle
import pandas as pd 
import csv
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
data = pd.read_csv("./data/steam-200k.csv") 
gameData = pd.read_csv("./data/gameInfo/steam.csv") 
print(data.head())
game_title=set()
print(data.gameTitle)
for game in data.gameTitle:
    game_title.add(game)
print(len(game_title))
gameIds=dict()
i=0

na=[]
idToGame=dict()
gameToId=dict()
for gameTitle in game_title:
    flag=False
    game=gameTitle.lower().replace(":","").replace("®","")
    for tuple in list(zip(gameData.appid, gameData.name)):
        if similar(tuple[1].lower().replace(":","").replace("®",""),game)>0.8:
            if(tuple[1].lower().replace(":","").replace("®","").split(" ")[-1]==game.split(" ")[-1]):
                flag=True
                i+=1
                idToGame[tuple[0]]=gameTitle
                gameToId[gameTitle]=int(tuple[0])
                break
    if i%100==0:
        print("{}%".format(i/len(game_title)*100))
    if not flag:
        na.append(gameTitle)
a_file = open("./data/idToGame.pkl", "wb")
pickle.dump(idToGame, a_file)
a_file.close()
a_file = open("./data/gameToId.pkl", "wb")
pickle.dump(gameToId, a_file)
a_file.close()

data[['gameId']] = data['gameTitle'].map(gameToId)
print(data)
data.to_csv("./data/steamWithIds-200k.csv")

data=data.dropna()
data.to_csv("./data/noNAsteamWithIds-200k.csv")

print(na)
print(len(na))