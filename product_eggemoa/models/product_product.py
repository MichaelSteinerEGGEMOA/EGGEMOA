from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    secondary_qty_at_date = fields.Float(
        string="Secondary Qty at Date", compute="_compute_secondary_qty_at_date"
    )

    def _compute_secondary_qty_at_date(self):
        for record in self:
            record.secondary_qty_at_date = record.convert_secondary_uom(
                record.qty_at_date, record.uom_id, record.secondary_uom_id
            )

    def convert_secondary_uom(self, qty, input_uom_id, output_uom_id):
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
            ref_input_uom = self.uom_id
            ref_output_uom = self.secondary_uom_id
            ratio = self.secondary_uom_ratio
        else:
            ref_input_uom = self.secondary_uom_id
            ref_output_uom = self.uom_id
            ratio = 1 / self.secondary_uom_ratio

        input_qty = (
            qty
            if input_uom_id.id == ref_input_uom.id
            else input_uom_id._compute_quantity(qty, ref_input_uom)
        )

        ref_output_uom_qty = input_qty * ratio

        return (
            ref_output_uom_qty
            if output_uom_id.id == ref_output_uom.id
            else ref_output_uom._compute_quantity(ref_output_uom_qty, output_uom_id)
        )
