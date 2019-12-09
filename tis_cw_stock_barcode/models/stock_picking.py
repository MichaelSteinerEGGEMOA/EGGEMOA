# -*- coding: utf-8 -*-
# Copyright (C) 2019-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'barcodes.barcode_events_mixin']

    def get_barcode_view_state(self):
        pickings = super(StockPicking, self).get_barcode_view_state()
        move_lines = self.read([
            'move_line_ids',
        ])
        for picking in pickings:
            for move_line in move_lines:
                picking['move_line_ids'] = self.env['stock.move.line'].browse(move_line.pop('move_line_ids')).read([
                    'product_id',
                    'location_id',
                    'location_dest_id',
                    'qty_done',
                    'display_name',
                    'product_uom_qty',
                    'product_uom_id',
                    'product_barcode',
                    'owner_id',
                    'catch_weight_ok',
                    'lot_id',
                    'lot_name',
                    'package_id',
                    'result_package_id',
                    'dummy_id',
                    'cw_qty_done',
                    'product_cw_uom_qty',
                    'product_cw_uom',
                ])
                for move_line_id in picking['move_line_ids']:
                    move_line_id['product_id'] = \
                        self.env['product.product'].browse(move_line_id.pop('product_id')[0]).read([
                            'id',
                            'tracking',
                            'barcode',
                        ])[0]
                    move_line_id['location_id'] = \
                        self.env['stock.location'].browse(move_line_id.pop('location_id')[0]).read([
                            'id',
                            'display_name',
                        ])[0]
                    move_line_id['location_dest_id'] = \
                        self.env['stock.location'].browse(move_line_id.pop('location_dest_id')[0]).read([
                            'id',
                            'display_name',
                        ])[0]
        return pickings
