# -*- coding: utf-8 -*-
# Copyright (C) 2019-Today  Technaureus Info Solutions Pvt Ltd.(<http://technaureus.com/>).

from odoo import models, fields, api, _


class ProductCategory(models.Model):
    _inherit = "product.category"

    sale_price_base = fields.Selection([('uom', 'UOM'), ('cwuom', 'CW-UOM')], string="Sale Price Based on")
    purchase_price_base = fields.Selection([('uom', 'UOM'), ('cwuom', 'CW-UOM')], string="Purchase Price Based on")
