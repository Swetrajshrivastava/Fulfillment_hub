
from pathlib import Path
import sqlite3
from datetime import datetime, timedelta
import random

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "fulfillment.db"
SCHEMA = ROOT / "database" / "schema.sql"

random.seed(42)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
conn.executescript(SCHEMA.read_text())

# Reset demo data
for table in ["transfers", "exceptions", "shipments", "order_items", "inventory", "orders", "products"]:
    conn.execute(f"DELETE FROM {table}")

products = []
categories = ["Footwear", "Apparel", "Accessories", "Home"]
names = ["Running Shoes", "Casual Shoes", "T-Shirt", "Hoodie", "Backpack", "Socks", "Water Bottle", "Cap"]
variants = ["Black / S", "Black / M", "Black / L", "Blue / M", "Blue / L", "Red / M"]

for i in range(1, 31):
    sku = f"SKU-{100+i}"
    products.append((sku, random.choice(names), random.choice(variants), random.choice(categories)))
conn.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)

now = datetime.now().replace(second=0, microsecond=0)
customers = ["Aarav Sharma", "Priya Singh", "Rahul Verma", "Ananya Gupta", "Rohan Mehta",
             "Neha Jain", "Vikram Rao", "Kavya Patel", "Aditya Kumar", "Sneha Das"]
channels = ["Amazon", "Flipkart", "Website", "Meesho"]
couriers = ["Delhivery", "Blue Dart", "DTDC", "Ecom Express"]
statuses = ["Processing", "Picking", "Packing", "Staging", "Shipped"]

orders = []
order_items = []
shipments = []
overdue_order_ids = {"ORD-1005", "ORD-1012", "ORD-1021", "ORD-1033", "ORD-1044", "ORD-1055", "ORD-1066"}
at_risk_order_windows = {
    "ORD-1070": ("High", 90),
    "ORD-1071": ("High", 20),
    "ORD-1072": ("Normal", 45),
}
missed_pickup_order_id = "ORD-1078"
ready_for_pickup_order_id = "ORD-1080"

for i in range(1, 251):
    oid = f"ORD-{1000+i}"
    priority = random.choices(["Normal", "High"], weights=[85, 15])[0]
    status = random.choices(statuses, weights=[22, 28, 20, 18, 12])[0]
    if oid in overdue_order_ids:
        created = now - timedelta(hours=random.randint(6, 18), minutes=random.randint(0, 59))
        due = now - timedelta(minutes=random.randint(5, 90))
        status = "Staging" if oid == "ORD-1044" else random.choice(["Processing", "Picking", "Packing"])
        if oid in {"ORD-1005", "ORD-1021", "ORD-1044"}:
            priority = "High"
    else:
        created = now - timedelta(hours=random.randint(0, 4), minutes=random.randint(0, 59))
        due = created + timedelta(hours=(8 if priority == "High" else 12))
        if oid in {missed_pickup_order_id, ready_for_pickup_order_id}:
            status = "Staging"
        if oid in at_risk_order_windows:
            priority, minutes_to_due = at_risk_order_windows[oid]
            due = now + timedelta(minutes=minutes_to_due)
            status = "Picking"

    orders.append((oid, random.choice(customers), random.choice(channels), priority, status,
                   created.isoformat(timespec="minutes"), due.isoformat(timespec="minutes"),
                   random.choice(couriers), 0))

    item_count = random.randint(1, 3)
    chosen = random.sample(products, item_count)
    for sku, *_ in chosen:
        qty = random.randint(1, 2)
        order_items.append((oid, sku, qty))

conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", orders)
conn.executemany("INSERT INTO order_items(order_id, sku, quantity) VALUES (?, ?, ?)", order_items)

# Update total_items
conn.execute("""
UPDATE orders
SET total_items = (
    SELECT COALESCE(SUM(quantity), 0)
    FROM order_items oi
    WHERE oi.order_id = orders.order_id
)
""")

# Inventory: two warehouses, with deliberate mismatches/secondary-only stock
inventory = []
for sku, *_ in products:
    main_qty = random.randint(3, 25)
    secondary_qty = random.randint(0, 35)
    if sku == "SKU-109":
        main_qty = 0
        secondary_qty = random.randint(10, 30)
    inventory.extend([
        (sku, "Main Warehouse", main_qty, random.randint(0, min(3, main_qty))),
        (sku, "Secondary Warehouse", secondary_qty, 0)
    ])
conn.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?)", inventory)
secondary_only_order_id = conn.execute(
    "SELECT oi.order_id FROM order_items oi JOIN orders o ON o.order_id = oi.order_id "
    "WHERE oi.sku = 'SKU-109' AND o.status != 'Shipped' ORDER BY oi.order_id LIMIT 1"
).fetchone()[0]

# Shipments for packed, staged, and shipped orders
stages = ["A-01", "A-02", "A-03", "B-01", "B-02", "C-01"]
for idx, row in enumerate(conn.execute("SELECT order_id, status, courier FROM orders WHERE status IN ('Packing','Staging','Shipped')")):
    oid, status, courier = row
    shipment_status = (
        "Missed Pickup" if oid == missed_pickup_order_id
        else "Ready for Pickup" if status == "Staging"
        else "Picked Up" if status == "Shipped"
        else "Packing"
    )
    staging_location = "B-03" if oid == missed_pickup_order_id else random.choice(stages)
    if oid == missed_pickup_order_id:
        pickup_window = "09:00-10:00"
    else:
        pickup_start = random.choice([20, 40, 60, 90, 120])
        pickup_end = pickup_start + random.choice([60, 80, 100])
        pickup_window = (
            f"{(now + timedelta(minutes=pickup_start)).strftime('%H:%M')}-"
            f"{(now + timedelta(minutes=pickup_end)).strftime('%H:%M')}"
        )
    shipments.append((
        f"SHP-{idx+1:04d}", oid, courier, f"TRK{500000+idx}",
        staging_location,
        pickup_window,
        shipment_status,
    ))
conn.executemany("INSERT INTO shipments VALUES (?, ?, ?, ?, ?, ?, ?)", shipments)

# Operational exceptions
exception_rows = [
    ("EXC-001", "ORD-1005", "SKU-105", "Inventory mismatch", "System shows stock in main warehouse but picker could not locate it.", "Critical", "Open", now.isoformat(timespec="minutes"), "Warehouse Team"),
    ("EXC-002", "ORD-1021", "SKU-112", "Priority delay", "High-priority order is past its same-day processing deadline.", "Critical", "Open", now.isoformat(timespec="minutes"), "Office Team"),
    ("EXC-003", secondary_only_order_id, "SKU-109", "Secondary warehouse stock", "Required stock exists only in the secondary warehouse.", "High", "Open", now.isoformat(timespec="minutes"), "Warehouse Team"),
    ("EXC-004", "ORD-1044", "SKU-127", "Courier pickup risk", "Packed order is ready but pickup window is approaching.", "High", "Assigned", now.isoformat(timespec="minutes"), "Office Team"),
    ("EXC-005", "ORD-1055", "SKU-130", "Missing item", "Picker could not locate one item from the order.", "Medium", "Open", now.isoformat(timespec="minutes"), "Warehouse Team"),
    ("EXC-006", "ORD-1066", "SKU-130", "Variant verification", "Variant requires manual verification before packing.", "Medium", "Resolved", now.isoformat(timespec="minutes"), "Warehouse Team"),
]
conn.executemany("INSERT INTO exceptions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", exception_rows)

transfers = [
    ("TRF-001", "SKU-105", "Secondary Warehouse", "Main Warehouse", 4, "Pending", now.isoformat(timespec="minutes")),
    ("TRF-002", "SKU-112", "Secondary Warehouse", "Main Warehouse", 2, "In Transit", now.isoformat(timespec="minutes")),
    ("TRF-003", "SKU-109", "Secondary Warehouse", "Main Warehouse", 4, "Pending", now.isoformat(timespec="minutes")),
]
conn.executemany("INSERT INTO transfers VALUES (?, ?, ?, ?, ?, ?, ?)", transfers)

conn.commit()
conn.close()
print(f"Seeded database: {DB_PATH}")
