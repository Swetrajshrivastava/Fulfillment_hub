# Fulfillment Hub

## Product scope

**Fulfillment Hub V1 — Warehouse Operations MVP**

A focused operational system that helps an e-commerce warehouse monitor orders, identify delays and stock risks, coordinate warehouse transfers, manage staging and courier pickups, and track exceptions.

This is intentionally a small, practical warehouse workflow tool rather than a broad commerce or enterprise platform. The current version is designed to show strong problem understanding, operational judgment, and a usable local user experience for a real fulfillment scenario.

## Problem

XYZ relies on spreadsheets and shared folders to coordinate fulfillment. That makes it difficult to see urgent orders, identify inventory shortages, and follow dispatch problems through to an owner.

## Solution

Fulfillment Hub brings order visibility, stock-risk review, transfer requests, staging details, courier pickup status, and operational exceptions into one local application. Its focus is a clear next action for warehouse and dispatch staff—not a broad commerce platform.

## Key workflows implemented

- **Control tower:** order and priority counts plus an action queue for delayed and at-risk orders, stock transfers, missed pickups, and open exceptions.
- **SLA risk:** classify active orders as On Track, At Risk, Critical, or Delayed. High-priority orders enter At Risk within two hours of the due time; Normal orders enter At Risk within one hour.
- **Orders and timeline:** search and filter by customer/order ID, priority, status, and SLA risk; inspect progress through the fulfillment stages for an order.
- **Inventory:** review order-line shortages across Main and Secondary Warehouse; create a secondary-to-main transfer request when stock is available and record the related exception.
- **Staging and pickup:** review shipment courier, staging location, pickup window, and status; update a shipment to Ready for Pickup, Picked Up, Missed Pickup, or Shipped.
- **Missed pickup:** create an operational exception for seeded missed-pickup shipments.
- **Exception management:** filter exceptions, update status and priority, assign an owning team, and resolve issues.
- **Operations insights:** compare shipment counts, confirmed pickups, missed pickups, and confirmation rates by courier.

The current prototype does **not** include interactive SKU/variant pick verification or live warehouse/courier integrations. Order journey progress is inferred from current statuses; individual transition timestamps are not stored. Average courier delay is not shown because actual pickup timestamps are unavailable.

## Future roadmap

**V1 — Warehouse Operations MVP (implemented now)**

- Order dashboard and prioritization
- Delay and stock-risk visibility
- Secondary-to-main transfer requests
- Staging and courier pickup tracking
- Exception logging for operational issues

**V1.1 — Operational Control Tower (implemented now)**

- SLA risk detection and action queue
- Exception Management Center
- Status-based order journey
- Courier pickup outcome comparison

**V2 — Picking Execution**

- Interactive SKU/variant pick verification
- Barcode/QR workflow

**V3 — Fulfillment Analytics**

- Historical courier performance and trends
- Order and warehouse KPIs
- Operational dashboards
- Trend analysis

**V4 — Predictive Intelligence**

- Demand forecasting
- Delay prediction
- Inventory and replenishment recommendations
- AI operations assistant

**V5 — Production Architecture**

- FastAPI
- PostgreSQL
- Authentication and RBAC
- Deployment and production integrations

These future layers are intentionally documented as roadmap items only. They are not presented as implemented in the current application.

## Tech stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly

## Demo data

The local seed script generates 250 orders, 30 products, and two-warehouse inventory, plus shipment and exception examples. Most due dates remain in the future; seven orders are deliberately overdue, and three orders are placed inside priority-aware SLA risk windows. One lower-volume SKU is set to zero in the Main Warehouse with stock available in the Secondary Warehouse and a transfer queued, producing repeatable stock-risk and transfer-waiting cases. The data also includes a ready-for-pickup shipment and one missed-pickup shipment. Data is synthetic; no live store or courier integrations are used.

Running the seed script resets and recreates the local demo tables.

## How to install (Windows PowerShell)

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## How to run

Initialize or reset the synthetic demo data, then start the app:

```powershell
python database/seed.py
streamlit run app.py --server.port 8501
```

Then open http://localhost:8501. If that port is occupied, choose another available port.

## Demo access

No login or demo credentials are required. The app runs locally against SQLite and uses synthetic warehouse, order, shipment, and exception data.

## Sample workflow

1. Start at the Control Tower and review overdue orders, SLA risk, transfers, missed pickups, and open exceptions.
2. Open Orders, filter by SLA risk, and select an order to inspect its current fulfillment journey.
3. Use Inventory to review a shortage and create a Secondary-to-Main transfer where stock is available.
4. Use Staging to review a pickup window or update a shipment status.
5. Use Exceptions to assign a team, change priority/status, and resolve an issue.
6. Open Operations Insights to compare courier pickup outcomes.

The seed script resets the local demo tables. Only order creation time, due time, and scheduled pickup window are stored; the timeline does not invent event timestamps.

## Project structure

```text
fulfillment-hub/
├── app.py                 # Operations dashboard
├── pages/
│   ├── 1_Orders.py        # Order search, SLA filters, and timeline
│   ├── 2_Inventory.py    # Stock risk and transfer workflow
│   ├── 3_Staging.py      # Staging and courier pickup
│   ├── 4_Exceptions.py   # Exception assignment and resolution
│   └── 5_Insights.py     # Courier outcome comparison
├── database/
│   ├── db.py              # SQLite query/execute helpers
│   ├── schema.sql         # Local data model
│   └── seed.py            # Synthetic demo data
├── services/
│   └── sla.py             # Shared SLA risk rules
├── data/                  # Local SQLite database
├── docs/                  # Product, technical, UX, schema, plan, and walkthrough notes
│   ├── app-flow.md
│   ├── plan.md
│   ├── prd.md
│   ├── schema.md
│   ├── trd.md
│   ├── ui-ux.md
│   └── walkthrough.md
├── AI_USAGE.md            # AI usage disclosure
├── PROJECT_REPORT.md      # Product/technical summary
└── requirements.txt
```

## Walkthrough and AI disclosure

See [docs/walkthrough.md](docs/walkthrough.md) for the timed demo script and [AI_USAGE.md](AI_USAGE.md) for the AI usage note.
