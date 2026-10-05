import pandas as pd
import streamlit as st

from database.db import query

st.title("📈 Operations Insights")
st.subheader("Courier performance")
st.caption("Current shipment outcomes by courier. These are synthetic demo records, not live carrier data.")

performance = pd.DataFrame([dict(row) for row in query("""
    SELECT
        courier,
        COUNT(*) AS total_shipments,
        SUM(CASE WHEN status IN ('Picked Up', 'Shipped') THEN 1 ELSE 0 END) AS confirmed_pickups,
        SUM(CASE WHEN status = 'Missed Pickup' THEN 1 ELSE 0 END) AS missed_pickups,
        SUM(CASE WHEN status = 'Ready for Pickup' THEN 1 ELSE 0 END) AS ready_for_pickup
    FROM shipments
    GROUP BY courier
    ORDER BY total_shipments DESC, courier
""")])

if performance.empty:
    st.info("No shipment outcomes are available yet.")
    st.stop()

performance["completed_outcomes"] = performance["confirmed_pickups"] + performance["missed_pickups"]
performance["confirmation_rate"] = performance.apply(
    lambda row: f"{row['confirmed_pickups'] / row['completed_outcomes']:.0%}"
    if row["completed_outcomes"]
    else "No outcomes",
    axis=1,
)

summary_cols = st.columns(4)
summary_cols[0].metric("Shipments", int(performance["total_shipments"].sum()))
summary_cols[1].metric("Pickups confirmed", int(performance["confirmed_pickups"].sum()))
summary_cols[2].metric("Missed pickups", int(performance["missed_pickups"].sum()))
summary_cols[3].metric("Ready for pickup", int(performance["ready_for_pickup"].sum()))

display = performance.rename(columns={
    "courier": "Courier",
    "total_shipments": "Shipments",
    "confirmed_pickups": "Confirmed Pickups",
    "missed_pickups": "Missed Pickups",
    "ready_for_pickup": "Ready for Pickup",
    "confirmation_rate": "Pickup Confirmation Rate",
})
st.dataframe(
    display[["Courier", "Shipments", "Confirmed Pickups", "Missed Pickups", "Ready for Pickup", "Pickup Confirmation Rate"]],
    width="stretch",
    hide_index=True,
)

st.bar_chart(
    display.set_index("Courier")[["Confirmed Pickups", "Missed Pickups"]],
    horizontal=True,
)
st.caption(
    "Pickup confirmation rate = confirmed pickups ÷ (confirmed pickups + missed pickups). Ready and packing shipments are excluded until an outcome is recorded. Actual pickup timestamps are not stored, so average delay is not reported."
)