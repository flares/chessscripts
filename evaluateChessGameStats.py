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
    class GameCounter:
        def __init__(self, name, description = ""):
            self.cleanup()
            self.name = name
            self.description = description

        def cleanup(self):
            self.pieceSheet = {
                    'p':0, 'r':0, 'n':0, 'b':0, 'q':0, 'k':0,
                    'P':0, 'R':0, 'N':0, 'B':0, 'Q':0, 'K':0
                    }
            self.num_white_games = 0
            self.num_black_games = 0

        def pretty_print(self):
            print ("------------", self.name, '-----------')
            total_black_kills = [self.pieceSheet[piece] for piece in self.pieceSheet if piece.islower()]
            total_white_kills = [self.pieceSheet[piece] for piece in self.pieceSheet if piece.isupper()]

            black_kills = {piece:self.pieceSheet[piece] for piece in self.pieceSheet if piece.islower()}
            white_kills = {piece:self.pieceSheet[piece] for piece in self.pieceSheet if piece.isupper()}

            if sum(total_black_kills) != 0:
                black_kills_pct = {piece:str(round(self.pieceSheet[piece]*100/sum(total_black_kills), 2))+" %" for piece in self.pieceSheet if piece.islower()}
            else:
                black_kills_pct = {piece:"0 %" for piece in self.pieceSheet if piece.islower()}
            if sum(total_white_kills) != 0:
                white_kills_pct = {piece:str(round(self.pieceSheet[piece]*100/sum(total_white_kills), 2))+" %" for piece in self.pieceSheet if piece.isupper()}
            else:
                white_kills_pct = {piece:"0 %" for piece in self.pieceSheet if piece.isupper()}

            avg_white_kills_per_game = round((sum(total_black_kills) / self.num_black_games),2) if self.num_black_games != 0 else 0
            avg_black_kills_per_game = round((sum(total_white_kills) / self.num_white_games),2) if self.num_white_games != 0 else 0

            print (black_kills)
            print (white_kills)
            print (black_kills_pct)
            print (white_kills_pct)
            print ("Total black %s : " % self.name, sum(total_black_kills),
                    ", Avg %s per game : " % self.name, avg_black_kills_per_game)
            print ("Total white %s : " % self.name, sum(total_white_kills),
                    ", Avg %s per game : " % self.name, avg_white_kills_per_game)

    def __init__(self):
        self.counters = {
                "kills" : self.GameCounter("Kills", "Number of kills by a piece"),
                "moves" : self.GameCounter("Moves", "Number of moves by a piece")
                }

    def run(self, user):
        self.user = user
        self.cleanup()
        archive_list = self.fetchAllAvailableArchives()
        for archive in archive_list:
            monthly_archive_data = cachedHTTPRequests.get(archive)
            self.parseAndEvaluateMonthlyData(user, json.loads(monthly_archive_data.text)["games"])

        self.pretty_print_stats()

    def fetchAllAvailableArchives(self):
        apiUrl = ARCHIVES_LIST_API.replace("<USER>", self.user)
        print ("Fetching from ", apiUrl)
        url_data = requests.get(apiUrl)
        archive_list = json.loads(url_data.text)["archives"]
        return archive_list

    def pretty_print_stats(self):
        print ("=========== Chess Stats of ", self.user, " ===============")
        for counter in self.counters:
            self.counters[counter].pretty_print()

    def cleanup(self):
        for counter in self.counters:
            self.counters[counter].cleanup()
        print()

    def parseAndEvaluateMonthlyData(self, user, game_list):
        for game in game_list:
            game_pgn = game["pgn"] if "pgn" in game else None
            skip = True if "pgn" not in game or "Variant" in game["pgn"] else False

            if skip:
                continue

            parsed_game = parser.parse(game_pgn, actions=pgn.Actions())
            self.get_game_kill_stats(parsed_game.movetext, parsed_game.tag_pairs["White"] == user)
            self.get_game_move_stats(parsed_game.movetext, parsed_game.tag_pairs["White"] == user)

    def get_game_kill_stats(self, movelist, is_white):
        counter = self.counters["kills"]
        white_moves = [m.white.san for m in movelist if m.white.san != ""]
        black_moves = [m.black.san for m in movelist if m.black.san != ""]

        moves = white_moves if is_white else black_moves
        if is_white:
            counter.num_white_games = counter.num_white_games + 1
        else:
            counter.num_black_games = counter.num_black_games + 1

        for move in moves:
            if 'x' in move:
                if move[0] in ['R', 'B', 'N', 'Q', 'K']:
                    piece = move[0]
                else:
                    piece = 'P'
                piece = piece.upper() if is_white else piece.lower()
                counter.pieceSheet[piece] = counter.pieceSheet[piece] + 1
        pass

    def get_game_move_stats(self, movelist, is_white):
        counter = self.counters["moves"]
        white_moves = [m.white.san for m in movelist if m.white.san != ""]
        black_moves = [m.black.san for m in movelist if m.black.san != ""]

        moves = white_moves if is_white else black_moves
        if is_white:
            counter.num_white_games = counter.num_white_games + 1
        else:
            counter.num_black_games = counter.num_black_games + 1

        for move in moves:
            if move[0].upper() in ['R', 'B', 'N', 'Q', 'K']:
                piece = move[0]
            else:
                piece = 'P'
            piece = piece.upper() if is_white else piece.lower()
            counter.pieceSheet[piece] = counter.pieceSheet[piece] + 1
        pass

if __name__ == "__main__":
    chessGameAnalyser = ChessGameAnalyser()
    chessGameAnalyser.run("Subramanyam782")
    chessGameAnalyser.run("fun_man")
