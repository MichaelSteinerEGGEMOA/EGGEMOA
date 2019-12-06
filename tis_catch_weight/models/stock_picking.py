# -*- coding: utf-8 -*-
# Copyright (C) 2019-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def button_validate(self):
        # Set User error warning in two cases:
        #     case 1:If you enter quantity without entering cw quantity.
        #     case 2:If you enter cw quantity without entering quantity.
        #     These will be consider only if the product is catch weight.

        for line in self.move_lines:
            if line.product_id._is_cw_product():
                if line.quantity_done != 0 and line.cw_qty_done == 0:
                    raise UserError(_("Enter the CW Done quantity for the product %r.") % (line.product_id.name))
                elif line.quantity_done == 0 and line.cw_qty_done != 0:
                    raise UserError(_("Enter the Done quantity for the product %r.") % (line.product_id.name))
            else:
                line.cw_qty_done = 0
                return super(Picking, self).button_validate()
        return super(Picking, self).button_validate()
