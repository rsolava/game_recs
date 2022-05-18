import streamlit as st
import pandas as pd
import numpy as np

import pickle

def get_creators(row):
    try:
        result = row["designers"] + row["publishers"]
    except:
        result = []
    return result
        

def get_cat_mechs(row):
    try:
        result = row["categories"] + row["mechanics"]
    except:
        result = []
    return result

def sim_many(row,multirow):
    vals = multirow.apply(lambda x: similarity(row,x),axis=1)
    vals.head(5)
    return vals.mean()
    

def similarity(row1,row2):
    a = .7
    b = .3
    c = 1 - a - b
    #Creator similarity
    
    creator_sim = jaccard(get_creators(row1),get_creators(row2))
    
    #Genre/Mechanics similarity
    cat_sim = jaccard(get_cat_mechs(row1),get_cat_mechs(row2))
    
    #Description similarity
    descr_sim = 0
    
    print("Success")
    return a*creator_sim + b*cat_sim + c*descr_sim
    
def jaccard(list1, list2):
        
    set1 = set(list1)
    set2 = set(list2)
    
    num = len(set1 & set2)
    denom = len(set1 | set2)
    
    if denom == 0:
        return 0
    else:
        return len(set1 & set2)/len(set1 | set2)

def find_top_recs(options, rows, n):
    dists = options.apply(lambda x: 1-sim_many(x,rows), axis=1)
    
    dists = np.where(dists == 0.0, 1, dists)

    best_indices = np.argpartition(dists, n)[:n]
    return pd.DataFrame([options.iloc[i] for i in best_indices])

if "iter" not in st.session_state:
    st.session_state["iter"] = 1

    st.session_state["game_df"] = pickle.load( open("df2.p","rb"))
    
    st.session_state["game_list"] = st.session_state.game_df.name.unique()
    st.session_state.game_list.sort()
    

else:
    st.session_state.iter += 1

game_df = st.session_state.game_df
game_list = st.session_state.game_list

"## Board game recommender"

with st.form("my_form"):

    
    "### Enter some games you like"
    
    game_vals = st.multiselect("Games",game_list)
    
    "### Filter on any additional criteria"
    
    grating_vals = st.slider("Geek Rating",0.0, 10.0, (0.0, 10.0))
    complexity_vals = st.slider("Complexity",0.0, 5.0, (0.0, 5.0))
    player_val = st.text_input("Number of players")
    age_val = st.text_input("Player age")
    year_val = st.text_input("Year published")
    
    st.write("")
    
    st.form_submit_button(label="Recommend!", help=None, on_click=None, args=None, kwargs=None)
    

if st.session_state.iter > 1:
    
    recs = game_df
    
    player_num = int(player_val) if player_val.isnumeric() else None
    
    if player_val.isnumeric():
        player_num = int(player_val)
        recs = game_df[(game_df.min_players <= player_num) & (game_df.max_players >= player_num)]
        
    if age_val.isnumeric():
        age_num = int(age_val)
        recs = recs[game_df.player_age <= age_num]
        
    if year_val.isnumeric():
        year_num = int(year_val)
        recs = recs[game_df.year == year_num]
    
    recs = recs[(complexity_vals[0] <= recs.weight) & (recs.weight <= complexity_vals[1])]
    recs = recs[(grating_vals[0] <= recs.rating) & (recs.rating <= grating_vals[1])]
    recs = recs[recs.name.apply(lambda x: x not in game_vals)]
    
    selections = game_df[game_df.name.apply(lambda x: x in game_vals)]
    recs = find_top_recs(recs,selections,5)
    #recs.sort_values(by="rating", inplace = True, ascending = False)
    
    #recs = recs.head(5)
    recs.reset_index(inplace=True)
    
    if(recs.shape[0] == 0):
        st.text("No results found.")
    
    
    for i, row in recs.iterrows():
        game_name = row["name"]
        game_url = row["url"]
        game_year= row["year"]
        
        line = str(i+1)  + ". "
        try:
            line += "[" + game_name + " (" + str(int(game_year)) + ")]"
        except:
            line +="[" + game_name + "]"
        line +=  "(https://boardgamegeek.com/" + game_url + ")"
        st.write(line)

