import streamlit as st     
import json
import os
from datetime import datetime, date
import pandas as pd


st.set_page_config(
    page_title="Log Reader",
    page_icon="📁",
    layout="wide"
)


#========== CONFIG A FILE ==========
with open("config.json", "r") as file:
    config = json.load(file)

folder_path = config["default_folder"]
ROWS_PER_PAGE = config["ROWS_PER_PAGE"]


# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>


            
/* Main Background */
.stApp{
    background:
        radial-gradient(circle at top left, #1e3a8a 0%, transparent 35%),
        radial-gradient(circle at top right, #7c3aed 0%, transparent 35%),
        radial-gradient(circle at bottom left, #0891b2 0%, transparent 35%),
        #020617;
}

/* Header */
.title-box{
    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed,
        #ec4899
    );

    color:white;
    padding:25px;
    border-radius:20px;
    text-align:center;
    font-size:48px;
    font-weight:bold;

    box-shadow:
        0px 0px 20px rgba(124,58,237,0.5);
}

# /* Labels */
# label,
# .stDateInput label,
# .stMultiSelect label{
#     color:#38bdf8 !important;
#     font-size:18px !important;
#     font-weight:bold !important;
#     text-transform:uppercase;
# }

   div[data-testid="stWidgetLabel"] label{
    color:#38bdf8 !important;
    font-size:16px !important;
    font-weight:bold !important;
}         

/* Date Box */
.stDateInput input{
    background:#1e293b !important;
    color:#f8fafc !important;
    border:2px solid #38bdf8 !important;
    border-radius:10px !important;
            
}
/* Select Folder & Type Box */
div[data-testid="stMultiSelect"] > div {
    background: #1e293b !important;
    border: 2px solid #38bdf8 !important;
    border-radius: 10px !important;
}

/* Focus effect */
div[data-testid="stMultiSelect"] > div:focus-within {
    border: 2px solid #38bdf8 !important;
    box-shadow: 0 0 8px #38bdf8 !important;
}

/* Text color */
div[data-testid="stMultiSelect"] span {
    color: white !important;
}

/* Dropdown */
.stMultiSelect{
    color:white !important;
}

/* Search Button */
.stButton > button{
    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );

    color:white;
    border:none;
    border-radius:12px;
    font-size:18px;
    font-weight:bold;
    height:50px;

    box-shadow:
        0px 0px 15px rgba(124,58,237,0.4);
}

.stButton > button:hover{
    background: linear-gradient(
        90deg,
        #7c3aed,
        #ec4899
    );

    transform:scale(1.05);
}

/* Dashboard Cards */
.metric-card{
    background:
        linear-gradient(
            145deg,
            rgba(30,41,59,0.95),
            rgba(15,23,42,0.95)
        );

    border:1px solid #475569;

    border-radius:5px;

    box-shadow:
        0px 8px 25px rgba(0,0,0,0.4);

    padding:5px;
}

/* Card Titles */
.metric-title{
    color:#38bdf8;
    font-size:20px;
    font-weight:bold;
}

/* Card Values */
.metric-value{
    color:white;
    font-size:20px;
    font-weight:bold;
}

/* Pagination */
h1{
    color:#38bdf8 !important;
}
            

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    '<div class="title-box">📁 Log Reader </div>',
    unsafe_allow_html=True
)

# ========== SELECT A FOLDER ==========


def get_folders(folder_path):
    folders =[]
    
    for item in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path,item)):
            folders.append(item)
    return folders

folders = get_folders(folder_path)

# #========== TYPE FILTER ==========
type_options = ["Error", "Info", "Warn"]

def folder_changed():
    selected = st.session_state.folder_select

    # If nothing selected -> All
    if not selected:
        st.session_state.folder_select = ["All"]
        return

    # If All + others selected
    if "All" in selected and len(selected) > 1:
        if selected[-1] == "All":
            # User clicked All last
            st.session_state.folder_select = ["All"]
        else:
            # User clicked another folder
            st.session_state.folder_select = [
                x for x in selected if x != "All"
            ]


def type_changed():
    selected = st.session_state.type_select

    if not selected:
        st.session_state.type_select = ["All"]
        return

    if "All" in selected and len(selected) > 1:
        if selected[-1] == "All":
            st.session_state.type_select = ["All"]
        else:
            st.session_state.type_select = [
                x for x in selected if x != "All"
            ]

# -----------------------------
# FILTERS
# -----------------------------
col1,col2,col3,col4,col5 = st.columns([2,2,2,2,1])

with col1:
    date_from = st.date_input(
        "DATE FROM",
        value=date.today()
    )

with col2:
    date_to = st.date_input(
        "DATE TO",
        value=date.today()
    )

with col3:

    folder = st.multiselect(
        "SELECT FOLDER",
        ["All"] + folders,
        default=["All"],
        key="folder_select",
        on_change=folder_changed
    )
with col4:

    log_type = st.multiselect(
        "TYPE",
        ["All", "INFO", "WARNING", "ERROR"],
        default=["All"],
        key="type_select",
        on_change=type_changed
    )

# Folder filter
if not folder or "All" in folder:
    folders_to_search = folders
else:
    folders_to_search = folder

# Type filter
if not log_type or "All" in log_type:
    types_to_search = []
else:
    types_to_search = log_type

with col5:
    st.write("")
    st.write("")
    search_clicked = st.button(
        "🔍 Search",
        use_container_width=True
    )

    

#========== SEARCH SECTION ==========
if search_clicked:

    if date_from > date_to:
        st.error("Invalid date range!")
        st.stop()

    else:

        results = []

        for folder in folders_to_search:        #ALL SECTION (selcted_folders=> Folders_to_search)=

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
                                    if types_to_search:  #ALL SECTION (selected_types=>types_to_search)

                                        match_found = False

                                        for log_type in types_to_search:  #ALL SECTION (selected_types=>types_to_search)

                                            if f"| {log_type.upper()} |" in line.upper():
                                                match_found = True
                                                break

                                        if not match_found:
                                            continue

                                    parts = [x.strip() for x in line.split("|")]

                                    if len(parts) >= 6:

                                        try:
                                            log_date = datetime.strptime(
                                                parts[0][:8],
                                                "%Y%m%d"
                                            ).date()
                                            if date_from > date_to:
                                                st.error("Invalid date range!")
                                                st.stop()

                                            # DATE FILTER
                                            if (
                                                log_date < date_from
                                                or
                                                log_date > date_to
                                            ):
                                                continue

                                        except:
                                            continue

                                        results.append([
                                            parts[0],  # Timestamp
                                            parts[1],  # Log Type
                                            folder,  # Source
                                            parts[3],  # Session
                                            parts[4],  # Method
                                            parts[5][:100]  # Details (shortened)
                                        ])

                        except Exception as e:
                            st.error(f"Error reading {file}: {e}")

        if results:

            df = pd.DataFrame(
                results,
                columns=[
                    "DATE",
                    "Log Type",
                    "Source",
                    "Session",
                    "Method",
                    "Details"
                ]
            )

            # -------------------------
            # DASHBOARD
            # -------------------------

            c1,c2,c3,c4 = st.columns(4)

            with c1:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-title">📄 Total Logs</div>
                    <div class="metric-value">16376</div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-title">ℹ️ Info</div>
                    <div class="metric-value">16344</div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-title">⚠️ Warnings</div>
                    <div class="metric-value">0</div>
                </div>
                """, unsafe_allow_html=True)

            with c4:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-title">❌ Errors</div>
                    <div class="metric-value">32</div>
                </div>
                """, unsafe_allow_html=True)

            st.write("")


           # Save DataFrame
            st.session_state["result_df"] = df
            st.session_state.search_done = True
            
            if "result_df" in st.session_state:

                df = st.session_state["result_df"]

                # ROWS_PER_PAGE = 20
                total_pages = max(
                    1,
                    (len(df) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE
                )

                if "page" not in st.session_state:
                    st.session_state.page = 1

                # -------------------------
                # PAGINATION ABOVE TABLE
                # -------------------------

                left, mid, right = st.columns([1, 3, 1])

                with left:
                    if st.button("⬅ Previous"):
                        if st.session_state.page > 1:
                            st.session_state.page -= 1

                with mid:
                    st.markdown(
                        f"""
                        <h3 style='text-align:center;color:white;'>
                        Page {st.session_state.page} of {total_pages}
                        </h3>
                        """,
                        unsafe_allow_html=True
                    )

                with right:
                    if st.button("Next ➡"):
                        if st.session_state.page < total_pages:
                            st.session_state.page += 1

                start_idx = (
                    (st.session_state.page - 1)
                    * ROWS_PER_PAGE
                )

                end_idx = start_idx + ROWS_PER_PAGE

                page_df = df.iloc[start_idx:end_idx]

                # -------------------------
                # RESULTS HEADING
                # -------------------------

                st.markdown("""
                <h3 style='
                text-align:center;
                background-color:#1f4e79;
                color:white;
                padding:10px;
                border-radius:10px;'>
                📊 Results
                </h3>
                """, unsafe_allow_html=True)



            st.markdown("""
                <style>

                /* Keep dataframe toolbar visible */
                [data-testid="stDataFrame"] [data-testid="stElementToolbar"] {
                    opacity: 1 !important;
                    visibility: visible !important;
                    display: flex !important;
                }

                /* Keep toolbar visible even when not hovering */
                [data-testid="stDataFrame"] .stElementToolbar {
                    opacity: 1 !important;
                    visibility: visible !important;
                }

                </style>
                """, unsafe_allow_html=True)
            
            

            st.dataframe(
                    page_df,
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.warning("⚠️ No matching logs found.")