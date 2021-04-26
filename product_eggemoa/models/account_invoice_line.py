from odoo import models, fields, api
from odoo.addons import decimal_precision


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    secondary_uom_quantity = fields.Float(
        string="Invoice Quantity",
        compute="_compute_secondary_uom_quantity",
        store=True,
        readonly=False,
    )

    secondary_uom_ratio = fields.Float(
        string="Invoice UoM Ratio",
        compute="_compute_secondary_uom_ratio",
        store=True,
        readonly=False,
    )

    secondary_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Invoice UoM",
        help="The secondary UoM informed in the product. Otherwise, the default one.",
        compute="_compute_secondary_uom_id",
        store=True,
        readonly=False,
    )

    secondary_uom_price_unit = fields.Float(
        string="Invoice UoM Price Unit",
        compute="_compute_secondary_uom_price_unit",
        store=True,
        digits=decimal_precision.get_precision("Product Price"),
        readonly=False,
    )

    @api.onchange("quantity", "secondary_uom_ratio")
    def _onchange_quantity_info(self):
        self.secondary_uom_quantity = self.product_id.convert_secondary_uom(
            self.quantity,
            self.uom_id,
            self.secondary_uom_id or self.uom_id,
            self.secondary_uom_ratio,
        )

    @api.depends("price_unit")
    def _compute_secondary_uom_price_unit(self):
        for rec in self:
            rec.secondary_uom_price_unit = rec.product_id.convert_secondary_price(
                rec.price_unit,
                rec.uom_id,
                rec.secondary_uom_id,
                rec.secondary_uom_ratio,
            )

    @api.onchange("secondary_uom_quantity")
    def _onchange_secondary_uom_quantity(self):
        self.secondary_uom_ratio = (
            self.secondary_uom_quantity / self.quantity
            if self.quantity
            else self.secondary_uom_ratio
        )

    @api.onchange("secondary_uom_price_unit", "secondary_uom_ratio")
    def _onchange_secondary_uom_price_unit(self):
        self.price_unit = self.product_id.convert_secondary_price(
            self.secondary_uom_price_unit,
            self.secondary_uom_id,
            self.uom_id,
            self.secondary_uom_ratio,
        )

    @api.depends("product_id", "sale_line_ids")
    def _compute_secondary_uom_ratio(self):
        for rec in self:
            rec.secondary_uom_ratio = (
                rec.sale_line_ids[0].secondary_uom_ratio
                if rec.sale_line_ids
                else (
                    rec.product_id.secondary_uom_ratio
                    if rec.product_id.secondary_uom_id
                    else 1
                )
            )

    @api.depends("product_id", "sale_line_ids")
    def _compute_secondary_uom_id(self):
        for rec in self:
            rec.secondary_uom_id = (
                rec.sale_line_ids[0].secondary_uom_id
                if rec.sale_line_ids
                else (rec.product_id.secondary_uom_id or rec.product_id.uom_id)
            )

    @api.depends("quantity", "uom_id", "secondary_uom_id")
    def _compute_secondary_uom_quantity(self):
        for rec in self:
            rec.secondary_uom_quantity = rec.product_id.convert_secondary_uom(
                rec.quantity,
                rec.uom_id,
                rec.secondary_uom_id or rec.uom_id,
                rec.secondary_uom_ratio,
            )
