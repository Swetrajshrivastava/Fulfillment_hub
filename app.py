
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from database.db import query
from services.sla import classify_sla, format_time_remaining

st.set_page_config(page_title="Fulfillment Hub", page_icon="📦", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
.metric-card {padding: 1rem; border-radius: 10px; border: 1px solid #ddd;}
.small-muted {color: #666; font-size: 0.9rem;}
</style>
""", unsafe_allow_html=True)

st.title("📦 Fulfillment Hub")
st.caption("Operations dashboard for XYZ's order fulfillment workflow")

orders = pd.DataFrame([dict(r) for r in query("SELECT * FROM orders")])
exceptions = pd.DataFrame([dict(r) for r in query("SELECT * FROM exceptions")])
shipments = pd.DataFrame([dict(r) for r in query("SELECT * FROM shipments")])

inventory_risk_sql = """
SELECT DISTINCT o.order_id
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
LEFT JOIN inventory main ON main.sku = oi.sku AND main.warehouse = 'Main Warehouse'
WHERE COALESCE(main.quantity, 0) < oi.quantity
    AND o.status != 'Shipped'
ORDER BY o.order_id
"""

inventory_risk_orders = [r["order_id"] for r in query(inventory_risk_sql)]

now = datetime.now()
orders["due_dt"] = pd.to_datetime(orders["due_at"])
sla_results = orders.apply(
    lambda row: classify_sla(row["due_at"], row["priority"], row["status"], now),
    axis=1,
)
orders["sla_status"] = [result[0] for result in sla_results]
orders["minutes_remaining"] = [result[1] for result in sla_results]
orders["time_remaining"] = orders["minutes_remaining"].apply(format_time_remaining)
orders["priority"] = pd.Categorical(orders["priority"], categories=["High", "Normal"], ordered=True)

ready_for_pickup = int((shipments["status"] == "Ready for Pickup").sum()) if not shipments.empty else 0
missed_pickup = int((shipments["status"] == "Missed Pickup").sum()) if not shipments.empty else 0

total_orders = len(orders)
priority_orders = int((orders["priority"] == "High").sum())
delayed_orders = int((orders["sla_status"] == "Delayed").sum())
at_risk_orders = int(orders["sla_status"].isin(["Critical", "At Risk"]).sum())
open_exceptions = int((exceptions["status"] != "Resolved").sum())
inventory_mismatches = len(inventory_risk_orders)

transfer_waiting_sql = """
SELECT DISTINCT o.order_id
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN transfers t ON t.sku = oi.sku AND t.status IN ('Pending', 'In Transit')
LEFT JOIN inventory main ON main.sku = oi.sku AND main.warehouse = 'Main Warehouse'
WHERE COALESCE(main.quantity, 0) < oi.quantity
    AND o.status != 'Shipped'
ORDER BY o.order_id
"""
transfer_waiting_orders = [r["order_id"] for r in query(transfer_waiting_sql)]

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Orders", total_orders)
c2.metric("Priority Orders", priority_orders)
c3.metric("Delayed Orders", delayed_orders, delta="Needs attention" if delayed_orders else None, delta_color="inverse")
c4.metric("Open Exceptions", open_exceptions)
c5.metric("Stock Risk Orders", inventory_mismatches)
c6.metric("Ready for Pickup", ready_for_pickup, delta="Missed" if missed_pickup else None, delta_color="inverse")

st.divider()

st.subheader("Action Required")
st.caption("Prioritized from live order, inventory, transfer, shipment, and exception records.")
action_cols = st.columns(5)
action_items = [
    ("Delayed orders", delayed_orders, "pages/1_Orders.py"),
    ("SLA at risk", at_risk_orders, "pages/1_Orders.py"),
    ("Awaiting transfer", len(transfer_waiting_orders), "pages/2_Inventory.py"),
    ("Missed pickups", missed_pickup, "pages/3_Staging.py"),
    ("Open exceptions", open_exceptions, "pages/4_Exceptions.py"),
]
for column, (label, count, page) in zip(action_cols, action_items):
    with column:
        st.metric(label, count)
        st.page_link(page, label="Review")

st.caption("SLA rule: overdue orders are Delayed; within 30 minutes is Critical; High priority is At Risk within 2 hours and Normal within 1 hour.")

st.divider()

left, right = st.columns([1.35, 1])

with left:
    st.subheader("🚨 SLA risk queue")

    attention = orders[orders["sla_status"].isin(["Delayed", "Critical", "At Risk"])].copy()
    attention["sla_sort"] = attention["sla_status"].map({"Delayed": 0, "Critical": 1, "At Risk": 2})
    attention = attention.sort_values(["sla_sort", "priority", "due_dt"])

    display = attention[["order_id", "priority", "status", "sla_status", "time_remaining", "due_at"]].head(12)
    st.dataframe(
        display.rename(columns={
            "order_id": "Order",
            "priority": "Priority",
            "status": "Status",
            "due_at": "Due",
            "sla_status": "SLA Risk",
            "time_remaining": "Time Remaining",
        }),
        width="stretch",
        hide_index=True
    )

with right:
    st.subheader("📊 Orders by status")
    status_counts = orders["status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Orders"]
    fig = px.bar(status_counts, x="Status", y="Orders")
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig, width="stretch")

st.divider()

st.subheader("⚠️ Open operational exceptions")
open_exc = exceptions[exceptions["status"] != "Resolved"].copy()
if open_exc.empty:
    st.success("No open exceptions.")
else:
    st.dataframe(
        open_exc[["exception_id", "order_id", "type", "priority", "status", "assigned_to"]].rename(
            columns={
                "exception_id": "ID",
                "order_id": "Order",
                "type": "Problem",
                "priority": "Priority",
                "status": "Status",
                "assigned_to": "Assigned To"
            }
        ),
        width="stretch",
        hide_index=True
    )

st.info("Design principle: the dashboard answers one question first — **what needs attention right now?**")

if inventory_mismatches:
    st.caption(f"Inventory risk flagged for {inventory_mismatches} order(s). Review the Inventory workflow for transfer action.")
