# <<<<<<< HEAD
import streamlit as st
import os
import pandas as pd
from datetime import datetime

# ==========================================
# 1. PAGE STYLING & SETUP
# ==========================================
st.set_page_config(layout="wide") # Optional: makes the app wider to fit logs better

st.markdown("""
<style>
div[data-testid="stDateInput"] {
    width: 150px !important;
}
div[data-testid="stMultiSelect"] {
    width: 150px !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. GET FOLDERS FUNCTION
# ==========================================
folder_path = r"D:\Coding\gauri\NavigaLog"

def get_folders(path):
    folders = []
    # Added a check just in case the path doesn't exist yet
    if os.path.exists(path):
        for item in os.listdir(path):
            if os.path.isdir(os.path.join(path, item)):
                folders.append(item)
    return folders

folders = get_folders(folder_path)
type_options = ["Error", "Info", "Warn"]

# ==========================================
# 3. FILTERS (DATES, FOLDERS, TYPES)
# ==========================================
col1, col2 = st.columns(2)

with col1:
    date_from = st.date_input("DATE FROM")
    selected_folder = st.multiselect(
        "Select Folder",
        options=["All"] + folders,
        default=["All"]
    )

with col2:
    date_to = st.date_input("DATE TO")
    selected_types = st.multiselect(
        "Type",
        options=["All"] + type_options,
        default=["All"]
    )

# Handle "All" selections
folders_to_search = folders if "All" in selected_folder else selected_folder
types_to_search = [] if "All" in selected_types else selected_types

# ==========================================
# 4. SEARCH LOGIC
# ==========================================
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
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
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
                                            # Example: 20260317_03:06:45,290
                                            log_date = datetime.strptime(parts[0][:8], "%Y%m%d").date()
                                            if date_from > date_to:
                                                st.error("Invalid date range!")
                                                st.stop()
                                                
                                                      # DATE FILTER
                                            if log_date < date_from or log_date > date_to:
                                                continue
                                                
                                        except:
                                            continue

                                        results.append([
                                            parts[0],        # Timestamp
                                            parts[1],        # Log Type
                                            folder,              # Source
                                            parts[3],        # Session
                                            parts[4],        # Method
                                            parts[5][:100]   # Details (shortened)
                                        ])

                        except Exception as e:
                            st.error(f"Error reading {file}: {e}")

        # Save results to session state
        if results:
            df = pd.DataFrame(
                results,
                columns=["DATE", "Log Type", "source ", "Session", "Method", "Details"]
            )
            st.session_state["results_df"] = df
            st.success(f"{len(df)} records found")
        else:
            st.warning("No matching logs found.")
            # Clear previous state if search returns empty
            if "results_df" in st.session_state:
                del st.session_state["results_df"]



                # ==========================================
# 5. DASHBOARD & PAGINATION DISPLAY
# ==========================================
if "results_df" in st.session_state:

    df = st.session_state["results_df"]

    # --- TOP DASHBOARD METRICS ---
    st.markdown("### 📊 Overall Log Summary")

    error_total = len(df[df["Log Type"].str.contains("ERROR", case=False, na=False)])
    warn_total = len(df[df["Log Type"].str.contains("WARN", case=False, na=False)])
    info_total = len(df[df["Log Type"].str.contains("INFO", case=False, na=False)])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🚨 Total Errors", error_total)

    with col2:
        st.metric("⚠️ Total Warnings", warn_total)

    with col3:
        st.metric("ℹ️ Total Info", info_total)

    st.markdown("---")

    # ==========================================
    # PAGINATION
    # ==========================================
    rows_per_page = 50
    total_pages = max(1, (len(df) - 1) // rows_per_page + 1)

    # Save current page in session
    if "page" not in st.session_state:
        st.session_state.page = 1

    current_page = st.session_state.page

    # Pagination Buttons
    pcol1, pcol2, pcol3, pcol4, pcol5, pcol6, pcol7, pcol8 = st.columns(8)

    # Previous Button
    with pcol1:
        if st.button("⬅ Previous"):
            if current_page > 1:
                st.session_state.page -= 1
                st.rerun()

    # Page 1
    with pcol2:
        if st.button("1"):
            st.session_state.page = 1
            st.rerun()

    # Page 2
    with pcol3:
        if total_pages >= 2:
            if st.button("2"):
                st.session_state.page = 2
                st.rerun()

    # Page 3
    with pcol4:
        if total_pages >= 3:
            if st.button("3"):
                st.session_state.page = 3
                st.rerun()

    # Dots
    with pcol5:
        if total_pages > 4:
            st.write("...")

    # Last Page
    with pcol6:
        if total_pages > 3:
            if st.button(str(total_pages)):
                st.session_state.page = total_pages
                st.rerun()

    # Next Button
    with pcol8:
        if st.button("Next ➡"):
            if current_page < total_pages:
                st.session_state.page += 1
                st.rerun()

    current_page = st.session_state.page

    # Records for current page
    start_row = (current_page - 1) * rows_per_page
    end_row = start_row + rows_per_page

    st.write(
        f"Showing {start_row + 1} to "
        f"{min(end_row, len(df))} of "
        f"{len(df)} records"
    )

    # Display Table
    st.dataframe(
        df.iloc[start_row:end_row],
        use_container_width=True,
        hide_index=True,
        height=500
    )





# ggfrgeruogerghavuethgifds

