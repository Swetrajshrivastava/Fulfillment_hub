# APP FLOW — Fulfillment Hub

> **Scope note:** This document describes the intended operational flow. The current prototype implements the Control Tower and SLA risk queue, searchable orders with a status-based journey, inventory transfers, shipment status updates, actionable exception management, and courier pickup outcome comparison. Interactive SKU/variant picking verification, live integrations, and historical event timestamps are not implemented; see [README.md](README.md) and [docs/walkthrough.md](docs/walkthrough.md) for the verified demo scope.

## Screen inventory
| Screen | Purpose | Access | Key actions |
|--------|---------|--------|-------------|
| Dashboard | Overview of operations and at-risk orders | Internal ops user | Filter, review urgency, open order details |
| Orders list | Search and review all orders by status or priority | Internal ops user | Search, filter, open order |
| Order detail | Operational review for one order | Internal ops user | Check lines, status, pickup, exceptions |
| Picking verification | Validate SKU/variant before packing | Warehouse user | Confirm correct item, flag mismatch |
| Inventory mismatch | Review missing or miscounted stock | Warehouse lead | Mark item missing, create transfer request |
| Transfer workflow | Move stock from secondary to main warehouse | Warehouse lead | Trigger transfer and review status |
| Staging / courier | Track staging bay and pickup schedule | Dispatch team | Update staging location, confirm pickup |
| Exceptions board | Review problems and resolutions | Ops team | Open, assign, resolve, escalate |

## Flow 1: Daily operations dashboard
Dashboard -> review metric cards -> identify attention queue -> click an order -> Order detail -> decide: verify pick, resolve exception, or update staging status

## Flow 1b: High-priority risk handling
Dashboard -> high-priority/delayed order flagged -> open order detail -> identify missing item -> Inventory mismatch screen -> check secondary warehouse -> create transfer request -> return to order detail -> update status

## Flow 2: Picking verification
Orders list -> select order awaiting pick -> Picking verification -> compare ordered SKU and variant -> if correct -> mark verified -> if wrong -> block pack and create exception

## Flow 2b: Wrong-SKU edge cases
- Ordered item not found in system -> show item missing / mismatch
- Ordered SKU exists but variant differs -> require manual override with reason
- User confirms verification but mismatch exists -> mark exception as Critical and route to supervisor
- Repeated wrong pick attempts -> freeze order and require recheck

## Flow 3: Inventory mismatch and transfer
Order detail -> inventory mismatch -> system stock vs actual warehouse count -> if secondary warehouse has stock -> create transfer -> update status to Pending / In Transit -> re-check allocation for order

## Flow 3b: Transfer edge cases
- Secondary warehouse quantity is 0 -> show no transfer possible and raise exception
- Destination main warehouse already has sufficient stock -> flag duplicate transfer request
- Transfer takes longer than expected -> escalate as operational exception / SLA breach

## Flow 4: Staging and courier pickup
Packing complete -> staging location assigned -> order is marked Ready for Pickup -> courier window visible -> dispatch team confirms pickup -> shipment status updates to Picked Up

## Flow 4b: Pickup edge cases
- Pickup window missed -> create urgent exception
- Wrong staging bay assigned -> update location and notify dispatch
- Courier not arrived -> keep order visible in at-risk queue

## Flow 5: Exception lifecycle
Exceptions board -> select open exception -> assign to owner -> resolve with action taken -> mark Resolved -> record closure details

## Global rules
- Any protected operational screen without a valid session or user state should redirect to the dashboard or a safe landing state
- Every list screen should include an empty state with a clear CTA
- Every async or state-changing action must have a loading, success, and error state
- Every order screen must account for: loading, empty, error, and populated states
- Every workflow must preserve the order id and exception id references for traceability

## 4-state rule
For every screen that loads operational data, define the states clearly:
- Loading: data is fetching or re-evaluating
- Empty: no relevant records for this filter or context
- Error: data cannot be loaded or action failed
- Populated: records available and actionable

This rule prevents blank UI states and ensures the dashboard always communicates operational status.
