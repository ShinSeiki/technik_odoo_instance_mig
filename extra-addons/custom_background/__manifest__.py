# -*- coding: utf-8 -*-

{
    'name': 'Custom Background',
    'version': '1.0',
    'category': 'Customization',
    'summary': 'Change background image for Odoo views',
    'depends': ['base', 'web'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/assets.xml',
    ],
    'installable': True,
    'application': False,
}
