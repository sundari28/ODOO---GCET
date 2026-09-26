from odoo import api, fields, models


class GcetStockOperation(models.Model):
    _name = "gcet.stock.operation"
    _description = "Stock Operation"
    _order = "id desc"

    name = fields.Char(
        string="Reference",
        required=True,
        default="New",
    )

    operation_type = fields.Selection(
        [
            ("receipt", "Receipt"),
            ("delivery", "Delivery"),
            ("internal", "Internal Transfer"),
            ("adjustment", "Inventory Adjustment"),
        ],
        string="Operation Type",
        required=True,
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("ready", "Ready"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        default="draft",
        required=True,
    )

    date = fields.Datetime(
        string="Date",
        default=fields.Datetime.now,
        required=True,
    )

    source_location_id = fields.Many2one(
        "gcet.location",
        string="Source Location",
    )

    destination_location_id = fields.Many2one(
        "gcet.location",
        string="Destination Location",
    )

    notes = fields.Text(
        string="Notes",
    )

    line_ids = fields.One2many(
        "gcet.stock.operation.line",
        "operation_id",
        string="Products",
    )

    def action_ready(self):
        self.write({"state": "ready"})

    def action_cancel(self):
        self.write({"state": "canceled"})

    def action_done(self):
        for operation in self:
            if operation.state not in ("draft", "ready"):
                continue

            for line in operation.line_ids:
                product = line.product_id
                qty = line.quantity

                if operation.operation_type == "receipt":
                    product.current_stock += qty

                elif operation.operation_type == "delivery":
                    product.current_stock -= qty

                elif operation.operation_type == "adjustment":
                    product.current_stock = line.quantity

                self.env["gcet.stock.ledger"].create({
                    "operation_id": operation.id,
                    "product_id": product.id,
                    "quantity": qty,
                    "operation_type": operation.operation_type,
                    "source_location_id": operation.source_location_id.id,
                    "destination_location_id": operation.destination_location_id.id,
                })

            operation.state = "done"


class GcetStockOperationLine(models.Model):
    _name = "gcet.stock.operation.line"
    _description = "Stock Operation Line"

    operation_id = fields.Many2one(
        "gcet.stock.operation",
        required=True,
        ondelete="cascade",
    )

    product_id = fields.Many2one(
        "gcet.product",
        string="Product",
        required=True,
    )

    quantity = fields.Float(
        string="Quantity",
        required=True,
    )

    uom = fields.Char(
        related="product_id.uom",
        string="UoM",
        readonly=True,
    )


class GcetStockLedger(models.Model):
    _name = "gcet.stock.ledger"
    _description = "Stock Ledger"
    _order = "id desc"

    operation_id = fields.Many2one(
        "gcet.stock.operation",
        string="Operation",
        ondelete="cascade",
    )

    product_id = fields.Many2one(
        "gcet.product",
        string="Product",
        required=True,
    )

    quantity = fields.Float(
        string="Quantity",
    )

    operation_type = fields.Selection(
        [
            ("receipt", "Receipt"),
            ("delivery", "Delivery"),
            ("internal", "Internal Transfer"),
            ("adjustment", "Inventory Adjustment"),
        ],
        string="Operation Type",
    )

    source_location_id = fields.Many2one(
        "gcet.location",
        string="Source Location",
    )

    destination_location_id = fields.Many2one(
        "gcet.location",
        string="Destination Location",
    )

    date = fields.Datetime(
        default=fields.Datetime.now,
        required=True,
    )
