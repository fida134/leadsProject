import streamlit as st
import pandas as pd
import os

BIN_PATH = "/crmproject/data/bin.csv"

def load_bin_data():
    if os.path.exists(BIN_PATH):
        return pd.read_csv(BIN_PATH)
    else:
        return pd.DataFrame()

def bin_page():
    st.title("Bin Page")
    if os.path.exists(BIN_PATH):
        data = pd.read_csv(BIN_PATH)
        if not data.empty:
            st.dataframe(data)
        else:
            st.info("No data in Bin.")
    else:
        st.info("Bin file does not exist yet.")
