import pandas as pd
import requests
from datetime import *
import re


class ChessArchiveUrlGenerator:
    def __init__(self):
        self.user = "Subramanyam782"
        self.user = "fun_man"
        self.url = "https://www.chess.com/games/archive/<USER>?gameOwner=other_game&gameType=recent&timeSort=asc&startDate%5Bdate%5D=<START_DATE>&endDate%5Bdate%5D=<END_DATE>"
        self.url  = self.url.replace("<USER>", self.user)

        self.one_days = timedelta(1,0,0)
        self.seven_days = timedelta(2,0,0)

        self.query_range_days = self.seven_days

    def reset(self, fromDate = date(2020,4,20), toDate = date(2020,7,15)):
        self.from_date = fromDate
        self.to_date  = toDate
        self.lastStartDate = None
        self.lastEndDate = None
        pass

    def pickNextStartEndDates(self):
        start_date, end_date = None, None
        if self.lastStartDate == None:
            start_date = self.from_date
            end_date = self.from_date + self.query_range_days
        else:
            start_date = self.lastEndDate + self.one_days
            end_date = start_date + self.query_range_days

        self.lastStartDate = start_date
        self.lastEndDate = end_date
        return (start_date, end_date)

    def getNextUrl(self):
        start_date, end_date = self.pickNextStartEndDates()

        if start_date > self.to_date:
            print("Done with URL's")
            return None
        else:
            start_date_string = start_date.strftime("%m/%d/%Y")
            end_date_string = end_date.strftime("%m/%d/%Y")

            newUrl = self.url.replace("<START_DATE>", start_date_string)
            newUrl = newUrl.replace("<END_DATE>", end_date_string)
            print ("Next URL - ", newUrl)
            return newUrl


#cag = ChessArchiveUrlGenerator()
#cag.reset(date(2020,6,2), date(2020,7,5))
#cag.getNextUrl()

