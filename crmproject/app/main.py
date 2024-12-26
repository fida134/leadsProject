import streamlit as st
from raw_data import raw_data_page
from bin import bin_page
from meeting_booked import meeting_booked_page
from qualified_disqualified import qualified_disqualified_page
from not_picked import not_picked_page
from callback import callback_page
from deal import deals_page
from graph import weekly_graphs_page

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to", ["Raw Data", "Not Picked", "Callback", "Meeting Booked", "Qualified/Disqualified", "Deals Page", "Bin", "Weekly Graphs"]
)

# Render pages based on selection
if page == "Raw Data":
    raw_data_page()
elif page == "Bin":
    bin_page()
elif page == "Meeting Booked":
    meeting_booked_page()
elif page == "Qualified/Disqualified":
    qualified_disqualified_page()
elif page == "Not Picked":
    not_picked_page()
elif page == "Callback":
    callback_page()
elif page == "Deals Page":
    deals_page()
elif page == "Weekly Graphs":
    weekly_graphs_page()
