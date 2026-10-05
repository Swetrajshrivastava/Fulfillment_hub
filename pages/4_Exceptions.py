import pandas as pd
import streamlit as st

from database.db import execute, query

st.title("⚠️ Exception Management")
st.caption("Review operational issues, assign an owning team, and track resolution.")

exceptions = pd.DataFrame([dict(row) for row in query(
    "SELECT * FROM exceptions ORDER BY CASE priority WHEN 'Critical' THEN 0 WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END, created_at"
)])

if exceptions.empty:
    st.success("No exceptions have been recorded.")
    st.stop()

exceptions["status_display"] = exceptions["status"].replace({"Assigned": "In Progress"})

filter_cols = st.columns(3)
with filter_cols[0]:
    status_filter = st.selectbox("Status", ["All", "Open", "In Progress", "Resolved"])
with filter_cols[1]:
    priority_filter = st.selectbox("Priority", ["All"] + sorted(exceptions["priority"].dropna().unique().tolist()))
with filter_cols[2]:
    search = st.text_input("Search exception / order / issue")

filtered = exceptions.copy()
if status_filter != "All":
    filtered = filtered[filtered["status_display"] == status_filter]
if priority_filter != "All":
    filtered = filtered[filtered["priority"] == priority_filter]
if search:
    search_columns = ["exception_id", "order_id", "type", "assigned_to"]
    matches = pd.Series(False, index=filtered.index)
    for column in search_columns:
        matches |= filtered[column].fillna("").astype(str).str.contains(search, case=False, na=False)
    filtered = filtered[matches]

st.caption(f"Showing {len(filtered)} of {len(exceptions)} exceptions")
st.dataframe(
    filtered[["exception_id", "type", "order_id", "priority", "status_display", "assigned_to", "created_at"]].rename(columns={
        "exception_id": "ID",
        "type": "Issue",
        "order_id": "Order",
        "priority": "Priority",
        "status_display": "Status",
        "assigned_to": "Assigned Team",
        "created_at": "Created",
    }),
    width="stretch",
    hide_index=True,
)

if filtered.empty:
    st.info("No exceptions match those filters.")
    st.stop()

selected_id = st.selectbox("Select exception to manage", filtered["exception_id"].tolist())
selected = filtered[filtered["exception_id"] == selected_id].iloc[0]
st.subheader(f"{selected['type']} · {selected_id}")
st.write(selected["description"])
if pd.notna(selected["order_id"]):
    st.caption(f"Related order: {selected['order_id']} · Created: {selected['created_at']}")

if "courier" in str(selected["type"]).lower() or "pickup" in str(selected["type"]).lower():
    st.page_link("pages/3_Staging.py", label="View staging and courier")
elif "inventory" in str(selected["type"]).lower() or "stock" in str(selected["type"]).lower():
    st.page_link("pages/2_Inventory.py", label="View inventory")
else:
    st.page_link("pages/1_Orders.py", label="View orders")

status_options = ["Open", "In Progress", "Resolved"]
priority_options = ["Critical", "High", "Medium", "Low"]
selected_status = selected["status_display"]
if selected_status not in status_options:
    selected_status = "Open"
selected_priority = selected["priority"]
if selected_priority not in priority_options:
    priority_options.append(selected_priority)

with st.form("exception_update"):
    form_cols = st.columns(3)
    with form_cols[0]:
        new_status = st.selectbox("Status", status_options, index=status_options.index(selected_status))
    with form_cols[1]:
        new_priority = st.selectbox("Priority", priority_options, index=priority_options.index(selected_priority))
    with form_cols[2]:
        new_assignee = st.text_input("Assigned team", value=selected["assigned_to"] or "")
    save = st.form_submit_button("Save changes", width="stretch")

if save:
    execute(
        "UPDATE exceptions SET status = ?, priority = ?, assigned_to = ? WHERE exception_id = ?",
        (new_status, new_priority, new_assignee.strip() or None, selected_id),
    )
    st.success(f"{selected_id} updated.")
    st.rerun()

resolve_col, _ = st.columns(2)
with resolve_col:
    if st.button("Resolve", key=f"resolve_{selected_id}", width="stretch"):
        execute("UPDATE exceptions SET status = 'Resolved' WHERE exception_id = ?", (selected_id,))
        st.success(f"{selected_id} resolved.")
        st.rerun()