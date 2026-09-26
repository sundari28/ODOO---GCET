from odoo import api, fields, models


class GcetInventoryDashboard(models.Model):
    _name = "gcet.inventory.dashboard"
    _description = "GCET Inventory Dashboard"

    name = fields.Char(
        string="Dashboard",
        default="Inventory Dashboard",
        required=True,
    )

    total_stock = fields.Float(
        string="Total Stock Quantity",
        compute="_compute_kpis",
    )

    low_stock_count = fields.Integer(
        string="Low Stock Items",
        compute="_compute_kpis",
    )

    out_of_stock_count = fields.Integer(
        string="Out of Stock Items",
        compute="_compute_kpis",
    )

    pending_receipts = fields.Integer(
        string="Pending Receipts",
        compute="_compute_kpis",
    )

    pending_deliveries = fields.Integer(
        string="Pending Deliveries",
        compute="_compute_kpis",
    )

    internal_transfers = fields.Integer(
        string="Internal Transfers Scheduled",
        compute="_compute_kpis",
    )

    @api.depends()
    def _compute_kpis(self):
        Product = self.env["gcet.product"]
        Operation = self.env["gcet.stock.operation"]

        products = Product.search([("active", "=", True)])

        total_stock = sum(products.mapped("current_stock"))

        low_stock = products.filtered(
            lambda p: p.current_stock <= p.minimum_stock
            and p.current_stock > 0
        )

        out_of_stock = products.filtered(
            lambda p: p.current_stock <= 0
        )

        for dashboard in self:
            dashboard.total_stock = total_stock
            dashboard.low_stock_count = len(low_stock)
            dashboard.out_of_stock_count = len(out_of_stock)

            dashboard.pending_receipts = Operation.search_count([
                ("operation_type", "=", "receipt"),
                ("state", "in", ["draft", "ready"]),
            ])

            dashboard.pending_deliveries = Operation.search_count([
                ("operation_type", "=", "delivery"),
                ("state", "in", ["draft", "ready"]),
            ])

            dashboard.internal_transfers = Operation.search_count([
                ("operation_type", "=", "internal"),
                ("state", "in", ["draft", "ready"]),
            ])
