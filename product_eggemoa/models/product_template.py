from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    secondary_uom_ratio = fields.Float(
        string="Secondary UoM ratio",
        help="Ratio between secondary unit and primary one.",
        default=1,
    )

    secondary_uom_id = fields.Many2one(
        string="Secondary UoM",
        comodel_name="uom.uom",
        help="Secondary unit that will be used for invoicing",
    )

    @api.constrains("secondary_uom_ratio", "secondary_uom_id")
    def _check_secondary_uom_ratio(self):
        for rec in self:
            if (
                rec.secondary_uom_id
                and float_compare(
                    rec.secondary_uom_ratio,
                    0,
                    precision_rounding=rec.secondary_uom_id.rounding,
                )
                != 1
            ):
                raise ValidationError(
                    _("Secondary UoM ratio has to be greater than zero.")
                )
