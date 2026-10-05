# PRD — Fulfillment Hub

## 1. One-line pitch
Fulfillment Hub helps warehouse and ops teams spot at-risk orders, verify picks, resolve inventory issues, and track handoff to courier pickup so they can ship on time with fewer operational errors.

## 2. The problem
XYZ's fulfillment process is still managed through spreadsheets and fragmented operational communication. Orders can sit in the wrong stage, stock is not always visible where it is needed, and warehouse teams struggle to identify exceptions quickly.

This leads to missed deadlines, wrong-SKU picks, inventory mismatch escalations, delayed dispatch, and slow resolution for urgent orders. The product must make operational risk visible in one place and give teams a clear next action.

## 3. Target user
- Who they are: operations managers, warehouse supervisors, and fulfillment coordinators
- What they use today: spreadsheets, shared tracking files, manual status checks, email/WhatsApp communication, and basic order views
- What frustrates them: incomplete visibility, delayed alerts, manual exception handling, multiple systems that do not align, and difficulty identifying which order needs attention now

## 4. Core features (v1 must-have)
1. Order workboard — shows all orders, priority, status, due dates, and operational risk in a single dashboard.
2. Picking verification workflow — prevents wrong SKU or wrong variant during pick by requiring verification before order is considered ready.
3. Inventory mismatch handling — flags when system stock says an item exists but the warehouse cannot locate it; supports transfer workflow when stock exists in secondary warehouse.
4. Staging and pickup tracking — shows the staging location and courier pickup status for orders that are packed and awaiting dispatch.
5. Exception management — creates, prioritizes, assigns, and resolves operational exceptions without leaving the app.

## 5. OUT OF SCOPE for v1
The following are not in scope for this first release:
- Customer-facing storefront or order placement
- Payment processing, returns, refunds, or invoicing
- Multi-tenant organization setup or enterprise admin console
- Real courier API integrations or live GPS tracking
- Full ERP synchronization or warehouse device scanning
- Chat, comments, or discussion threads on orders
- Role-based login and SSO beyond simple internal access
- Advanced analytics exports or BI dashboards

## 6. User stories
- As an operations manager, I want to see all orders requiring attention in one place, so that I can prioritize urgent work quickly.
- As a warehouse picker, I want to verify the SKU and variant before packing, so that incorrect picks are prevented.
- As a warehouse lead, I want to detect inventory mismatches, so that I can resolve missing stock before dispatch is delayed.
- As a fulfillment coordinator, I want to trigger a transfer from the secondary warehouse to the main warehouse, so that orders can continue without delay.
- As a dispatch manager, I want to track staging bays and pickup windows, so that orders reach the courier on time.
- As a support user, I want to open and resolve exceptions, so that issues are tracked from discovery to closure.

## 7. Success criteria
- A user can identify all high-priority or delayed orders in under 10 seconds.
- A warehouse user can verify a pick and detect a wrong SKU or variant before the order is marked ready.
- A mismatch can be escalated into a transfer + exception workflow without leaving the app.
- Orders in staging show the pickup window and the current status clearly.
- An exception can move from Open to Assigned or Resolved with clear audit visibility.
- The dashboard supports the core operational scenario without needing a full warehouse management system.
