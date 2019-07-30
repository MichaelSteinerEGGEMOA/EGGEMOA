# -*- coding: utf-8 -*-
# Copyright (C) 2019-Today  Technaureus Info Solutions Pvt Ltd.(<http://technaureus.com/>).

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    cw_quantity = fields.Float('CW Quantity', digits=dp.get_precision('Product CW Unit of Measure'))
