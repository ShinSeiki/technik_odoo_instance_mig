from odoo import api, fields, models

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    expiration_date = fields.Date(string='Fecha de vencimiento')

    @api.onchange('lot_id', 'expiration_date')
    def _onchange_lot_expiration(self):
        if self.lot_id and self.expiration_date:
            self.lot_id.expiration_date = self.expiration_date

    def _action_done(self):
        res = super(StockMoveLine, self)._action_done()
        for move_line in self:
            if move_line.exists() and move_line.lot_id and move_line.expiration_date:
                move_line.lot_id.expiration_date = move_line.expiration_date
                move_line.lot_id.life_date = move_line.expiration_date
        return res
        
