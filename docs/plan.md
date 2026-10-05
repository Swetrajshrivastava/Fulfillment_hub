# IMPLEMENTATION PLAN

## RULES FOR AI
- Build one phase at a time.
- Stop at the end of each phase.
- Do not scaffold future phases.
- Do not touch completed code.
- After each phase, document files changed and how the phase was tested.
- If a requirement is unclear, ask before assuming.

## PHASE 0 — Foundation and local working app
Goal: Confirm the project can run locally with the seeded demo dataset.
Build:
0.1 Validate Python environment and dependencies.
0.2 Confirm database is seeded and accessible.
0.3 Launch the dashboard and confirm the app renders.
Depends on: None
Done when: the app loads and metrics render without runtime errors.
Do NOT build yet: the picking verification or transfer modules.

## PHASE 1 — Ops dashboard and priority queue
Goal: Make it obvious what work needs attention first.
Build:
1.1 Build a worklist of orders with due date and urgency.
1.2 Show priority and delayed orders in a clear queue.
1.3 Add filtering by priority/status/search.
Depends on: Phase 0
Done when: a user can quickly identify the urgent orders in one view.
Do NOT build yet: advanced exception workflows.

## PHASE 2 — Picking verification workflow
Goal: Prevent wrong-SKU and wrong-variant picks.
Build:
2.1 Add a picking verification view for selected orders.
2.2 Compare ordered SKUs/variants to expected pick data.
2.3 Block the workflow if a mismatch is detected and create a record of the exception.
Depends on: Phase 1
Done when: the app recognizes a bad SKU or variant before the order is marked complete.
Do NOT build yet: staging or courier handoff modules.

## PHASE 3 — Inventory mismatch and secondary transfer
Goal: Give the user a practical path when stock is missing or mismatched.
Build:
3.1 Add an inventory mismatch view for stock discrepancies.
3.2 Check if the required stock exists in the secondary warehouse.
3.3 Create a transfer record and document the exception path.
Depends on: Phase 2
Done when: a missing item can be routed into a transfer workflow instead of silently failing.
Do NOT build yet: courier pickup tracking.

## PHASE 4 — Staging and courier pickup visibility
Goal: Make dispatch status clear and controllable.
Build:
4.1 Show staging location and pickup window for packed orders.
4.2 Add a pickup status view and alert when the window is at risk.
4.3 Keep shipments visible in the active workflow.
Depends on: Phase 3
Done when: a dispatch user can tell which orders are ready, delayed, or at risk.
Do NOT build yet: broad reporting or ERP integration.

## PHASE 5 — Exception board and resolution
Goal: Convert operational issues into a manageable work queue.
Build:
5.1 Add an exception list with open and resolved states.
5.2 Let the user assign owners and close issues.
5.3 Track the issue lifecycle from create to resolution.
Depends on: Phase 4
Done when: a warehouse issue is visible, actionable, and traceable.
Do NOT build yet: consumer features or unrelated platform expansion.

## PHASE 6 — Demo polish and communication readiness
Goal: Make the product ready for the 5-minute walkthrough and final submission.
Build:
6.1 Improve empty, loading, and error states.
6.2 Tighten the UI flow so the demo is obvious and easy to follow.
6.3 Prepare final project narrative and AI usage note.
Depends on: Phase 5
Done when: the app can explain the core workflow to a reviewer in a short walkthrough.
