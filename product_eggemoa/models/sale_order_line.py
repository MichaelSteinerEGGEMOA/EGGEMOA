from odoo import models, fields, api
from odoo.addons import decimal_precision


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    secondary_uom_price_unit = fields.Float(
        string="Invoice UoM Price Unit",
        digits=decimal_precision.get_precision("Product Price"),
    )

    secondary_uom_id = fields.Many2one(comodel_name="uom.uom", string="Invoice Uom")

    secondary_uom_ratio = fields.Float(string="Invoice UoM Ratio",)

    secondary_uom_qty = fields.Float(string="Invoice UoM Total Quantity",)

    @api.onchange("product_uom_qty", "secondary_uom_ratio")
    def _onchange_quantity_info(self):
        self.secondary_uom_qty = self.product_id.convert_secondary_uom(
            self.product_uom_qty,
            self.product_uom,
            self.secondary_uom_id or self.product_uom,
            self.secondary_uom_ratio,
        )

    @api.onchange("secondary_uom_qty")
    def _onchange_secondary_uom_qty(self):
        self.secondary_uom_ratio = (
            self.secondary_uom_qty / self.product_uom_qty
            if self.product_uom_qty
            else self.secondary_uom_ratio
        )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.secondary_uom_id = (
            self.product_id.secondary_uom_id or self.product_id.uom_id
        )
        self.secondary_uom_ratio = (
            self.product_id.secondary_uom_ratio
            if self.product_id.secondary_uom_id
            else 1
        )

    @api.onchange("price_unit")
    def _onchange_price_unit(self):
        self.secondary_uom_price_unit = self.product_id.convert_secondary_price(
            self.price_unit,
            self.product_uom,
            self.secondary_uom_id or self.product_uom,
            self.secondary_uom_ratio,
        )

    @api.onchange("secondary_uom_price_unit", "secondary_uom_ratio")
    def _onchange_secondary_uom_price_unit(self):
        self.price_unit = self.product_id.convert_secondary_price(
            self.secondary_uom_price_unit,
            self.secondary_uom_id or self.product_uom,
            self.product_uom,
            self.secondary_uom_ratio,
        )
