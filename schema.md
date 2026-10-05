# Backend Schema — Fulfillment Hub

## Part A — Tables and fields

### TABLE: products
- sku TEXT PK
- product_name TEXT NOT NULL
- variant TEXT NOT NULL
- category TEXT NOT NULL

### TABLE: orders
- order_id TEXT PK
- customer_name TEXT NOT NULL
- channel TEXT NOT NULL
- priority TEXT NOT NULL
- status TEXT NOT NULL
- created_at TEXT NOT NULL
- due_at TEXT NOT NULL
- courier TEXT NOT NULL
- total_items INTEGER NOT NULL

### TABLE: order_items
- order_item_id INTEGER PK AUTOINCREMENT
- order_id TEXT NOT NULL FK -> orders.order_id
- sku TEXT NOT NULL FK -> products.sku
- quantity INTEGER NOT NULL

### TABLE: inventory
- sku TEXT NOT NULL FK -> products.sku
- warehouse TEXT NOT NULL
- quantity INTEGER NOT NULL
- reserved_quantity INTEGER NOT NULL DEFAULT 0
- PRIMARY KEY (sku, warehouse)

### TABLE: shipments
- shipment_id TEXT PK
- order_id TEXT NOT NULL FK -> orders.order_id
- courier TEXT NOT NULL
- tracking_number TEXT NOT NULL
- staging_location TEXT NULL
- pickup_window TEXT NOT NULL
- status TEXT NOT NULL

### TABLE: exceptions
- exception_id TEXT PK
- order_id TEXT NULL FK -> orders.order_id
- sku TEXT NULL FK -> products.sku
- type TEXT NOT NULL
- description TEXT NOT NULL
- priority TEXT NOT NULL
- status TEXT NOT NULL
- created_at TEXT NOT NULL
- assigned_to TEXT NULL

### TABLE: transfers
- transfer_id TEXT PK
- sku TEXT NOT NULL FK -> products.sku
- source_warehouse TEXT NOT NULL
- destination_warehouse TEXT NOT NULL
- quantity INTEGER NOT NULL
- status TEXT NOT NULL
- created_at TEXT NOT NULL

## Part B — Relationships
- One order has many order items.
- One product can appear in many order items and many inventory rows.
- One order has zero or many shipments or exception records.
- One order can trigger many transfer records over time.
- A warehouse may several stock rows for many SKUs; each SKU/warehouse pair is unique.
- A user or operator can resolve an exception, but current v1 keeps the workflow simple and local rather than multi-user enterprise setup.

## Part C — Indexes
- idx_orders_priority_due ON orders(priority, due_at)
- idx_orders_status ON orders(status)
- idx_order_items_order ON order_items(order_id)
- idx_inventory_warehouse ON inventory(warehouse)
- idx_shipments_order ON shipments(order_id)
- idx_exceptions_status ON exceptions(status)
- idx_transfers_status ON transfers(status)

## Part D — API contract
| Method | Endpoint | Auth | Returns |
|--------|----------|------|---------|
| GET | /api/v1/orders | Yes | 200 { data[], total, page } |
| GET | /api/v1/orders/:id | Yes | 200 { order, items, shipment, exceptions } |
| POST | /api/v1/picking/verify | Yes | 201 { verified, mismatch, exception_id? } |
| POST | /api/v1/inventory/mismatch | Yes | 201 { exception, transfer? } |
| POST | /api/v1/transfers | Yes | 201 { transfer } |
| PATCH | /api/v1/shipments/:id | Yes | 200 { shipment } |
| GET | /api/v1/exceptions | Yes | 200 { data[] } |
| POST | /api/v1/exceptions | Yes | 201 { exception } |
| PATCH | /api/v1/exceptions/:id | Yes | 200 { exception } |

## Global API rules
- Every error returns: { error: { code, message } }
- Every list endpoint is paginated with default limit 20 and max 100
- Every write validates input before the database is touched
- Never expose raw stock or customer PII beyond the need of the operational workflow
- 401 = not authenticated; 403 = authenticated but not allowed; 404 = resource not found
- A mismatch must not silently succeed; it must create an exception or transfer follow-up

## Operational data rules
- `priority`: High or Normal
- `status`: Processing, Picking, Packing, Staging, Shipped
- `exception.status`: Open, Assigned, Resolved
- `transfer.status`: Pending, In Transit, Completed, Failed
- A pick cannot be considered complete until the SKU and variant match the order requirement

## Schema comments
This schema is intentionally compact and pragmatic. It supports the exact operational risks in scope while staying simple enough for a prototype workflow, a local app, and fast iteration.
