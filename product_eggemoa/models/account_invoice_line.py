from odoo import models, fields, api


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    secondary_uom_quantity = fields.Float(
        string="Invoice Quantity",
        compute="_compute_secondary_uom_quantity",
        inverse="_inverse_set_secondary_uom_quantity",
        store=True,
    )

    secondary_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Invoice UoM",
        help="The secondary UoM informed in the product. Otherwise, the default one.",
        compute="_compute_secondary_uom_id",
        store=True,
        readonly=False,
    )

    @api.depends("product_id")
    def _compute_secondary_uom_id(self):
        for rec in self:
            rec.secondary_uom_id = (
                rec.product_id.secondary_uom_id or rec.product_id.uom_id
            )

    @api.depends("quantity", "uom_id", "secondary_uom_id")
    def _compute_secondary_uom_quantity(self):
        for rec in self:
            rec.secondary_uom_quantity = rec.product_id.convert_secondary_uom(
                rec.quantity, rec.uom_id, rec.secondary_uom_id,
            )

    def _inverse_set_secondary_uom_quantity(self):
        for rec in self:
            rec.quantity = rec.product_id.convert_secondary_uom(
                rec.secondary_uom_quantity, rec.secondary_uom_id, rec.uom_id
            )

    @api.onchange("secondary_uom_quantity")
    def _onchange_secondary_uom_quantity(self):
        self.quantity = self.product_id.convert_secondary_uom(
            self.secondary_uom_quantity, self.secondary_uom_id, self.uom_id
        )
