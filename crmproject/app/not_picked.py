import streamlit as st
import pandas as pd
import os
from raw_data import editable_table 
MEETING_BOOKED_PATH = "/Users/hassaniftikhar4472/Desktop/crmproject/data/meeting_booked.csv"
BIN_PATH = "/Users/hassaniftikhar4472/Desktop/crmproject/data/bin.csv"
NOT_PICKED_PATH = "/Users/hassaniftikhar4472/Desktop/crmproject/data/not_picked.csv"

def load_notpicked_data():
    if os.path.exists(NOT_PICKED_PATH):
        return pd.read_csv(NOT_PICKED_PATH)
    else:
        return pd.DataFrame()

def save_data(data, file_path, append=False):
    """Save data to the given file, appending if append is True, otherwise overwriting the file."""
    if not os.path.exists(file_path) or not append:
        # If the file does not exist or append is False, create it with headers (overwrite)
        data.to_csv(file_path, index=False)
    else:
        # Append to the file if it exists and append is True
        data.to_csv(file_path, mode='a', header=False, index=False)

def not_picked_page():
    st.title("Callback Page")
    data = load_notpicked_data()
    
    if not data.empty:
        st.subheader("Edit Callback Data")
        # Use the editable_table function from raw_data.py
        edited_data = editable_table(data)

        # Save Changes Button
        if st.button("Save Changes"):
            save_data(edited_data, NOT_PICKED_PATH)
            st.success("Changes saved successfully!")

        st.subheader("Select rows to move:")
        selected_rows = st.multiselect(
            "Select Rows by Index", data.index.tolist(), default=[]
        )

        # Move to Bin
        if st.button("Move to Bin"):
            if selected_rows:
                bin_data = pd.DataFrame(data.loc[selected_rows])
                save_data(bin_data, BIN_PATH, append=True)  # Append data to Bin
                data.drop(index=selected_rows, inplace=True)
                save_data(data, NOT_PICKED_PATH)  # Save updated callback.csv
                st.success("Selected rows moved to Bin!")
                st.experimental_rerun()
            else:
                st.warning("Please select rows to move.")

        # Move to Meeting Booked
        if st.button("Move to Meeting Booked"):
            if selected_rows:
                meeting_data = pd.DataFrame(data.loc[selected_rows])
                save_data(meeting_data, MEETING_BOOKED_PATH, append=True)  # Append data to Meeting Booked
                data.drop(index=selected_rows, inplace=True)
                save_data(data, NOT_PICKED_PATH)  # Save updated callback.csv
                st.success("Selected rows moved to Meeting Booked!")
                st.experimental_rerun()
            else:
                st.warning("Please select rows to move.")
    else:
        st.info("No data available in Callback.")