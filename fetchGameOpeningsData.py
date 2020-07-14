import pandas as pd
import requests
from datetime import *
import re
import json
from pgn_parser import pgn, parser
import hashlib
import os
import pickle

available_archives_api = "https://api.chess.com/pub/player/<USER>/games/archives"

columns = [
        "GAME_ID", "GAME_DATE", "TIME_CONTROL", "OPENING", "NUM_MOVES",
        "WHITE_PLAYER", "WHITE_ELO",
        "BLACK_PLAYER", "BLACK_ELO",
        "GAME_TERMINATION",
        "WINNER", "WIN_TYPE",
        "START_TIME", "END_TIME",
        "GAME_LINK", "GAME_OPENING_LINK"
        ]
all_game_data = pd.DataFrame(columns = columns)

def fetchAllAvailableArchives(user):
    newUrl = available_archives_api.replace("<USER>", user)
    print ("Fetching from ", newUrl)
    r = requests.get(newUrl)
    print(r.text)
    return json.loads(r.text)

def processUserData(user):
    data = fetchAllAvailableArchives(user)
    archives = data["archives"]

    global all_game_data
    for archive in archives:
        monthly_archive_data = fetch_and_cahce_url(archive)
        processed_df = parseMonthlyArchiveJson(json.loads(monthly_archive_data.text))
        if all_game_data is None:
            all_game_data = processed_df
        else:
            all_game_data = all_game_data.append(processed_df, ignore_index=True)

    print ("Done processing for ", user, "!")

def parseMonthlyArchiveJson(gameData):
    games = gameData["games"]
    parsed_data = []
    pgn_missing_counter = 0
    variant_game_counter = 0
    for game in games:
        if "pgn" not in game:
            pgn_missing_counter = pgn_missing_counter + 1
            continue
        game_pgn = game["pgn"]
        if "Variant" in game_pgn:
            variant_game_counter = variant_game_counter + 1
            continue
        parsed_game = parser.parse(game_pgn, actions=pgn.Actions())
        tags = parsed_game.tag_pairs

        num_moves =  int(len(parsed_game.movetext) / 2) + int(len(parsed_game.movetext) % 2)
        #import code
        #code.interact(local=locals())
        termination = tags.get("Termination", "NA")
        winner = termination.split(" ")[0] if "Game" not in termination else "Draw"
        win_type = " ".join(termination.split(" ")[2:]) if "Game" not in termination else termination

        parsed_data.append([
            game["url"].split("/")[-1],
            tags.get("Date", "NA"),
            tags.get("TimeControl", "NA"),
            tags.get("ECOUrl", "NA").split("/")[-1],
            num_moves,

            tags.get("White", "NA"),
            tags.get("WhiteElo", "NA"),
            tags.get("Black", "NA"),
            tags.get("BlackElo", "NA"),
            tags.get("Termination", "NA"),

            winner,
            win_type,

            tags.get("StartTime", "NA"),
            tags.get("EndTime", "NA"),

            tags.get("Link", "NA"),
            tags.get("ECOUrl", "NA")
        ])

    print ("Total games : ", len(parsed_data), ", Pgn missing :", pgn_missing_counter, ", Variant games : ",  variant_game_counter)
    return pd.DataFrame(parsed_data, columns = columns)

def fetch_and_cahce_url(url):
    cache_path = "/Users/funtimer/Dev/URL_CACHE/"
    cache_index_file = cache_path + "cache_index.pkl"
    if os.path.exists(cache_index_file):
        f = open(cache_index_file, "rb")
        index = pickle.load(f)
        data = None
        if url in index and os.path.exists(index[url]):
            with open(index[url], "rb") as g:
                data = pickle.load(g)
        f.close()
        if data is not None:
            return data

    print ("Fetching url - ", url)
    fetched_data = requests.get(url)
    # store data
    index = {}
    if os.path.exists(cache_index_file):
        with open(cache_index_file, "rb") as h:
            index = pickle.load(h)
    data_file_name= hashlib.md5(url.encode('utf-8')).hexdigest()
    index[url] = cache_path + data_file_name
    with open(cache_index_file, "wb") as h:
        print ("Storing ", cache_index_file)
        pickle.dump(index, h)
    with open(cache_path + data_file_name, "wb") as h:
        print ("Storing ", cache_path + data_file_name)
        pickle.dump(fetched_data, h)
    return fetched_data

processUserData("fun_man")
processUserData("Subramanyam782")
all_game_data.to_csv("All_opening_termination.csv")
