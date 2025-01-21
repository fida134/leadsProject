import streamlit as st
import pandas as pd
import os

DATA_PATH = "/crmproject/data/raw_data.csv"
BIN_PATH = "/crmproject/data/bin.csv"
MEETING_BOOKED_PATH = "/crmproject/data/meeting_booked.csv"
APPSETTER_PATH = "/crmproject/data/appsetter.csv"
NOT_PICKED_PATH = "/crmproject/data/not_picked.csv"
CALLBACK_PATH = "/crmproject/data/callback.csv"

def load_data():
    """Load raw data from CSV."""
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        st.error("Raw data file not found!")
        return pd.DataFrame()


#ddS
def load_appsetters():
    """Load AppSetter names from appsetter.csv."""
    if os.path.exists(APPSETTER_PATH):
        df = pd.read_csv(APPSETTER_PATH)
        return df["AppSetter"].dropna().tolist()
    else:
        st.error("AppSetter file not found!")
        return []

def save_data(data, file_path, append=False):
    """Save data to the given file, appending if append is True, otherwise overwriting the file."""
    if not os.path.exists(file_path) or not append:
        # If the file does not exist or append is False, create it with headers (overwrite)
        data.to_csv(file_path, index=False)
    else:
        # Append to the file if it exists and append is True
        data.to_csv(file_path, mode='a', header=False, index=False)

st.set_page_config(layout="wide")  # Enables wide-screen layout

# Custom CSS to Reduce Table Header Size and Padding
def set_custom_css():
    custom_css = """
    <style>
        /* Make table headers smaller */
        .stDataFrame table th {
            font-size: 12px !important;  /* Adjust header font size */
            padding: 4px !important;     /* Reduce padding */
        }

        /* Make table content smaller */
        .stDataFrame table td {
            font-size: 12px !important;  /* Adjust content font size */
            padding: 4px !important;     /* Reduce padding */
        }

        /* Enable horizontal scrolling */
        .stDataFrame table {
            display: block;
            overflow-x: auto; /* Add horizontal scroll for wide tables */
            white-space: nowrap;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Call custom CSS
set_custom_css()

def editable_table(data):
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
    )

    return editable_data

def raw_data_page():
    """Main page for raw data handling."""
    st.title("Raw Data Page")
    data = load_data()

    if not data.empty:
        # Display and allow inline editing of 4 specific columns
        edited_data = editable_table(data)

        st.subheader("Select rows to move:")
        selected_rows = st.multiselect(
            "Select Rows by Index", data.index.tolist(), default=[]
        )

        # Check which rows have been modified
        if st.button("Save Changes"):
            # Compare the original data with the edited data
            modified_rows = edited_data != data
            modified_rows_index = modified_rows.any(axis=1).index[modified_rows.any(axis=1)].tolist()

            if modified_rows_index:
                # Update only modified rows in the original data
                for row_index in modified_rows_index:
                    data.loc[row_index] = edited_data.loc[row_index]

                # Save the updated data to the raw data file
                save_data(data, DATA_PATH)
                st.success("Changes saved successfully!")
            else:
                st.warning("No changes detected.")

        # Move to Bin
        if st.button("Move to notpicked"):
            if selected_rows:
                notpicked = pd.DataFrame(data.loc[selected_rows])
                save_data(notpicked, NOT_PICKED_PATH , append=True)  # Remove append=True
                data.drop(index=selected_rows, inplace=True)
                save_data(data, DATA_PATH)  # Save updated raw_data.csv
                st.success("Selected rows moved to notpicked!")
                st.experimental_rerun()
            else:
                st.warning("Please select rows to move.")
        if st.button("Move to callback"):
            if selected_rows:
                callback = pd.DataFrame(data.loc[selected_rows])
                save_data(callback, CALLBACK_PATH, append=True)  # Remove append=True
                data.drop(index=selected_rows, inplace=True)
                save_data(data, DATA_PATH)  # Save updated raw_data.csv
                st.success("Selected rows moved to callback!")
                st.experimental_rerun()
            else:
                st.warning("Please select rows to move.")
        if st.button("Move to Bin"):
            if selected_rows:
                bin_data = pd.DataFrame(data.loc[selected_rows])
                save_data(bin_data, BIN_PATH, append=True)  # Append data to Bin
                data.drop(index=selected_rows, inplace=True)
                save_data(data, DATA_PATH)  # Save updated callback.csv
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
                save_data(data, DATA_PATH)  # Save updated callback.csv
                st.success("Selected rows moved to Meeting Booked!")
                st.experimental_rerun()
            else:
                st.warning("Please select rows to move.")
    else:
        st.info("No data available in Raw Data.")
