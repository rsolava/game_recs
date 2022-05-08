import streamlit as st
import pandas as pd
import numpy as np

import pickle


if "iter" not in st.session_state:
    st.session_state["iter"] = 1

    st.session_state["game_df"] = pickle.load( open("df2.p","rb"))

else:
    st.session_state.iter += 1

game_df = st.session_state.game_df

"Board game recommender"

with st.form("my_form"):
    complexity_vals = st.slider("Complexity",0.0, 5.0, (1.0, 4.0))
    player_val = st.slider("Number of players", min_value = 1, max_value = 10, step= 1)
    #complexity_val = st.slider("Complexity", min_value = 0.0, max_value = 5.0, step = .1)
    #age_val = st.slider("Player age", min_value = 0, max_value = , step= 1)
    st.form_submit_button(label="Submit", help=None, on_click=None, args=None, kwargs=None)

if st.session_state.iter > 1:
    recs = game_df[(game_df.min_players <= player_val) & (game_df.max_players >= player_val)]
    recs = recs[(complexity_vals[0] <= recs.weight) & (recs.weight <= complexity_vals[1])]
    recs.sort_values(by="rating", inplace = True, ascending = False)
    recs = recs.head(5)
    recs
