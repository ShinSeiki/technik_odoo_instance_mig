import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    lot_id = fields.Many2one("stock.production.lot", "Lot", copy=False)
    life_date = fields.Datetime(related="lot_id.life_date")

    @api.onchange("product_id")
    def product_id_change(self):
        res = super().product_id_change()
        #self.lot_id = False
        _logger.info("ORDER LINE: change product_id 02")
        return res

    @api.onchange("product_id")
    def _onchange_product_id_set_lot_domain(self):
        _logger.info("ORDER LINE: change product_id")
        available_lot_ids = []
        self.lot_id = False
        if self.order_id.warehouse_id and self.product_id:
            location = self.order_id.warehouse_id.lot_stock_id
            quants = self.env["stock.quant"].read_group(
                [
                    ("product_id", "=", self.product_id.id),
                    ("location_id", "child_of", location.id),
                    ("quantity", ">", 0),
                    ("lot_id", "!=", False),
                ],
                ["lot_id"],
                "lot_id",
            )
            available_lot_ids = [quant["lot_id"][0] for quant in quants]
            result_lot_id = self.env["stock.move.line"].search([("lot_id", "in", available_lot_ids)], order="expiration_date", limit=1)
            if result_lot_id:
                self.lot_id = result_lot_id.lot_id
        return {"domain": {"lot_id": [("id", "in", available_lot_ids)]}}
