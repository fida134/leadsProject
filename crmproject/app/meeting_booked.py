import streamlit as st
import pandas as pd
import os
from raw_data import editable_table  # Import the editable_table function

MEETING_BOOKED_PATH = "/Users/hassaniftikhar4472/Desktop/crmproject/data/meeting_booked.csv"
QUALIFIED_PATH = "/Users/hassaniftikhar4472/Desktop/crmproject/data/qualified.csv"
DISQUALIFIED_PATH = "/Users/hassaniftikhar4472/Desktop/crmproject/data/disqualified.csv"
DEALS_ACTIVE_PATH = "/Users/hassaniftikhar4472/Desktop/crmproject/data/deals_active.csv"

def load_meeting_data():
    if os.path.exists(MEETING_BOOKED_PATH):
        return pd.read_csv(MEETING_BOOKED_PATH)
    else:
        return pd.DataFrame()

def save_data(data, file_path, append=False):
    """Save data to the given file, appending if append is True, otherwise overwriting the file."""
    if not os.path.exists(file_path) or not append:
        data.to_csv(file_path, index=False)
    else:
        data.to_csv(file_path, mode='a', header=False, index=False)

def meeting_booked_page():
    st.title("Meeting Booked Page")
    data = load_meeting_data()
    
    if not data.empty:
        # Display and allow inline editing of the table
        st.subheader("Edit Meeting Booked Data")
        edited_data = editable_table(data)  # Get the edited data

        # Track changes in session state
        if 'changed' not in st.session_state:
            st.session_state.changed = False
        
        if not edited_data.equals(data):
            st.session_state.changed = True
        else:
            st.session_state.changed = False

        # Show Save button only if changes have been made
        if st.session_state.changed:
            save_button = st.button("Save Changes")
            if save_button:
                save_data(edited_data, MEETING_BOOKED_PATH)
                st.success("Changes saved successfully!")
        else:
            st.write("No changes detected.")

        # Row selection and moving logic
        st.subheader("Select rows to move:")
        selected_rows = st.multiselect(
            "Select Rows by Index", data.index.tolist(), default=[]
        )
        
        if st.button("Move to Qualified"):
            if selected_rows:
                qualified_data = pd.DataFrame(data.loc[selected_rows])
                
                # Append to qualified file
                save_data(qualified_data, QUALIFIED_PATH, append=True)
                
                # Append to Deals Active table
                save_data(qualified_data, DEALS_ACTIVE_PATH, append=True)
                
                # Remove from Meeting Booked
                data.drop(index=selected_rows, inplace=True)
                save_data(data, MEETING_BOOKED_PATH)
                st.success("Selected rows moved to Qualified and Deals Active!")
                st.experimental_rerun()
            else:
                st.warning("Please select rows to move.")
        
        if st.button("Move to Disqualified"):
            if selected_rows:
                disqualified_data = pd.DataFrame(data.loc[selected_rows])
                
                # Append to disqualified file
                save_data(disqualified_data, DISQUALIFIED_PATH, append=True)
                
                # Remove from Meeting Booked
                data.drop(index=selected_rows, inplace=True)
                save_data(data, MEETING_BOOKED_PATH)
                st.success("Selected rows moved to Disqualified!")
                st.experimental_rerun()
            else:
                st.warning("Please select rows to move.")
    else:
        st.info("No data in Meeting Booked.")
