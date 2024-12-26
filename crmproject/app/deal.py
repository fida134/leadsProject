import streamlit as st
import pandas as pd
import os

DEALS_ACTIVE_PATH = "/crmproject/data/deals_active.csv"
FOLLOW_UP_PATH = "/crmproject/data/follow_up.csv"
CLOSED_DEAL_PATH = "/crmproject/data/closed_deal.csv"
LOST_DEAL_PATH = "/crmproject/data/lost_deal.csv"
APPSETTER_PATH = "/crmproject/data/appsetter.csv"

def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

def save_data(data, file_path, append=False):
    """Save data to the given file, appending if append is True, otherwise overwriting the file."""
    if not os.path.exists(file_path) or not append:
        data.to_csv(file_path, index=False)
    else:
        data.to_csv(file_path, mode='a', header=False, index=False)

def load_appsetters():
    """Load AppSetter names from appsetter.csv."""
    if os.path.exists(APPSETTER_PATH):
        df = pd.read_csv(APPSETTER_PATH)
        return df["AppSetter"].dropna().tolist()
    else:
        return []

def editable_table(data, key):
    """Allow inline editing of Date, Priority, Comment, and AppSetter."""
    
    # Ensure Date column is in the correct format
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce").dt.date

    # Convert text columns to string for consistency
    for col in ["comment", "AppSetter", "priority"]:  # Add more editable columns if needed
        if col in data.columns:
            data[col] = data[col].fillna("").astype(str)

    # Load AppSetter dropdown options
    appsetter_names = load_appsetters()

    # Define Streamlit column configuration for editable fields
    column_config = {
        "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
        "priority": st.column_config.SelectboxColumn(
            "Priority",
            options=["High", "Medium", "Low"],  # Define options explicitly
        ),
        "comment": st.column_config.TextColumn("Comment"),
        "AppSetter": st.column_config.SelectboxColumn(
            "AppSetter",
            options=appsetter_names,  # Dynamically load dropdown options
        ),
    }

    # Display the data editor with editable fields
    editable_data = st.data_editor(
        data,
        column_config=column_config,
        disabled=list(data.columns.difference(["Date", "priority", "comment", "AppSetter"])),
        use_container_width=True,
        key=key  # Pass the unique key here
    )

    return editable_data

def deals_page():
    st.title("Deals Page")

    # Load data for each table
    active_data = load_data(DEALS_ACTIVE_PATH)
    follow_up_data = load_data(FOLLOW_UP_PATH)
    closed_deal_data = load_data(CLOSED_DEAL_PATH)
    lost_deal_data = load_data(LOST_DEAL_PATH)

    # Active Deals Table
    st.subheader("Active Deals")
    if not active_data.empty:
        edited_active_data = editable_table(active_data, key="active_deals_table")
        
        # Save button for Active Deals
        if st.button("Save Changes to Active Deals"):
            if not edited_active_data.equals(active_data):
                save_data(edited_active_data, DEALS_ACTIVE_PATH)
                st.success("Changes saved to Active Deals!")

        selected_rows = st.multiselect("Select Active Deals to move:", active_data.index.tolist(), default=[])
        move_to = st.selectbox("Move to:", ["Follow-Up", "Closed", "Lost"])

        if st.button("Move Deal"):
            if selected_rows:
                if move_to == "Follow-Up":
                    follow_up_rows = active_data.loc[selected_rows]
                    save_data(follow_up_rows, FOLLOW_UP_PATH, append=True)
                    active_data.drop(index=selected_rows, inplace=True)
                    save_data(active_data, DEALS_ACTIVE_PATH)
                    st.success("Selected rows moved to Follow-Up!")
                elif move_to == "Closed":
                    closed_rows = active_data.loc[selected_rows]
                    save_data(closed_rows, CLOSED_DEAL_PATH, append=True)
                    active_data.drop(index=selected_rows, inplace=True)
                    save_data(active_data, DEALS_ACTIVE_PATH)
                    st.success("Selected rows moved to Closed Deals!")
                elif move_to == "Lost":
                    lost_rows = active_data.loc[selected_rows]
                    save_data(lost_rows, LOST_DEAL_PATH, append=True)
                    active_data.drop(index=selected_rows, inplace=True)
                    save_data(active_data, DEALS_ACTIVE_PATH)
                    st.success("Selected rows moved to Lost Deals!")
                
                st.rerun()  # Replace experimental rerun with the current one
            else:
                st.warning("Please select rows to move.")

    else:
        st.info("No active deals.")

    # Follow-Up Deals Table
    st.subheader("Follow-Up Deals")
    if not follow_up_data.empty:
        edited_follow_up_data = editable_table(follow_up_data, key="follow_up_deals_table")
        
        # Save button for Follow-Up Deals
        if st.button("Save Changes to Follow-Up Deals"):
            if not edited_follow_up_data.equals(follow_up_data):
                save_data(edited_follow_up_data, FOLLOW_UP_PATH)
                st.success("Changes saved to Follow-Up Deals!")

    else:
        st.info("No follow-up deals.")

    # Closed Deals Table
    st.subheader("Closed Deals")
    if not closed_deal_data.empty:
        edited_closed_deal_data = editable_table(closed_deal_data, key="closed_deals_table")
        
        # Save button for Closed Deals
        if st.button("Save Changes to Closed Deals"):
            if not edited_closed_deal_data.equals(closed_deal_data):
                save_data(edited_closed_deal_data, CLOSED_DEAL_PATH)
                st.success("Changes saved to Closed Deals!")

    else:
        st.info("No closed deals.")

    # Lost Deals Table
    st.subheader("Lost Deals")
    if not lost_deal_data.empty:
        edited_lost_deal_data = editable_table(lost_deal_data, key="lost_deals_table")
        
        # Save button for Lost Deals
        if st.button("Save Changes to Lost Deals"):
            if not edited_lost_deal_data.equals(lost_deal_data):
                save_data(edited_lost_deal_data, LOST_DEAL_PATH)
                st.success("Changes saved to Lost Deals!")

    else:
        st.info("No lost deals.")
