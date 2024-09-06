from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    pos_type = fields.Selection([
        ('full', 'Punto de Venta y Caja'),
        ('order_only', 'Solo Registro de Pedidos')
    ], string='Tipo de POS', default='full', required=True)
