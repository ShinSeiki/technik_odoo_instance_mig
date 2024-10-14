# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, api, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    create_from_pos = fields.Boolean(string="Created From POS", default=False)

    @api.model
    def create_order_from_ui(self, order):
        order_id = self.search([
            ('partner_id', '=', order['partner_id']),
            ('create_from_pos', '=', True),
            ('state', '=', 'draft')
        ])
        if order_id:
            for line in order['order_line']:
                orderLine = self.env['sale.order.line'].search([
                    ('order_id', '=', order_id.id),
                    ('product_id', '=', line[2]['product_id'])
                ])
                if orderLine:
                    orderLine.product_uom_qty += line[2]['product_uom_qty']
                else:
                    orderLine.create({
                        'product_id': line[2]['product_id'],
                        'product_uom_qty': line[2]['product_uom_qty'],
                        'order_id': order_id.id
                    })
        else:
            order_id = self.create(order)
        order_ref = self.browse(order_id.id).name
        return [order_ref, order['order_line']]

    @api.model
    def get_sale_order_lines(self, ref):
        result = []
        order_id = self.search([('id', '=', ref)], limit=1)
        if order_id:
            lines = self.env['sale.order.line'].search([('order_id', '=', order_id.id)])
            for line in lines:
                new_vals = {
                    'product_id': line.product_id.id,
                    'product': line.product_id.name,
                    'qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                }
                result.append(new_vals)

        return [result]
