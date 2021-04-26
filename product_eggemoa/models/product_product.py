from odoo import models, fields, api, _
from odoo.tools.float_utils import float_round
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    secondary_qty_at_date = fields.Float(
        string="Secondary Qty at Date", compute="_compute_secondary_qty_at_date"
    )

    valuation_display_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Secondary UoM",
        compute="_compute_valuation_display_uom_id",
    )

    @api.depends("uom_id", "secondary_uom_id")
    def _compute_valuation_display_uom_id(self):
        for record in self:
            record.valuation_display_uom_id = (
                record.product_tmpl_id.secondary_uom_id or record.product_tmpl_id.uom_id
            )

    def _compute_secondary_qty_at_date(self):
        for record in self:
            record.secondary_qty_at_date = record.convert_secondary_uom(
                record.qty_at_date,
                record.uom_id,
                record.secondary_uom_id or record.uom_id,
                record.secondary_uom_ratio,
            )

    def convert_secondary_price(
        self, price, input_uom_id, output_uom_id, secondary_uom_ratio
    ):
        return float_round(
            self.convert_secondary_uom(
                price, output_uom_id, input_uom_id, secondary_uom_ratio
            ),
            precision_digits=2,
        )

    def convert_secondary_uom(
        self, qty, input_uom_id, output_uom_id, secondary_uom_ratio
    ):
        if (
            not self.secondary_uom_id
            or input_uom_id.category_id.id == output_uom_id.category_id.id
        ):
            return (
                qty
                if input_uom_id.id == output_uom_id.id
                else input_uom_id._compute_quantity(qty, output_uom_id)
            )

        if input_uom_id.category_id.id == self.uom_id.category_id.id:
            ratio = secondary_uom_ratio
        else:
            if not secondary_uom_ratio:
                raise ValidationError(_("The Secondary UoM Ratio can not be zero."))
            ratio = 1 / secondary_uom_ratio

        ref_output_uom_qty = qty * ratio

        return ref_output_uom_qty
