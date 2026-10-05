
import streamlit as st
import pandas as pd
from database.db import query
from datetime import datetime
from services.sla import classify_sla, format_time_remaining

st.title("📋 Orders")

orders = pd.DataFrame([dict(r) for r in query("SELECT * FROM orders ORDER BY priority DESC, due_at")])

if orders.empty:
    st.warning("No orders found.")
    st.stop()

now = datetime.now()
sla_results = orders.apply(
    lambda row: classify_sla(row["due_at"], row["priority"], row["status"], now),
    axis=1,
)
orders["SLA Risk"] = [result[0] for result in sla_results]
orders["Time Remaining"] = [format_time_remaining(result[1]) for result in sla_results]

col1, col2, col3, col4 = st.columns(4)
with col1:
    priority_filter = st.selectbox("Priority", ["All", "High", "Normal"])
with col2:
    status_filter = st.selectbox("Status", ["All"] + sorted(orders["status"].unique().tolist()))
with col3:
    search = st.text_input("Search Order / Customer")
with col4:
    sla_filter = st.selectbox("SLA Risk", ["All", "Delayed", "Critical", "At Risk", "On Track", "Complete"])

filtered = orders.copy()
if priority_filter != "All":
    filtered = filtered[filtered["priority"] == priority_filter]
if status_filter != "All":
    filtered = filtered[filtered["status"] == status_filter]
if sla_filter != "All":
    filtered = filtered[filtered["SLA Risk"] == sla_filter]
if search:
    mask = (
        filtered["order_id"].str.contains(search, case=False, na=False)
        | filtered["customer_name"].str.contains(search, case=False, na=False)
    )
    filtered = filtered[mask]

st.caption(f"Showing {len(filtered)} of {len(orders)} orders")

st.dataframe(
    filtered[[
        "order_id", "customer_name", "channel", "priority",
        "status", "SLA Risk", "Time Remaining", "created_at", "due_at", "courier", "total_items"
    ]].rename(columns={
        "order_id": "Order",
        "customer_name": "Customer",
        "channel": "Channel",
        "priority": "Priority",
        "status": "Status",
        "created_at": "Created",
        "due_at": "Due",
        "courier": "Courier",
        "total_items": "Items"
    }),
    width="stretch",
    hide_index=True
)

if filtered.empty:
    st.info("No orders match the current filters, so there is no journey to display.")
    st.stop()

st.divider()
st.subheader("Order Timeline")
selected_order_id = st.selectbox("Select an order journey", filtered["order_id"].tolist())
selected_order = filtered[filtered["order_id"] == selected_order_id].iloc[0]
shipment_rows = query(
    "SELECT courier, staging_location, pickup_window, status FROM shipments WHERE order_id = ? LIMIT 1",
    (selected_order_id,),
)
shipment = dict(shipment_rows[0]) if shipment_rows else None
shipment_status = shipment["status"] if shipment else None
inventory_rows = query(
    """
    SELECT
        oi.sku,
        oi.quantity AS required_qty,
        COALESCE(main.quantity, 0) AS main_qty,
        COALESCE(secondary.quantity, 0) AS secondary_qty,
        EXISTS (
            SELECT 1 FROM transfers t
            WHERE t.sku = oi.sku AND t.status IN ('Pending', 'In Transit')
        ) AS transfer_pending
    FROM order_items oi
    LEFT JOIN inventory main ON main.sku = oi.sku AND main.warehouse = 'Main Warehouse'
    LEFT JOIN inventory secondary ON secondary.sku = oi.sku AND secondary.warehouse = 'Secondary Warehouse'
    WHERE oi.order_id = ?
    """,
    (selected_order_id,),
)
open_exceptions = query(
    "SELECT type, priority FROM exceptions WHERE order_id = ? AND status != 'Resolved' ORDER BY created_at",
    (selected_order_id,),
)

summary_cols = st.columns(5)
summary_cols[0].metric("Order", selected_order_id)
summary_cols[1].metric("Customer", selected_order["customer_name"])
summary_cols[2].metric("Priority", selected_order["priority"])
summary_cols[3].metric("Current status", selected_order["status"])
summary_cols[4].metric("SLA risk", selected_order["SLA Risk"])

stock_warnings = []
for row in inventory_rows:
    shortage = int(row["required_qty"]) - int(row["main_qty"])
    if shortage > 0:
        if row["transfer_pending"]:
            action = "transfer pending"
        elif int(row["secondary_qty"]) >= shortage:
            action = "transfer available"
        else:
            action = "no secondary stock available"
        stock_warnings.append(f"{row['sku']}: short {shortage} ({action})")

if stock_warnings:
    st.warning("Inventory risk: " + "; ".join(stock_warnings))
if open_exceptions:
    exception_summary = "; ".join(f"{row['type']} ({row['priority']})" for row in open_exceptions)
    st.warning("Open exceptions: " + exception_summary)
if shipment:
    st.caption(
        f"Courier: {shipment['courier']} | Staging: {shipment['staging_location']} | "
        f"Pickup window: {shipment['pickup_window']} | Shipment status: {shipment_status}"
    )
else:
    st.caption("No shipment is assigned to this order yet.")

step_names = [
    "Order received",
    "Processing",
    "Picking",
    "Packing",
    "Staging",
    "Ready for pickup",
    "Picked up",
    "Shipped",
]
order_step = {"Processing": 1, "Picking": 2, "Packing": 3, "Staging": 4, "Shipped": 7}
if selected_order["status"] == "Shipped" or shipment_status == "Shipped":
    current_step = 7
elif shipment_status in {"Picked Up", "Missed Pickup"}:
    current_step = 6
elif shipment_status == "Ready for Pickup":
    current_step = 5
else:
    current_step = order_step.get(selected_order["status"], 1)

timeline_rows = []
for index, step in enumerate(step_names):
    if shipment_status == "Missed Pickup" and index == 6:
        state = "Missed"
    elif current_step == 7 or index < current_step:
        state = "Complete"
    elif index == current_step:
        state = "Current"
    else:
        state = "Pending"

    if step == "Order received":
        detail = f"Created {selected_order['created_at']}"
    elif step == "Staging" and shipment and shipment["staging_location"]:
        detail = f"Location {shipment['staging_location']}"
    elif step == "Ready for pickup" and shipment:
        detail = f"{shipment['courier']} · window {shipment['pickup_window']}"
    elif step == "Picked up" and shipment_status in {"Picked Up", "Shipped"}:
        detail = "Pickup confirmed; event time not stored"
    elif step == "Picked up" and shipment_status == "Missed Pickup":
        detail = "Pickup missed; follow up in Exceptions"
    elif step == "Shipped" and current_step == 7:
        detail = "Order marked shipped; event time not stored"
    else:
        detail = "No event timestamp stored"

    timeline_rows.append({"Milestone": step, "Progress": state, "Recorded detail": detail})

st.dataframe(pd.DataFrame(timeline_rows), width="stretch", hide_index=True)
st.caption(
    "Progress is inferred from the current order and shipment statuses. The database stores order creation, due time, and pickup window, but not timestamps for each status transition."
)
