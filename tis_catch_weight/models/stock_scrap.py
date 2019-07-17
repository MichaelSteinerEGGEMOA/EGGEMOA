# -*- coding: utf-8 -*-
# Copyright (C) 2019-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

from odoo import api, fields, models, _


class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    catch_weight_ok = fields.Boolean(invisible='1', related='product_id.catch_weight_ok')
    product_cw_uom = fields.Many2one('uom.uom', string='CW-UOM', states={'done': [('readonly', True)]})
    scrap_cw_qty = fields.Float(string='CW Quantity', states={'done': [('readonly', True)]})

    def _prepare_move_values(self):
        res = super(StockScrap, self)._prepare_move_values()
        res.update({
            'product_cw_uom': self.product_cw_uom.id,
            'product_cw_uom_qty': self.scrap_cw_qty,

        })
        for values in res['move_line_ids']:
            values[2].update({
                'product_cw_uom': self.product_cw_uom.id,
                'cw_qty_done': self.scrap_cw_qty,
            })
        return res

    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super(StockScrap, self).onchange_product_id()
        self.product_cw_uom = self.product_id.cw_uom_id.id
        return res
