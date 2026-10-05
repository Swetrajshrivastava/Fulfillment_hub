# APP FLOW — Fulfillment Hub

## Screen inventory
| Screen | Purpose | Access | Key actions |
|--------|---------|--------|-------------|
| Dashboard | Overview of fulfillment risk and work queue | Ops user | Review metrics, identify urgent orders |
| Orders list | Browse orders with filters | Ops user | Search, filter by status/priority |
| Order detail | See one order in context | Ops user | Review items, due date, shipment, exceptions |
| Picking verification | Validate SKU/variant before pack | Warehouse worker | Confirm correct item or flag mismatch |
| Inventory mismatch | Review stock in main vs secondary warehouse | Warehouse lead | Trigger transfer or create exception |
| Transfer workflow | Move stock when main warehouse is short | Warehouse lead | Approve transfer and track status |
| Staging and pickup | Review staging location and courier handoff | Dispatch team | Confirm staging and pickup window |
| Exceptions board | Review all open issues | Ops user | Assign and resolve exceptions |

## Flow 1: Daily ops review
Dashboard -> priority queue -> open order -> review due status -> decide to verify, transfer, or dispatch

## Flow 2: Order processing to pick
Orders list -> select order -> Order detail -> mark as ready for picking -> Picking verification -> item matches expected SKU/variant -> continue to pack

## Flow 2b: Wrong-SKU / wrong-variant edge cases
- Item exists but variant differs -> stop workflow and raise exception
- Item missing in main warehouse -> check inventory mismatch
- User tries to continue without verification -> block and require confirmation
- Repeated mismatch on same order -> escalate to supervisor

## Flow 3: Inventory mismatch and transfer
Order detail -> inventory mismatch -> compare system quantity vs actual warehouse stock -> if stock exists in secondary warehouse -> create transfer -> update order status and exception record

## Flow 3b: Transfer edge cases
- secondary warehouse has zero stock -> show unavailable and escalate
- transfer pending beyond SLA -> highlight in exceptions queue
- destination warehouse already has enough stock -> prevent duplicate transfer

## Flow 4: Pack to staging
Pick complete -> order packed -> assign staging bay -> record pickup window -> dispatch can track ready orders

## Flow 4b: Pickup edge cases
- pickup window missed -> create urgent exception
- assigned staging bay wrong -> update and reassign
- courier not present -> keep order visible in at-risk list

## Flow 5: Exceptions lifecycle
Exceptions board -> select issue -> assign owner -> resolve with action taken -> mark resolved and keep traceability

## Global rules
- Every list screen should include an empty state with a call to action.
- Every state-changing workflow should have loading, success, and error states.
- Every screen that loads data must support the 4-state rule: loading, empty, error, populated.
- Processed orders must retain IDs and references across order, transfer, shipment, and exception records.

## 4-state rule
For every screen that loads operational data:
- Loading: page is fetching or recalculating data
- Empty: no relevant orders or records for the current filter
- Error: data failed to load or action did not succeed
- Populated: records are available and actionable

This prevents blank or confusing warehouse screens and gives the team a consistent operational pattern.
