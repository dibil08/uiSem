import pandas as pd
import numpy as np


def read():
    df = pd.read_csv("steamWithIds-200k.csv")
    
    # use assign to normalize player ID... note we dont have player data so can lose information about original player ID
    df = df.assign(playerId=pd.factorize(df.playerId)[0])

    # do the same for game ID but keep the original data, as we want to use the game ID later on
    y, label = pd.factorize(df.gameId)

    #label = label.values

    df = df.assign(gameId = y)
    #df = df.assign(gameId = label)

    #pred = clf.predict(test[features])
    #pred_label = label[pred]

    #print(len(label))
    #pred = clf.predict(test[features])
    #pred_label = label[pred]


    df_purchase = df.loc[(df['playerGameStatus']=='purchase')]
    play = df.loc[(df['playerGameStatus']=='play')]
    

    return(df_purchase, play)

def generate_matrix(df):
    player_id = []
    game_id = []
    for index, row in df.iterrows():
        player_id.append(row["playerId"])
        game_id.append(row["gameId"])
    
    #print(min(player_id))
    #print(max(player_id))

    #print(len(player_id))

    #print(min(game_id))
    #print(max(game_id))

    R = np.zeros((max(player_id)+1, max(game_id)+1))
    #print(R)

    player_game = list(zip(player_id, game_id))

    for pair in player_game:
        #print(pair)
        R[pair[0]][pair[1]] = 1
    return(R)


#P is diagonal of RRT
def useruser(ratings):
    user_similarity_nonnormalised = np.matmul(ratings, ratings.T)
    P = np.zeros((len(user_similarity_nonnormalised), len(user_similarity_nonnormalised)), int)
    np.fill_diagonal(P, np.diag(user_similarity_nonnormalised))
    
    #recommendation matrix gamma
    gamma = (np.divide(1,np.sqrt(P), where=P!=0)) @ user_similarity_nonnormalised @ (np.divide(1,np.sqrt(P), where=P!=0)) @ ratings 

    print(gamma)



#Q is diagonal of RTR
def itemitem(ratings):
    item_similarity_nonnormalised = np.matmul(ratings.T, ratings)
    Q = np.zeros((len(item_similarity_nonnormalised), len(item_similarity_nonnormalised)), int)
    np.fill_diagonal(Q, np.diag(item_similarity_nonnormalised))

    #recommendation matrix gamma
    gamma = ratings @(np.divide(1,np.sqrt(Q), where=Q!=0)) @ item_similarity_nonnormalised @ (np.divide(1,np.sqrt(Q), where=Q!=0))
    print(gamma)


if __name__ == "__main__":
    purchase, play = read()
    #print(purchase[0:5])
    R = generate_matrix(purchase)
    useruser(R)
    

