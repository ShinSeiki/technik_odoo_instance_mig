from odoo import fields, models

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    expiration_date = fields.Date(string='Fecha de vencimiento')
    
