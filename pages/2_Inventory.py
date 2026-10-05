import streamlit as st
import pandas as pd
from datetime import datetime

from database.db import query, execute

st.title("📦 Inventory Mismatch & Transfer")

picking_risk_sql = """
SELECT
    o.order_id,
    o.customer_name,
    o.priority,
    o.status,
    o.due_at,
    oi.sku,
    p.product_name,
    p.variant,
    oi.quantity AS required_qty,
    COALESCE(main.quantity, 0) AS main_qty,
    COALESCE(sec.quantity, 0) AS secondary_qty,
    COALESCE(main.quantity, 0) - oi.quantity AS shortage_qty
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.sku = oi.sku
LEFT JOIN inventory main ON main.sku = oi.sku AND main.warehouse = 'Main Warehouse'
LEFT JOIN inventory sec ON sec.sku = oi.sku AND sec.warehouse = 'Secondary Warehouse'
WHERE COALESCE(main.quantity, 0) < oi.quantity
    AND o.status != 'Shipped'
ORDER BY o.due_at ASC, o.order_id ASC
"""

risk_df = pd.DataFrame([dict(r) for r in query(picking_risk_sql)])

if risk_df.empty:
    st.success("No inventory shortages currently flagged for active orders.")
    st.stop()

risk_df["shortage_qty"] = (risk_df["required_qty"] - risk_df["main_qty"]).clip(lower=0)

order_ids = sorted(risk_df["order_id"].unique().tolist())
selected_order = st.selectbox("Select order with stock risk", order_ids)

order_rows = risk_df[risk_df["order_id"] == selected_order].copy()

st.subheader(f"Order {selected_order}")

meta_cols = st.columns([1.2, 1.2, 1, 1])
with meta_cols[0]:
    st.metric("Customer", order_rows.iloc[0]["customer_name"])
with meta_cols[1]:
    st.metric("Priority", order_rows.iloc[0]["priority"])
with meta_cols[2]:
    st.metric("Status", order_rows.iloc[0]["status"])
with meta_cols[3]:
    st.metric("Due", order_rows.iloc[0]["due_at"])

st.markdown("### Stock mismatch details")
show_df = order_rows[["sku", "product_name", "variant", "required_qty", "main_qty", "secondary_qty", "shortage_qty"]].copy()
show_df.columns = ["SKU", "Product", "Variant", "Required", "Main WH", "Secondary WH", "Shortage"]
st.dataframe(show_df, width="stretch", hide_index=True)

needs_transfer = (order_rows["secondary_qty"] >= order_rows["shortage_qty"]).any()

if needs_transfer:
    st.warning("Secondary warehouse has enough stock to cover at least one missing item. Transfer is available.")
else:
    st.error("No available stock in secondary warehouse to cover the shortfall. This should be escalated as a real exception.")

if st.button("Create Secondary → Main Warehouse transfer", width="stretch"):
    created = []
    for _, row in order_rows.iterrows():
        shortage = int(max(0, row["required_qty"] - row["main_qty"]))
        secondary_qty = int(row["secondary_qty"])
        if shortage <= 0:
            continue
        if secondary_qty < shortage:
            continue

        transfer_id = f"TRF-{datetime.now().strftime('%Y%m%d%H%M%S')}-{row['sku']}"
        existing = query(
            "SELECT 1 FROM transfers WHERE sku = ? AND status IN ('Pending', 'In Transit') LIMIT 1",
            (row["sku"],),
        )
        if not existing:
            execute(
                """
                INSERT INTO transfers (transfer_id, sku, source_warehouse, destination_warehouse, quantity, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    transfer_id,
                    row["sku"],
                    "Secondary Warehouse",
                    "Main Warehouse",
                    shortage,
                    "Pending",
                    datetime.now().isoformat(timespec="minutes"),
                ),
            )
            created.append(row["sku"])

        existing_exception = query(
            "SELECT 1 FROM exceptions WHERE order_id = ? AND sku = ? AND type = 'Inventory mismatch' AND status != 'Resolved' LIMIT 1",
            (selected_order, row["sku"]),
        )
        if not existing_exception:
            execute(
                """
                INSERT INTO exceptions (exception_id, order_id, sku, type, description, priority, status, created_at, assigned_to)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"EXC-{datetime.now().strftime('%Y%m%d%H%M%S')}-{row['sku']}",
                    selected_order,
                    row["sku"],
                    "Inventory mismatch",
                    f"System stock is short for {row['product_name']} ({row['variant']}) and transfer from secondary warehouse was triggered.",
                    "High" if row["priority"] == "High" else "Medium",
                    "Open",
                    datetime.now().isoformat(timespec="minutes"),
                    "Warehouse Team",
                ),
            )

    if created:
        st.success(f"Transfer request(s) created for: {', '.join(created)}")
    else:
        st.info("A transfer was already queued for the stock shortfall, or no transfer was required.")

st.markdown("### Recommended operational action")
if needs_transfer:
    st.write("1. Trigger transfer from Secondary Warehouse to Main Warehouse.\n2. Confirm the stock arrives before the order due time.\n3. Reopen the order for picking once the item is available.")
else:
    st.write("1. Escalate the shortfall as a warehouse exception.\n2. Check if the item can be reallocated from another order or a later replenishment cycle.\n3. Notify the operation lead before the order misses its due time.")
