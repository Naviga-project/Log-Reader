col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.markdown(f"""
#     <div class="metric-card">
#         <h2>📄 Total Logs</h2>
#         <p>{total_logs}</p>
#     </div>
#     """, unsafe_allow_html=True)

# with col2:
#     st.markdown(f"""
#     <div class="metric-card">
#         <h2>ℹ️ Info</h2>
#         <p>{total_info}</p>
#     </div>
#     """, unsafe_allow_html=True)

# with col3:
#     st.markdown(f"""
#     <div class="metric-card">
#         <h2>⚠️ Warnings</h2>
#         <p>{total_warn}</p>
#     </div>
#     """, unsafe_allow_html=True)

# with col4:
#     st.markdown(f"""
#     <div class="metric-card">
#         <h2>❌ Errors</h2>
#         <p>{total_error}</p>
#     </div>
#     """, unsafe_allow_html=True)