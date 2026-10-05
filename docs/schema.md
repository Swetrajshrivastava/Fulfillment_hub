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
- One order can have many shipments over time.
- One order can create many exceptions.
- One inventory SKU can exist in multiple warehouses.
- Transfer records connect missing stock to a warehouse action.

## Part C — Indexes
- idx_orders_priority_due ON orders(priority, due_at)
- idx_orders_status ON orders(status)
- idx_order_items_order ON order_items(order_id)
- idx_inventory_warehouse ON inventory(warehouse)
- idx_shipments_order ON shipments(order_id)
- idx_exceptions_status ON exceptions(status)
- idx_transfers_status ON transfers(status)

## Part D — API contract (conceptual)
| Method | Endpoint | Auth | Returns |
|--------|----------|------|---------|
| GET | /api/v1/orders | yes | list of orders |
| GET | /api/v1/orders/:id | yes | order + items + shipment context |
| POST | /api/v1/picking/verify | yes | verification result |
| POST | /api/v1/inventory/mismatch | yes | mismatch + exception or transfer |
| POST | /api/v1/transfers | yes | transfer creation |
| PATCH | /api/v1/shipments/:id | yes | staging / pickup update |
| GET | /api/v1/exceptions | yes | current exception queue |
| PATCH | /api/v1/exceptions/:id | yes | resolve / assign |

## Global API rules
- Every error returns: { error: { code, message } }
- Every list endpoint is paginated with default limit 20 and max 100
- Every write validates input before database changes
- Never expose password or sensitive operational data beyond the needs of the internal workflow
- 401 = not authenticated, 403 = authenticated but not allowed, 404 = missing resource

## Operational logic rules
- `priority` is High or Normal.
- `status` should remain within the workflow chain: Processing, Picking, Packing, Staging, Shipped.
- Exceptions must be actionable, not decorative.
- A pick is not complete until the expected SKU and variant match the order.
