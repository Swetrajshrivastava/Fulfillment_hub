
CREATE TABLE IF NOT EXISTS products (
    sku TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    variant TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    channel TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    due_at TEXT NOT NULL,
    courier TEXT NOT NULL,
    total_items INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL,
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(sku) REFERENCES products(sku)
);

CREATE TABLE IF NOT EXISTS inventory (
    sku TEXT NOT NULL,
    warehouse TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    reserved_quantity INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (sku, warehouse),
    FOREIGN KEY(sku) REFERENCES products(sku)
);

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    courier TEXT NOT NULL,
    tracking_number TEXT NOT NULL,
    staging_location TEXT,
    pickup_window TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(order_id)
);

CREATE TABLE IF NOT EXISTS exceptions (
    exception_id TEXT PRIMARY KEY,
    order_id TEXT,
    sku TEXT,
    type TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    assigned_to TEXT,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(sku) REFERENCES products(sku)
);

CREATE TABLE IF NOT EXISTS transfers (
    transfer_id TEXT PRIMARY KEY,
    sku TEXT NOT NULL,
    source_warehouse TEXT NOT NULL,
    destination_warehouse TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(sku) REFERENCES products(sku)
);
