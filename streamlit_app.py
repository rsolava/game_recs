import streamlit as st
import pandas as pd
import numpy as np

import pickle


if "iter" not in st.session_state:
    st.session_state["iter"] = 1

    st.session_state["game_df"] = pickle.load( open("df2.p","rb"))

else:
    st.session_state.iter += 1



text = st.text_area("Board game recommender!")

game_df = st.session_state.game_df


if st.session_state.iter > 1:

    recs = game_df.head()

    for i in range(0,5):
        st.text(str(i+1) + ". "+ recs.name[i])
