
import streamlit as st 
st.markdown("""
<style>
div[data-testid="stDateInput"] {
    width: 150px !important;
}
</style>
""", unsafe_allow_html=True)

# DATE TO 

col1, col2 = st.columns(2)

with col1:
    date_from = st.date_input("DATE FROM")

with col2:
    date_to = st.date_input("DATE TO")


# select a folder
import os
import streamlit as st

st.markdown("""
<style>
div[data-testid="stMultiSelect"] {
    width: 150px !important;
}
</style>
""", unsafe_allow_html=True)

def get_folders(folder_path):
    folders =[]
    
    for item in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path,item)):
            folders.append(item)
    return folders
folder_path = r"D:\Coding\gauri\NavigaLog"


folders = get_folders(folder_path)
# selected_folder = st.multiselect("Select Folder",folders)


#type 

import streamlit as st
st.markdown("""
<style>
div[data-testid="stMultiSelect"] {
    width: 150px !important;
}
</style>
""", unsafe_allow_html=True)

#


import streamlit as st

# Type Filter
type_options = ["Error", "Info", "Warn"]

# selected_types = st.multiselect("Type", options=type_options)


col1, col2 = st.columns(2)

# with col1:
    # selected_folder = st.multiselect(
        # "Select Folder",
        # folders
    # )

# with col2:
    # selected_types = st.multiselect("Type",options=type_options )

col1, col2 = st.columns(2)

with col1:
    selected_folder = st.multiselect(
        "Select Folder",
        options=["All"] + folders,
        default=["All"]
    )

with col2:
    selected_types = st.multiselect(
        "Type",
        options=["All"] + type_options,
        default=["All"]
    )


# Handle "All" selection
if "All" in selected_folder:
    folders_to_search = folders
else:
    folders_to_search = selected_folder

if "All" in selected_types:
    types_to_search = []  # empty list means no type filtering
else:
    types_to_search = selected_types









    

from datetime import datetime
import pandas as pd



if st.button("🔍 Search"):

    if not selected_folder:
        st.warning("Please select at least one folder.")

    else:

        results = []

        for folder in folders_to_search:

            folder_full_path = os.path.join(folder_path, folder)

            for root, dirs, files in os.walk(folder_full_path):

                for file in files:

                    if ".log" in file.lower():

                        file_path = os.path.join(root, file)

                        try:

                            with open(
                                file_path,
                                "r",
                                encoding="utf-8",
                                errors="ignore"
                            ) as f:

                                for line in f:

                                    # TYPE FILTER
                                    if types_to_search:

                                        match_found = False

                                        for log_type in types_to_search:

                                            if f"| {log_type.upper()} |" in line.upper():
                                                match_found = True
                                                break

                                        if not match_found:
                                            continue

                                    parts = [x.strip() for x in line.split("|")]

                                    if len(parts) >= 6:

                                        try:
                                            # Example:
                                            # 20260317_03:06:45,290
                                            log_date = datetime.strptime(
                                                parts[0][:8],
                                                "%Y%m%d"
                                            ).date()

                                            # DATE FILTER
                                            if (
                                                log_date < date_from
                                                or
                                                log_date > date_to
                                            ):
                                                continue

                                        except:
                                            continue
                                        for folder in folders_to_search:
                                            folder_full_path=os.path.join(folder_path, folder)

                                            for root,dirs,file in os.walk(folder_full_path):
                                                for file in files:
                                                    if ".log" in file.lower():
                                                    #    source_folder=os.path.basename(root)
                                                       results.append([
                                            parts[0],  # Timestamp
                                            parts[1],  # Log Type
                                            folder,    # subfolders 
                                            parts[3],  # Session
                                            parts[4],  # Method
                                            parts[5][:100]  # Details (shortened)
                                        ])
                                                       

                        except Exception as e:
                            st.error(f"Error reading {file}: {e}")
                            # continue

        if results:

            df = pd.DataFrame(
                results,
                columns=[
                    "DATE",
                    "Log Type",
                    "source ",
                    "Session",
                    "Method",
                    "Details"
                ]
            )
            st.session_state["results_df"]=df
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.success(f"{len(df)} records found")

        else:
            st.warning("No matching logs found.")





           
           
           
           
if "results_df" in st.session_state:

    df = st.session_state["results_df"]

    rows_per_page = 50

    total_pages = max(
        1,
        (len(df) - 1) // rows_per_page + 1
    )

    page = st.selectbox(
        "Page",
        range(1, total_pages + 1)
    )

    start_row = (page - 1) * rows_per_page
    end_row = start_row + rows_per_page

    st.write(
        f"Showing {start_row + 1} to {min(end_row, len(df))} of {len(df)} records"
    )

    st.dataframe(
        df.iloc[start_row:end_row],
        use_container_width=True,
        hide_index=True,
        height=500
    )






    