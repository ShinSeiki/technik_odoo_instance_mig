from odoo import api, fields, models
import base64

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    background_image = fields.Binary(string="Background Image")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        background_image = ICPSudo.get_param('custom_background.background_image', default=False)
        res.update(
            background_image=background_image and base64.b64decode(background_image),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('custom_background.background_image', self.background_image and base64.b64encode(self.background_image).decode('utf-8') or False)
