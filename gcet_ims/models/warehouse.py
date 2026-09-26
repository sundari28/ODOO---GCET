from odoo import fields, models


class GcetWarehouse(models.Model):
    _name = "gcet.warehouse"
    _description = "Inventory Warehouse"
    _order = "name"

    name = fields.Char(
        string="Warehouse Name",
        required=True,
    )

    code = fields.Char(
        string="Warehouse Code",
        required=True,
        index=True,
    )

    address = fields.Char(
        string="Address",
    )

    active = fields.Boolean(
        default=True,
    )

    location_ids = fields.One2many(
        "gcet.location",
        "warehouse_id",
        string="Locations",
    )

    _sql_constraints = [
        (
            "warehouse_code_unique",
            "unique(code)",
            "Warehouse code must be unique.",
        ),
    ]


class GcetLocation(models.Model):
    _name = "gcet.location"
    _description = "Inventory Location"
    _order = "name"

    name = fields.Char(
        string="Location Name",
        required=True,
    )

    code = fields.Char(
        string="Location Code",
        required=True,
    )

    warehouse_id = fields.Many2one(
        "gcet.warehouse",
        string="Warehouse",
        required=True,
        ondelete="cascade",
    )

    parent_id = fields.Many2one(
        "gcet.location",
        string="Parent Location",
        ondelete="cascade",
    )

    child_ids = fields.One2many(
        "gcet.location",
        "parent_id",
        string="Child Locations",
    )

    location_type = fields.Selection(
        [
            ("internal", "Internal"),
            ("receiving", "Receiving"),
            ("shipping", "Shipping"),
            ("production", "Production"),
        ],
        string="Location Type",
        default="internal",
        required=True,
    )

    active = fields.Boolean(
        default=True,
    )

    _sql_constraints = [
        (
            "location_code_warehouse_unique",
            "unique(code, warehouse_id)",
            "Location code must be unique within a warehouse.",
        ),
    ]