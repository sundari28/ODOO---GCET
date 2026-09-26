from odoo import api, fields, models


class GcetProductCategory(models.Model):
    _name = "gcet.product.category"
    _description = "Product Category"
    _order = "name"

    name = fields.Char(
        string="Category Name",
        required=True,
    )

    description = fields.Text(
        string="Description",
    )

    active = fields.Boolean(
        default=True,
    )


class GcetProduct(models.Model):
    _name = "gcet.product"
    _description = "Inventory Product"
    _order = "name"

    name = fields.Char(
        string="Product Name",
        required=True,
    )

    sku = fields.Char(
        string="SKU / Code",
        required=True,
        index=True,
    )

    category_id = fields.Many2one(
        "gcet.product.category",
        string="Category",
        ondelete="restrict",
    )

    uom = fields.Char(
        string="Unit of Measure",
        default="Units",
    )

    initial_stock = fields.Float(
        string="Initial Stock",
        default=0.0,
    )

    current_stock = fields.Float(
        string="Current Stock",
        default=0.0,
    )

    minimum_stock = fields.Float(
        string="Minimum Stock",
        default=0.0,
    )

    maximum_stock = fields.Float(
        string="Maximum Stock",
        default=0.0,
    )

    active = fields.Boolean(
        default=True,
    )

    low_stock = fields.Boolean(
        string="Low Stock",
        compute="_compute_low_stock",
        store=True,
    )

    _sql_constraints = [
        (
            "sku_unique",
            "unique(sku)",
            "SKU must be unique.",
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "current_stock" not in vals:
                vals["current_stock"] = vals.get("initial_stock", 0.0)
        return super().create(vals_list)

    def _compute_low_stock(self):
        for product in self:
            product.low_stock = (
                product.current_stock <= product.minimum_stock
            )