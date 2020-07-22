import pandas as pd
import requests
from datetime import *
import re

user = "Subramanyam782"
url = "https://www.chess.com/games/archive/<USER>?gameOwner=other_game&gameType=recent&timeSort=asc&endDate%5Bdate%5D=<END_DATE>&startDate%5Bdate%5D=<START_DATE>&page=<PAGE>"
url  = url.replace("<USER>", user)

one_days = timedelta(1,0,0)
seven_days = timedelta(7,0,0)

today = date(2020,7,5)
query_range_days = seven_days

start_date = date(2020,4,20)
end_date = start_date + query_range_days
granular_end_date = today

gameList = None

url = url.replace('<PAGE>', 0)

granular_fetch = False
num_queries = 0
while start_date < today:
    start_date_string = start_date.strftime("%m/%d/%Y")
    end_date_string = end_date.strftime("%m/%d/%Y")

    newUrl = url.replace("<START_DATE>", start_date_string)
    newUrl = newUrl.replace("<END_DATE>", end_date_string)
    print (newUrl)
    print("Getting data of games from ", start_date_string, " to ", end_date_string, " ... ", end= '')

    r = requests.get(newUrl)
    num_queries = num_queries + 1

    if "No results found" in r.text:
        print ("Skipping parse as no table info")
    else:
        pattern = re.compile('Games \((\w+)\)')
        match_groups = re.search(pattern, r.text)
        num_games = 0
        if match_groups is not None:
            print("DATA - ", match_groups.group(0), end = "")
        num_games = int(match_groups.group(0)[5:].replace(")", "").replace("(", ""))
        df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
        gameListData = df_list[0]
        fetched_games = int(gameListData.shape[0])

        ## player data split
        player_break = pd.DataFrame(gameListData["Players"].str.split(" ").tolist(), columns = ["white_player", "e2", "white_rating", "e3", "black_player", "e4" ,"black_rating"])
        player_break = player_break.drop(columns=["e2","e3", "e4"])

        gameListData["white_player"] = player_break["white_player"]
        gameListData["white_rating"] = player_break["white_rating"]
        gameListData["black_player"] = player_break["black_player"]
        gameListData["black_rating"] = player_break["black_rating"]

        ## Result split
        result_break = pd.DataFrame(gameListData["Result"].str.split(" ").tolist(), columns = ["white_points", "e2", "black_points"])

        gameListData["white_points"] = result_break["white_points"]
        gameListData["black_points"] = result_break["black_points"]

        import code
        code.interact(local= locals())
        ## accuracy split
        tmp = gameListData["Accuracy"].str.split(" ")
        tmp.fillna(["", "", ""])
        accuracy_break = pd.DataFrame(gameListData["Accuracy"].str.split(" ").tolist(), columns = ["white_accuracy", "e2", "black_accuracy"])

        gameListData["white_accuracy"] = accuracy_break["white_accuracy"]
        gameListData["black_accuracy"] = accuracy_break["black_accuracy"]

        gameListData.drop(columns = ["Players", "Result", "Accuracy", "6"])

        print ("Got ", gameListData.shape, " elements")
        print ("Counts ", start_date_string, " to ", end_date_string, " : ", num_games, "-", gameListData.shape[0])

        if fetched_games != num_games:
            if granular_fetch:
                print(start_date, "-", end_date, "One days has more than 50 games - Good bye sir")
                exit()

            granular_fetch = True
            granular_end_date = end_date
            end_date = start_date
            print ("Going granualar...******************")
            continue

        if gameList is None:
            gameList = gameListData
        else:
            gameList = gameList.append(gameListData)
        print ("Game list size : ", gameList.shape)

    if end_date == granular_end_date:
        granular_fetch = False
        query_range_days = seven_days
        print ("coming out of granualar...******************")
    # Next batch
    start_date = end_date + one_days
    end_date = (start_date + query_range_days) if not granular_fetch else start_date

gameList.to_csv(user + "_all_game_summary.csv")
print ("Total number of queries - ", num_queries)
