# IMPLEMENTATION PLAN

## RULES FOR AI
- Build ONE phase at a time.
- Stop at the end of each phase.
- Do not scaffold future phases.
- Do not touch completed code.
- After each phase, list files created/changed and how to test.
- If a requirement is ambiguous, ask before assuming.

## PHASE 0 — Foundation and repo readiness
Goal: Ensure the project runs locally and the database is in a usable state.
Build:
1.0 Confirm project structure and local dependencies.
1.1 Validate Python environment and required packages.
1.2 Confirm the SQLite database is seeded and accessible.
1.3 Run the app and confirm the dashboard loads successfully.
Depends on: None
Done when: `streamlit run app.py` opens the dashboard and metrics render without errors.
Do NOT build yet: Picking logic, transfer workflow, or exception UI beyond the baseline dashboard.

## PHASE 1 — Core order visibility and filters
Goal: Deliver a clear operational view for order review.
Build:
1.1 Expand the order list with better filters and search.
1.2 Improve order detail and urgency logic.
1.3 Confirm that delayed and high-priority orders are easy to identify.
Depends on: Phase 0
Done when: A user can browse and filter orders by status, priority, and keyword.
Do NOT build yet: Inventory mismatch or transfer forms.

## PHASE 2 — Picking verification workflow
Goal: Prevent wrong-SKU and wrong-variant picks.
Build:
2.1 Add a picking verification screen for selected orders.
2.2 Compare the order item list to expected SKU/variant data.
2.3 Block a pick if mismatched and create an exception record.
Depends on: Phase 1
Done when: A mismatched pick can be detected before completion and is recorded as a workflow issue.
Do NOT build yet: Courier pickup status or full shipment tracking.

## PHASE 3 — Inventory mismatch and transfer workflow
Goal: Resolve missing stock with a clear operational path.
Build:
3.1 Add inventory mismatch review for orders with missing or conflicting stock.
3.2 Check whether the item exists in the secondary warehouse.
3.3 Create a transfer record and update the order or exception state.
Depends on: Phase 2
Done when: A missing item can be diagnosed and routed through a transfer workflow.
Do NOT build yet: Staging bay UI or dispatch monitoring.

## PHASE 4 — Staging and courier pickup tracking
Goal: Track warehouse-to-courier handoff.
Build:
4.1 Add staging location and pickup window visibility.
4.2 Create a dispatch queue and pickup status updates.
4.3 Surface at-risk orders whose handoff is delayed.
Depends on: Phase 3
Done when: An order can be tracked from packing to pickup window and status updates are visible.
Do NOT build yet: Advanced reporting or ERP integrations.

## PHASE 5 — Exception creation and resolution
Goal: Turn issues into a managed operational workflow.
Build:
5.1 Create exception records from mismatch, delay, and pickup issues.
5.2 Assign responsibility and mark resolution status.
5.3 Add a simple exception board with filters and closure flow.
Depends on: Phase 4
Done when: An issue can be created, assigned, and closed with a traceable record.
Do NOT build yet: Customer-facing features or external integrations.

## PHASE 6 — Polish and deployment readiness
Goal: Make the prototype feel coherent and ready for a demo.
Build:
6.1 Apply the UI/UX design system consistently.
6.2 Tighten empty, loading, and error states.
6.3 Check responsiveness and final demo flow.
Depends on: Phase 5
Done when: The app can be demonstrated from dashboard to issue resolution without confusion.
Do NOT build yet: Large-scale expansion or unrelated features.
