#Ryan Solava
#5/17/2022
#
#Using the SQL database initialized by the url_scraper code
#This program scrapes the data from the game specific pages on
#board game game_geek_rating



#Functions to find various features from the main game page
#All return None if fail to find
def get_description(soup):
    try:
        paras = soup.find("article",class_="game-description-body ng-scope").find_all("p")
        return " ".join(p.text for p in paras)
    except:
        return None

def get_weight(soup):
    try:
        gameplay_list = soup.find_all(class_="gameplay-item")

        return float(gameplay_list[3].find(text=re.compile("/ 5")).previous.strip())

    except:
        return None

def get_age(soup):
    #TODO: This function depends on the age being of the form ##+, fix
    try:
        gameplay_list = soup.find_all(class_="gameplay-item")
        return int(gameplay_list[2].find(text=re.compile("\+")).strip().replace("+",""))
    except:
        return None

def get_minmax_time(soup):
    try:
        gameplay_list = soup.find_all(class_="gameplay-item")
        time_values = gameplay_list[1].find_all(class_=re.compile("ng-binding ng-scope"))
        if len(time_values) == 3:
            return int(time_values[0].text), int(time_values[1].text.replace("–",""))
        else:
            #If only one value, same min and max time
            value = int(time_values[0].text)
            return value,value
    except:
        return None, None

def get_minmax_players(soup):
    try:
        gameplay_list = soup.find_all(class_="gameplay-item")
        players_values = gameplay_list[0].find_all(class_=re.compile("ng-binding ng-scope"))
        if len(players_values) == 3:
            return int(players_values[0].text), int(players_values[1].text.replace("–",""))
        else:
            #If only one player count, min and max are the same
            value = int(players_values[0].text)
            return value, value
    except:
        return None, None

#Functions to find features from game credits pages
def get_publishers(soup):
    try:
        pubs = soup.find(attrs={"name":"boardgamepublisher"}).find_next("div").find_all("a")
        pubs = [x.text.strip() for x in pubs]
        return pubs
    except:
        return None

def get_designers(soup):
    try:
        designers = soup.find(attrs={"name":"boardgamedesigner"}).find_next("div").find_all("a")
        designers = [x.text.strip() for x in designers]
        return designers
    except:
        return None

def get_categories(soup):
    try:
        cats = soup.find(attrs={"name":"boardgamecategory"}).find_next("div").find_all("a")
        cats = [x.text.strip() for x in cats]
        return cats
    except:
        return None

def get_mechanics(soup):
    try:
        mechs = soup.find(attrs={"name":"boardgamemechanic"}).find_next("div").find_all("a")
        mechs = [x.text.strip() for x in mechs]
        return mechs
    except:
        return None


#initialize selenium chrome drive
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)


#Initialize SQLalchemy connection
engine = db.create_engine("sqlite:///game.db")

connection = engine.connect()
metadata = db.MetaData()
game_table = db.Table('GAMES', metadata, autoload=True, autoload_with=engine)

#Read in current database
query = db.select([game_table])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
curr_df = pd.DataFrame(ResultSet)
curr_df.columns = ResultSet[0].keys()


for ind in curr_df.index:
    #Check if we've seen this row already
    #If so, skip
    if curr_df.iloc[ind].notna().sum() > 4:
        continue


    if ind % 20 == 0:
        print(ind, "games scraped", ind/curr_df.shape[0]*100, "%")

    #Fetch main game page
    url = "https://boardgamegeek.com/" + curr_df.iloc[ind].URL

    try:
        driver.get(url)
    except:
        print("Error!")
        time.sleep(5)
        continue
    stats_soup = bs(driver.page_source,'html5lib')

    avrating = get_avg_rating(stats_soup)
    weight = get_weight(stats_soup)
    player_age = get_age(stats_soup)
    min_time,max_time= get_minmax_time(stats_soup)
    min_players,max_players= get_minmax_players(stats_soup)
    descr = get_description(stats_soup)

    time.sleep(5)

    #Fetch game's credits page
    try:
        driver.get(url + "/credits")
    except:
        print("Error!")
        time.sleep(5)
        continue

    credits_soup = bs(driver.page_source,'html5lib')

    designers = get_designers(credits_soup)
    publishers = get_publishers(credits_soup)
    categories = get_categories(credits_soup)
    mechanics = get_mechanics(credits_soup)


    #Add scraped data to database
    query = db.update(game_table).where(game_table.c.URL == curr_df.iloc[ind].URL).values(
        AVRATING=avrating,WEIGHT=weight,AGE=player_age,MINTIME=min_time,MAXTIME=max_time,
        MINCOUNT = min_players,MAXCOUNT=max_players,DESCRIPTION=descr,
        DESIGNERS=str(designers),PUBLISHERS =str(publishers),CATEGORIES=str(categories),
        MECHANICS=str(mechanics),SCRAPEDATE=date.today())

    ResultProxy = connection.execute(query)
    time.sleep(5)
