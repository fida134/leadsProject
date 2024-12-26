import streamlit as st
import pandas as pd
import os
from raw_data import editable_table

QUALIFIED_PATH = "/Users/hassaniftikhar4472/Desktop/crmproject/data/qualified.csv"
DISQUALIFIED_PATH = "/Users/hassaniftikhar4472/Desktop/crmproject/data/disqualified.csv"

def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

def save_data(file_path, data):
    data.to_csv(file_path, index=False)

def qualified_disqualified_page():
    st.title("Qualified/Disqualified Page")
   
    
    qualified_data = load_data(QUALIFIED_PATH)
    disqualified_data = load_data(DISQUALIFIED_PATH)

    # Editable table for Qualified Data
    st.subheader("Qualified Data")
    qualified_data = editable_table(qualified_data)   
   

    # Editable table for Disqualified Data
    st.subheader("Disqualified Data")
    disqualified_data = editable_table(disqualified_data)   
     
    
    # Save button to store changes to CSV
    if st.button("Save Changes"):
        save_data(QUALIFIED_PATH, qualified_data)
        save_data(DISQUALIFIED_PATH, disqualified_data)
        st.success("Changes saved successfully!")
