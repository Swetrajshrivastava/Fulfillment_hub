# 5-Minute Walkthrough Script

**Recording target:** 4:45–5:00. Show the running app at `http://localhost:8501`. All data is synthetic and local.

## 0:00–0:30 — Problem understanding

**Show:** Fulfillment Hub Control Tower.

**Say:** “XYZ coordinates fulfillment through spreadsheets and shared folders. That makes it hard to see which orders are at risk, whether stock can be transferred in time, and who owns dispatch exceptions. I focused the project on those warehouse decisions, not on replacing the online store or courier systems.”

## 0:30–1:00 — Control Tower

**Show:** Action Required counts and SLA risk queue.

**Say:** “The Control Tower answers one question first: what needs attention now? It combines overdue work, orders nearing their SLA, transfer waits, missed pickups, and open exceptions, with links into the workflow where staff can act.”

## 1:00–1:35 — Orders and SLA Risk

**Show:** Orders page; filter for At Risk or Critical and point out priority and time remaining.

**Say:** “I added an intervention window instead of waiting until every order is already late. High-priority orders become At Risk within two hours of their deadline, Normal orders within one hour, and any order inside 30 minutes is Critical. Those thresholds are explicit and easy to explain.”

## 1:35–2:00 — Order Timeline

**Show:** Select an order and scroll to its timeline.

**Say:** “The timeline makes the current fulfillment journey understandable at a glance. It is inferred from order and shipment status. We do not store a timestamp for every transition, so the view clearly labels missing event times instead of presenting invented history.”

## 2:00–2:40 — Inventory and transfer

**Show:** Inventory page; select a SKU with a main-warehouse shortage and available secondary stock; show quantities and create a transfer if appropriate.

**Say:** “When Main Warehouse stock is short and Secondary Warehouse can cover it, the user can request a transfer. The related exception keeps the shortage visible while the order waits. If no stock is available, the operational response is escalation rather than a misleading transfer.”

## 2:40–3:15 — Staging and courier

**Show:** Staging board; select a Ready for Pickup shipment and point out courier, location, and pickup window.

**Say:** “Dispatch staff can see where each shipment is staged and which pickup window it is planned for, then record a pickup outcome. These are local demo status updates, not live carrier confirmations.”

## 3:15–3:50 — Exception Management

**Show:** Exceptions page; filter by status or priority, edit assigned team, then demonstrate Resolve on a suitable demo exception.

**Say:** “Exceptions bring inventory and courier problems into one queue. Staff can change priority, assign an owning team, move the issue through Open and In Progress, and resolve it. This turns a recorded issue into manageable work.”

## 3:50–4:20 — Courier Performance

**Show:** Operations Insights page; compare confirmed, missed, and ready pickup outcomes by courier.

**Say:** “The courier view compares outcomes using the shipment records we actually have. I did not add an average delay because actual pickup timestamps are not captured; a precise-looking metric without those events would be misleading.”

## 4:20–4:50 — Product choices and close

**Show:** Return to Control Tower.

**Say:** “I kept the build local, SQLite-backed, and focused on the end-to-end warehouse workflow: identify risk, check stock, stage the order, monitor pickup, and resolve exceptions. The data is synthetic. Live integrations and SKU-level pick verification are future work, not claims about this prototype.”

## Recording checklist

- Run from the `fulfillment-hub` project root and confirm the app opens at `http://localhost:8501`.
- Run `python database/seed.py` once before recording if you want fresh relative deadlines and all seeded scenarios; this resets local demo tables.
- Confirm the Control Tower has nonzero SLA-risk, missed-pickup, and exception counts, and that a pending transfer appears.
- Use the seeded Ready for Pickup and Missed Pickup examples. Avoid resolving the missed-pickup exception until after showing its open state.
- Keep the video under five minutes and call out that timeline status is inferred and courier metrics are synthetic outcomes.