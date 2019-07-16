# -*- coding: utf-8 -*-
# Copyright (C) 2019-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round


class ReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    cw_quantity = fields.Float("CW Quantity", digits=dp.get_precision('Product CW Unit of Measure'), required=True)
    cw_uom_id = fields.Many2one('uom.uom', string='CW-UOM', related='move_id.product_cw_uom')
    catch_weight_ok = fields.Boolean(invisible='1', related='product_id.catch_weight_ok')


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    @api.model
    def default_get(self, fields):
        res = super(ReturnPicking, self).default_get(fields)
        picking = self.env['stock.picking'].browse(self.env.context.get('active_id'))
        if picking:
            for move in picking.move_lines:
                if move.scrapped:
                    continue
                cw_quantity = move.cw_product_qty - sum(move.move_dest_ids.filtered(lambda m: m.state in ['partially_available', 'assigned', 'done']). \
                    mapped('move_line_ids').mapped('cw_product_qty'))
        if 'product_return_moves' in res.keys():
            product_return_moves = res.get('product_return_moves')
            order = product_return_moves[0][2]
            order.update({'cw_quantity': cw_quantity,
                          'cw_uom_id': move.product_id.cw_uom_id.id
                          })
        return res

    def _prepare_move_default_values(self, return_line, new_picking):
        res=  super(ReturnPicking, self)._prepare_move_default_values(return_line, new_picking )
        res.update({
            'product_cw_uom_qty': return_line.cw_quantity,
            'product_cw_uom': return_line.product_id.cw_uom_id.id,
            })
        return res