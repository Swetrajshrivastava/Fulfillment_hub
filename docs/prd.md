# PRD — Fulfillment Hub

## Assignment requirement
This project is a fulfillment operations dashboard for a small warehouse team handling around 200–300 orders per day. The product must help the team prioritize work, reduce picking errors, identify stock issues, manage courier handoff, and track operational exceptions.

## Proposed implementation decision
We will build a lightweight internal operations dashboard in Python using Streamlit and SQLite. This keeps the product practical for a small team, fast to iterate, and easy to run locally while still solving the business workflow clearly.

## 1. One-line pitch
Fulfillment Hub helps warehouse and operations teams manage the order lifecycle from intake to ship so that priority orders are completed on time, picking is verified, stock issues are visible, and handoff delays are caught early.

## 2. The problem
The fulfillment team is operating on a mix of manual checks, spreadsheets, and fragmented visibility. Orders move through processing, picking, packing, staging, and shipping without a single operational view.

This creates several operational risks:
- high-priority orders are missed or delayed
- incorrect SKU or variant selection during picking
- inventory mismatch between system stock and actual warehouse stock
- delayed transfer from secondary to main warehouse
- staging and pickup delays with courier handoff
- missing visibility into exceptions that require action

## 3. Target user
- Who they are: warehouse supervisors, ops coordinators, and warehouse staff
- What they use today: shared spreadsheets, manual handoff notes, Excel-based tracking, and verbal updates
- What frustrates them: unclear priorities, slow exception handling, physical stock not matching system stock, and lack of a single place to see what needs attention now

## 4. Core features (v1 must-have)
1. Order visibility board — shows all orders, urgency, due times, and order status.
2. Priority queue — surfaces same-day or delayed orders that need action.
3. Picking verification — checks SKU/variant before the pick is treated as complete.
4. Inventory mismatch workflow — shows stock discrepancies and supports transfer decisions.
5. Staging and courier pickup tracking — shows staging bay and pickup timing.
6. Exception board — lets the team open, assign, and resolve operational issues.

## 5. Out of scope for v1
- Customer checkout or storefront
- Payment processing, returns, refunds, or invoicing
- Real courier API integration or live telematics
- ERP-level inventory sync or full warehouse management system
- Multi-location admin portal or enterprise role management
- Chat threads or employee communication features

## 6. User stories
- As an operations manager, I want a priority queue, so I can see what must be actioned first.
- As a warehouse picker, I want to verify the SKU and variant, so I do not pick the wrong item.
- As a warehouse lead, I want to see inventory mismatches, so I can resolve stock gaps before dispatch.
- As a fulfillment coordinator, I want a transfer workflow, so stock can move from secondary to main warehouse when needed.
- As a dispatch team member, I want staging and pickup visibility, so I can ensure orders leave on time.
- As an ops user, I want an exception list, so I can track issues from open to resolved.

## 7. Success criteria
- A user can identify high-priority or delayed orders in under 10 seconds.
- A wrong-SKU or wrong-variant pick is detected before the order is marked ready.
- A stock issue can be escalated into a transfer and exception workflow without leaving the app.
- A packed order shows its staging location and pickup status clearly.
- An exception can move from open to assigned or resolved with a clear record.
- The dashboard supports the full order lifecycle from processing to shipping in a practical, low-complexity way.
