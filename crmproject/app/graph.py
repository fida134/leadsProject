import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# File paths
DEALS_ACTIVE_PATH = "/crmproject/data/deals_active.csv"
FOLLOW_UP_PATH = "/crmproject/data/follow_up.csv"
CLOSED_DEAL_PATH = "/crmproject/data/closed_deal.csv"
Qualified_DEAL_PATH = "/crmproject/data/qualified.csv"

def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

def weekly_graphs_page():
    st.title("Weekly Graphs")
    
    # CSV Selection
    csv_option = st.selectbox("Select Deal Page", ["Active", "Closed", "Follow-Up",'Qualified'])
    if csv_option == "Active":
        data_path = DEALS_ACTIVE_PATH
    elif csv_option == "Closed":
        data_path = CLOSED_DEAL_PATH
    elif csv_option == "Follow-Up":
        data_path = FOLLOW_UP_PATH
    elif csv_option == "Qualified":
        data_path = Qualified_DEAL_PATH
    
    # Load the selected CSV
    data = load_data(data_path)
    
    if data.empty:
        st.warning("No data available in the selected CSV.")
        return
    
    # Ensure 'Date' and 'AppSetter' columns exist
    if 'Date' not in data.columns or 'AppSetter' not in data.columns:
        st.error("The selected CSV is missing required columns: 'Date' and 'AppSetter'.")
        return
    
    # Filter by date range
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Convert Date column to datetime
    data = data.dropna(subset=['Date'])  # Remove rows with invalid dates

    st.subheader("Filter Data by Date Range")
    min_date = data['Date'].min()
    max_date = data['Date'].max()
    start_date, end_date = st.date_input("Select Date Range", [min_date, max_date])
    
    if start_date > end_date:
        st.error("Start date cannot be after end date.")
        return
    
    filtered_data = data[(data['Date'] >= pd.Timestamp(start_date)) & (data['Date'] <= pd.Timestamp(end_date))]

    if filtered_data.empty:
        st.warning("No data found for the selected date range.")
        return
    
    # Count rows grouped by 'AppSetter'
    grouped_data = filtered_data.groupby('AppSetter').size().reset_index(name='Count')

# Plotting the bar graph
    st.subheader("Bar Graph")
    col1, col2 = st.columns([1, 2])  # Create columns with relative widths

    with col1:
        # Show the graph in the narrower column
        fig, ax = plt.subplots(figsize=(5, 3))  # Adjust figure size
        ax.bar(grouped_data['AppSetter'], grouped_data['Count'], color='skyblue')
        ax.set_xlabel('AppSetter', fontsize=10)
        ax.set_ylabel('Number of Rows', fontsize=10)
        ax.set_title(f'Bar Graph for {csv_option} Deals', fontsize=12)
        ax.set_xticks(range(len(grouped_data['AppSetter'])))
        ax.set_xticklabels(grouped_data['AppSetter'], rotation=45, ha='right', fontsize=8)

        st.pyplot(fig)

    with col2:
        # Add other graphs or information in the second column
        st.write("Placeholder for other content")

