#Ryan Solava
#5/17/2022
#
#This code scrapes the search results of the boardgamegeek website.
#It gets the name, url, year of release, and rating
#Then adds it to an SQL database

import requests, bs4
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import time, os
import ast
import matplotlib.pyplot as plt

import numpy as np
import pickle
import sqlalchemy as db

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

#Initialize SQLalchemy connection
engine = db.create_engine("sqlite:///game.db")

connection = engine.connect()
metadata = db.MetaData()
game_table = db.Table('GAMES', metadata, autoload=True, autoload_with=engine)

#Initialize selenium crawler
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)

base_url = "https://boardgamegeek.com/browse/boardgame/page/"
start = 1 #Page of results to begin on
stop = 240 #Page of results to end on
i = start

while i <= stop:
    if  (i - start) % 10 == 2:
        print((i-start)/(stop-start)*100, "% pages read,", (i-start), "in total")
    #Open page https://boardgamegeek.com/browse/boardgame/page/i
    url = base_url + str(i)

    try:
        driver.get(url)
    except:
        print("Error Occured!")
        time.sleep(5)
        continue

    soup = bs(driver.page_source,'html5lib')
    #For each game (row of table on page), read in info
    for x in soup.find_all("tr", attrs={"id":re.compile("row")}):
        y = x.find("div", attrs={"id":re.compile("results_objectname")})
        try:
            game_url = y.find("a")["href"]
        except:
            game_url = None
        try:
            game_name = y.find("a").text
        except:
            game_name = None
        try:
            game_year = int(y.find(class_="smallerfont dull").text.replace("(","").replace(")",""))
        except:
            game_year = None

        try:
            game_geek_rating = float(x.find(class_="collection_bggrating").text)
        except:
            game_geek_rating = None

        #Add to SQL database
        query = db.insert(game_table).values(URL=game_url,NAME=game_name,
                                             YEAR=game_year,GRATING=game_geek_rating)
        ResultProxy = connection.execute(query)


    time.sleep(5)
    i += 1
