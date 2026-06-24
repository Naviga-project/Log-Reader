import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Log Folder Reader",
    page_icon="📁",
    layout="wide"
)

folder_path = r"D:\NavigaLog"

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

    border-radius:18px;

    box-shadow:
        0px 8px 25px rgba(0,0,0,0.4);

    padding:20px;
}

/* Card Titles */
.metric-title{
    color:#38bdf8;
    font-size:24px;
    font-weight:bold;
}

/* Card Values */
.metric-value{
    color:white;
    font-size:54px;
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
    '<div class="title-box">📁 Log Folder Reader</div>',
    unsafe_allow_html=True
)

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
    import os
    folder = [
        f for f in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path,f))
    ]

    folder = st.multiselect(
        "SELECT FOLDER",
        ["All"] + folder,
        default=["All"]
    )

with col4:
    log_type = st.multiselect(
        "TYPE",
        ["All","INFO","WARNING","ERROR"],
        default=["All"]
    )

with col5:
    st.write("")
    st.write("")
    search_clicked = st.button(
        "🔍 Search",
        use_container_width=True
    )

# -----------------------------
# SEARCH ACTION
# -----------------------------
if search_clicked:
    st.session_state.search_done = True
if "search_done" not in st.session_state:
    st.session_state.search_done = False
if st.session_state.search_done:




    # -------------------------
    # DATABASE / LOG FILE DATA
    # Replace with your actual data
    # -------------------------

    rows = 500

    df = pd.DataFrame({
        "DATE":[f"20260317_02:37:{i%60:02d},715" for i in range(rows)],
        "Log Type":["INFO"]*rows,
        "Source":["Applepay"]*rows,
        "Session":[f"TestClient.{i}" for i in range(rows)],
        "Method":["subscriptionpanel"]*rows,
        "Details":["Bearer XXXXXXXX TOKEN"]*rows
    })

    st.divider()

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

    # -------------------------
    # PAGINATION
    # -------------------------

    PAGE_SIZE = 20
    # total_pages = max.ceil(6000/20)

    if "page" not in st.session_state:
        st.session_state.page = 1

    total_pages = max(
        1,
        int(np.ceil(len(df)/PAGE_SIZE))
    )

    left,mid,right = st.columns([1,3,1])

    with left:
        if st.button("⬅ Previous"):
            if st.session_state.page > 1:
                st.session_state.page -= 1

    with mid:
        st.markdown(
            f"<h1 style='text-align:center;color:white;'>Page {st.session_state.page} of {total_pages}</h1>",
            unsafe_allow_html=True
        )

    with right:
        if st.button("Next ➡"):
            if st.session_state.page < total_pages:
                st.session_state.page += 1

    start = (st.session_state.page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    ROWS_PER_PAGE = 20
    total_pages = max(
        1,
        (len(df) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE
    )

    if "page" not in st.session_state:
        st.session_state.page = 1

        # -------------------------
    # TABLE
    # -------------------------
    st.dataframe(
        df.iloc[start:end],
        use_container_width=True,
        height=600
    )

# else:

st.info(
        "🔍 Select filters and click Search to load Dashboard and Table."
    )