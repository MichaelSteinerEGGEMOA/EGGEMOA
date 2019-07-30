# -*- coding: utf-8 -*-
# Copyright (C) 2019-Today  Technaureus Info Solutions Pvt Ltd.(<http://technaureus.com/>).

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_round
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare
from . import catch_weight


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def button_confirm(self):
        for line in self.order_line:
            if line.product_id._is_cw_product():
                if line.product_cw_uom_qty == 0 and line.product_qty != 0:
                    raise UserError(_("Please enter the CW Quantity for %s") % (line.product_id.name))
                elif line.product_cw_uom_qty != 0 and line.product_qty == 0:
                    raise UserError(_("Please enter the Quantity for %s") % (line.product_id.name))
            else:
                line.product_cw_uom_qty = 0
        return super(PurchaseOrder, self).button_confirm()


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_cw_uom_qty', 'product_cw_uom')
    def _onchange_cw_quantity(self):
        if not self.product_id:
            return
        if not self.product_id._is_price_based_on_cw('purchase'):
            return
        params = {'order_id': self.order_id}
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order[:10],
            uom_id=self.product_uom,
        )

        if seller or not self.date_planned:
            self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        if not seller:
            if self.product_id.seller_ids.filtered(lambda s: s.name.id == self.partner_id.id):
                self.price_unit = 0.0
            return

        price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price,
                                                                             self.product_id.supplier_taxes_id,
                                                                             self.taxes_id,
                                                                             self.company_id) if seller else 0.0
        if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
            price_unit = seller.currency_id._convert(
                price_unit, self.order_id.currency_id, self.order_id.company_id, self.date_order or fields.Date.today())
        if seller and self.product_cw_uom and self.product_id.cw_uom_id != self.product_cw_uom:
            price_unit = self.product_id.cw_uom_id._compute_price(price_unit, self.product_cw_uom)
        self.price_unit = price_unit

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'product_cw_uom_qty')
    def _compute_amount(self):
        if not self.env.user.has_group('tis_catch_weight.group_catch_weight'):
            return super(PurchaseOrderLine, self)._compute_amount()
        # phase one optimised
        for line in self:
            if line.product_id._is_price_based_on_cw('purchase'):
                quantity = line.product_cw_uom_qty
            else:
                quantity = line.product_qty
            taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, quantity,
                                              product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    @api.depends('order_id.state', 'move_ids.state', 'move_ids.cw_qty_done')
    def _compute_cw_qty_received(self):
        for line in self:
            if line.product_id._is_cw_product():
                if line.order_id.state not in ['purchase', 'done']:
                    line.cw_qty_received = 0.0
                    continue
                if line.product_id.type not in ['consu', 'product']:
                    line.cw_qty_received = line.product_cw_uom_qty
                    continue
                total = 0.0
                for move in line.move_ids:
                    if move.state == 'done':
                        if move.location_dest_id.usage == "supplier":
                            if move.to_refund:
                                total -= move.product_cw_uom._compute_quantity(move.cw_qty_done, line.product_cw_uom)
                        else:
                            total += move.product_cw_uom._compute_quantity(move.cw_qty_done, line.product_cw_uom)
                line.cw_qty_received = total
            else:
                line.cw_qty_received = 0.0

    @api.depends('invoice_lines.invoice_id.state', 'invoice_lines.product_cw_uom_qty')
    def _compute_cw_qty_invoiced(self):
        for line in self:
            qty = 0.0
            for inv_line in line.invoice_lines:
                if inv_line.invoice_id.state not in ['cancel']:
                    if inv_line.invoice_id.type == 'in_invoice':
                        qty += inv_line.product_cw_uom._compute_quantity(inv_line.product_cw_uom_qty,
                                                                         line.product_cw_uom)
                    elif inv_line.invoice_id.type == 'in_refund':
                        qty -= inv_line.product_cw_uom._compute_quantity(inv_line.product_cw_uom_qty,
                                                                         line.product_cw_uom)
            line.cw_qty_invoiced = qty

    product_cw_uom = fields.Many2one('product.uom', string='CW-UOM')
    catch_weight_ok = fields.Boolean(invisible='1', related='product_id.catch_weight_ok')
    product_cw_uom_qty = fields.Float(string='CW-Qty', default=0.0,
                                      digits=dp.get_precision('Product CW Unit of Measure'))
    cw_qty_invoiced = fields.Float(compute='_compute_cw_qty_invoiced',
                                   digits=dp.get_precision('Product CW Unit of Measure'))
    cw_qty_received = fields.Float(compute='_compute_cw_qty_received',
                                   digits=dp.get_precision('Product CW Unit of Measure'))

    @api.multi
    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super(PurchaseOrderLine, self).onchange_product_id()
        if self.product_id._is_cw_product():
            self.product_cw_uom = self.product_id.cw_uom_id
            domain_dict = res.get('domain')
            domain_dict.update({'product_cw_uom': [('category_id', '=', self.product_id.cw_uom_id.category_id.id)]})
        else:
            self.product_cw_uom = None
        return res

    def _update_received_cw_qty(self):
        for line in self:
            if line.product_id._is_cw_product():
                total = 0.0
                for move in line.move_ids:
                    if move.state == 'done':
                        if move.location_dest_id.usage == "supplier":
                            if move.to_refund:
                                total -= move.product_cw_uom._compute_quantity(move.cw_qty_done, line.product_cw_uom)
                        else:
                            total += move.product_cw_uom._compute_quantity(move.cw_qty_done, line.product_cw_uom)
                line.cw_qty_received = total

    @api.multi
    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        cw_qty = 0.0
        for move in self.move_ids.filtered(
                lambda x: x.state != 'cancel' and not x.location_dest_id.usage == "supplier"):
            cw_qty += move.product_cw_uom._compute_quantity(move.product_cw_uom_qty, self.product_cw_uom,
                                                            rounding_method='HALF-UP')

        diff_cw_quantity = self.product_cw_uom_qty - cw_qty
        if float_compare(diff_cw_quantity, 0.0, precision_rounding=self.product_cw_uom.rounding) > 0:
            if self.product_id._is_cw_product():
                cw_quant_uom = self.product_id.cw_uom_id
                get_param = self.env['ir.config_parameter'].sudo().get_param
                if self.product_cw_uom.id != cw_quant_uom.id and get_param('stock.propagate_uom') != '1':
                    cw_product_qty = self.product_cw_uom._compute_quantity(diff_cw_quantity, cw_quant_uom,
                                                                           rounding_method='HALF-UP')
                    if res:
                        res[0]['product_cw_uom'] = cw_quant_uom.id
                        res[0]['product_cw_uom_qty'] = cw_product_qty
                elif self.product_cw_uom.id == cw_quant_uom.id and res:
                    res[0]['product_cw_uom'] = self.product_cw_uom.id
                    res[0]['product_cw_uom_qty'] = diff_cw_quantity
                else:
                    raise UserError(
                        _('You cannot update CW quantity without updating quantity for validated receipts.'))
        return res

    @api.multi
    def write(self, values):
        result = super(PurchaseOrderLine, self).write(values)
        if 'product_cw_uom_qty' in values:
            self.filtered(lambda l: l.order_id.state == 'purchase')._create_or_update_picking()
        return result

    @api.multi
    def _create_or_update_picking(self):
        for line in self:
            if line.product_id.type in ('product', 'consu'):
                if float_compare(line.product_cw_uom_qty, line.cw_qty_received, line.product_cw_uom.rounding) < 0:
                    raise UserError(_('You cannot decrease the ordered cw quantity below the received cw quantity.\n'
                                      'Create a return first.'))
        return super(PurchaseOrderLine, self)._create_or_update_picking()
