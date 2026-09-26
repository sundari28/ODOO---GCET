{
    "name": "GCET Inventory Management System",
    "version": "19.0.1.0.0",
    "category": "Inventory",
    "summary": "Modular Inventory Management System for GCET",
    "description": """
GCET Inventory Management System

Features:
- Product management
- Product categories
- Warehouse management
- Location management
- Stock operations
- Receipts
- Deliveries
- Internal transfers
- Inventory adjustments
- Stock ledger
- Inventory dashboard
- Low stock alerts
""",
    "author": "GCET",
    "license": "LGPL-3",
    "depends": [
        "base"
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/product_views.xml",
        "views/warehouse_views.xml",
        "views/operation_views.xml",
        "views/dashboard_views.xml",
        "views/menu.xml",
    ],
    "installable": True,
    "application": True
}
