import streamlit as st
import pandas as pd
from database.db import query, execute
from datetime import datetime

st.title("📦 Staging + Courier Pickup")

staging_sql = """
SELECT
    s.shipment_id,
    s.order_id,
    o.customer_name,
    s.courier,
    s.staging_location,
    s.pickup_window,
    s.status
FROM shipments s
JOIN orders o ON o.order_id = s.order_id
ORDER BY s.pickup_window ASC
"""

staging_df = pd.DataFrame([dict(r) for r in query(staging_sql)])

if staging_df.empty:
    st.info("No shipment records are currently available.")
    st.stop()

display_df = staging_df.rename(columns={
    "shipment_id": "Shipment",
    "order_id": "Order",
    "customer_name": "Customer",
    "courier": "Courier",
    "staging_location": "Location",
    "pickup_window": "Pickup Window",
    "status": "Status"
})

st.subheader("Staging board")
st.dataframe(display_df, width="stretch", hide_index=True)

selected = st.selectbox("Select a shipment to update", staging_df["order_id"].tolist())
selected_row = staging_df[staging_df["order_id"] == selected].iloc[0]

st.subheader(f"Shipment controls for {selected}")

location_options = ["A-01", "A-02", "A-03", "B-01", "B-02", "B-03", "C-01"]
courier_options = ["Delhivery", "Blue Dart", "DTDC", "Ecom Express"]
status_options = ["Packing", "Ready for Pickup", "Picked Up", "Missed Pickup", "Shipped"]
location_index = location_options.index(selected_row["staging_location"]) if selected_row["staging_location"] in location_options else 0
courier_index = courier_options.index(selected_row["courier"]) if selected_row["courier"] in courier_options else 0
status_index = status_options.index(selected_row["status"]) if selected_row["status"] in status_options else 0

with st.form("staging_form"):
    location = st.selectbox("Staging location", location_options, index=location_index)
    courier = st.selectbox("Courier", courier_options, index=courier_index)
    status = st.selectbox("Status", status_options, index=status_index)
    submitted = st.form_submit_button("Update shipment status")

if submitted:
    execute(
        "UPDATE shipments SET staging_location = ?, courier = ?, status = ? WHERE order_id = ?",
        (location, courier, status, selected),
    )
    st.success(f"Updated shipment status for {selected} to {status}.")

st.markdown("### Courier pickup monitor")
by_courier = staging_df.groupby("courier").agg(
    ready_orders=("status", lambda s: int((s == "Ready for Pickup").sum())),
    missed=("status", lambda s: int((s == "Missed Pickup").sum())),
    picked_up=("status", lambda s: int((s == "Picked Up").sum()))
).reset_index()
by_courier.columns = ["Courier", "Ready for Pickup", "Missed Pickup", "Picked Up"]
st.dataframe(by_courier, width="stretch", hide_index=True)

missed = staging_df[staging_df["status"] == "Missed Pickup"].copy()
missed = missed.rename(columns={
    "order_id": "Order",
    "courier": "Courier",
    "staging_location": "Location",
    "pickup_window": "Pickup Window",
    "status": "Status"
})

if not missed.empty:
    st.warning(f"Pickup missed scenario detected for {len(missed)} order(s).")
    st.dataframe(missed[["Order", "Courier", "Location", "Pickup Window", "Status"]], width="stretch", hide_index=True)
    if st.button("Create missed-pickup exception"):
        created = 0
        for _, row in missed.iterrows():
            existing = query(
                "SELECT 1 FROM exceptions WHERE order_id = ? AND type = 'Courier pickup risk' AND status != 'Resolved' LIMIT 1",
                (row["Order"],),
            )
            if existing:
                continue
            execute(
                """
                INSERT INTO exceptions (exception_id, order_id, sku, type, description, priority, status, created_at, assigned_to)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"EXC-{datetime.now().strftime('%Y%m%d%H%M%S')}-{row['Order']}",
                    row["Order"],
                    None,
                    "Courier pickup risk",
                    f"Courier {row['Courier']} missed the pickup window for staging location {row['Location']}.",
                    "High",
                    "Open",
                    datetime.now().isoformat(timespec="minutes"),
                    "Dispatch Team",
                )
            )
            created += 1
        if created:
            st.success(f"Created {created} missed-pickup exception(s).")
        else:
            st.info("Open missed-pickup exceptions already exist.")

st.caption("This flow covers packing → staging → ready-for-pickup → picked up → shipped, with deliberate risk cases for demonstration.")
