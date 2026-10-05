# Fulfillment Hub — Product/Technical Notes

## Problem understanding

XYZ relies on spreadsheets and shared folders for fulfillment. The prototype focuses on making order urgency, stock shortages, dispatch state, and operational exceptions visible in one place.

## Product decision

The application is a small local operations dashboard rather than a broad commerce platform. The current scope is intentionally **Fulfillment Hub V1 — Warehouse Operations MVP**. The dashboard centers on the question: what needs attention now?

This is a deliberate product choice. The assignment asks for a practical fulfillment workflow, not a broad enterprise platform. The prototype therefore focuses on a credible warehouse operations workflow that can be explained, demonstrated, and reviewed without overstating the system's scope.

## Implemented

- Control Tower with action counts for delayed and at-risk orders, transfers, missed pickups, and exceptions
- Priority-aware SLA classification, order filtering, and status-based Order Timeline
- Inventory shortage review and secondary-to-main transfer request creation
- Staging location, courier, pickup window, and shipment-status updates
- Exception filtering, assignment, priority/status updates, and resolution
- Courier outcome comparison for confirmed, missed, and ready-for-pickup shipments
- SQLite-backed synthetic demo data

## Not implemented in this prototype

- Interactive SKU/variant pick verification
- Live order, inventory, or courier integrations
- Historical timestamps for each order/shipment status transition
- Average courier delay (actual pickup timestamps are not stored)

These remain roadmap items for future versions rather than claims of functionality already built.

## Future roadmap

**V1 — Warehouse Operations MVP (current)**

- Dashboard and prioritization
- Delay and stock-risk visibility
- Transfer request workflow
- Staging and pickup management
- Exception tracking

**V1.1 — Operational Control Tower (implemented)**

- SLA risk monitoring and action queue
- Exception Management Center
- Status-based order journey
- Courier pickup outcome comparison

**V2 — Picking Execution**

- Interactive SKU/variant pick verification
- Barcode/QR workflow

**V3 — Fulfillment Analytics**

- Historical courier and warehouse trends once timestamped operational data is available
- Order and warehouse KPIs
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

This roadmap makes the project look intentionally scoped and credible. The current application is complete as a V1 fulfillment operations MVP, and V2+ work is kept clearly separate as future development.

## Demo data

The seed script creates a mixture of ordinary and deliberate risk scenarios, including seven overdue orders, three orders inside priority-aware SLA windows, a pending transfer for secondary-only stock, a ready-for-pickup shipment, and one missed-pickup shipment. The generated records are synthetic and do not connect to real store or courier systems.
