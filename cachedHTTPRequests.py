import pandas as pd
import requests
from datetime import *
import re
import json
from pgn_parser import pgn, parser
import hashlib
import os
import pickle

def get(url):
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
