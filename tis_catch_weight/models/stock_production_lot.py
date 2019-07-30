# -*- coding: utf-8 -*-
# Copyright (C) 2019-Today  Technaureus Info Solutions Pvt Ltd.(<http://technaureus.com/>).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    product_cw_uom = fields.Many2one('product.uom', 'Unit of Measure', related='product_id.cw_uom_id', store=True)
    cw_product_qty = fields.Float('Quantity', compute='_cw_product_qty', digits=dp.get_precision('Product CW Unit of Measure'))

    @api.one
    def _cw_product_qty(self):
        quants = self.quant_ids.filtered(lambda q: q.location_id.usage in ['internal', 'transit'])
        self.cw_product_qty = sum(quants.mapped('cw_stock_quantity'))
