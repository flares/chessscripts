import pandas as pd
import requests
from datetime import *
import re
import json
from pgn_parser import pgn, parser
import hashlib
import os
import pickle
import cachedHTTPRequests

ARCHIVES_LIST_API = "https://api.chess.com/pub/player/<USER>/games/archives"

class ChessGameAnalyser:
    def __init__(self):
        self.kills = {
                'p':0, 'r':0, 'n':0, 'b':0, 'q':0, 'k':0,
                'P':0, 'R':0, 'N':0, 'B':0, 'Q':0, 'K':0
                }
        self.num_white_games = 0
        self.num_black_games = 0

    def fetchAllAvailableArchives(self):
        apiUrl = ARCHIVES_LIST_API.replace("<USER>", self.user)
        print ("Fetching from ", apiUrl)
        url_data = requests.get(apiUrl)
        print(url_data.text)
        archive_list = json.loads(url_data.text)["archives"]
        return archive_list

    def run(self, user):
        self.user = user
        #self.cleanup()

        archive_list = self.fetchAllAvailableArchives()

        for archive in archive_list:
            monthly_archive_data = cachedHTTPRequests.get(archive)
            self.parseAndEvaluateMonthlyData(user, json.loads(monthly_archive_data.text)["games"])

        self.pretty_print_stats()

    def pretty_print_stats(self):
        print ("=========== Chess Stats of ", user, " ===============")

        total_black_kills = [kills[piece] for piece in kills if piece.islower()]
        total_white_kills = [kills[piece] for piece in kills if piece.isupper()]

        black_kills_pct = {piece:str(round(kills[piece]*100/sum(total_black_kills), 2))+" %" for piece in kills if piece.islower()}
        white_kills_pct = {piece:str(round(kills[piece]*100/sum(total_white_kills), 2))+" %" for piece in kills if piece.isupper()}
        print (black_kills_pct, ", total black kills : ", sum(total_black_kills), sum(total_black_kills) * 100 / num_black_games)
        print (white_kills_pct, ", total white kills : ", sum(total_white_kills), sum(total_white_kills) * 100 / num_white_games)

    def parseAndEvaluateMonthlyData(self, user, game_list):
        for game in game_list:
            game_pgn = game["pgn"] if "pgn" in game else None
            skip = True if "pgn" not in game or "Variant" in game["pgn"] else False

            if skip:
                continue

            parsed_game = parser.parse(game_pgn, actions=pgn.Actions())
            import code
            code.interact(local=locals())

            #get_game_stats(parsed_game.movetext, parsed_game.tag_pairs["White"] == user)


        print ("Total games : ", len(parsed_data), ", Pgn missing :", pgn_missing_counter, ", Variant games : ",  variant_game_counter)

    def get_game_stats(movelist, is_white):
        global kills
        #print ("Analysing game stats as user is ", is_white)
        white_moves = [m.white.san for m in movelist if m.white.san != ""]
        black_moves = [m.black.san for m in movelist if m.black.san != ""]

        moves = white_moves if is_white else black_moves
        global num_white_games
        global num_black_games
        global kills
        if is_white:
            num_white_games = num_white_games + 1
        else:
            num_black_games = num_black_games + 1

        import code
        code.interact(local=locals())
        for move in moves:
            if 'x' in move:
                if move[0] in ['R', 'B', 'N', 'Q', 'K']:
                    piece = move[0]
                else:
                    piece = 'P'
                piece = piece.upper() if is_white else piece.lower()
                kills[piece] = kills[piece] + 1
        pass


if __name__ == "__main__":
    chessGameAnalyser = ChessGameAnalyser()
    chessGameAnalyser.run("Subramanyam782")
