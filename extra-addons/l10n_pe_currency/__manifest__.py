# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2019-TODAY OPeru.
#    Author      :  Grupo Odoo S.A.C. (<http://www.operu.pe>)
#
#    This program is copyright property of the author mentioned above.
#    You can`t redistribute it and/or modify it.
#
###############################################################################

{
    'name': 'Consulta Tipo de cambio Peru del día',
    'version': '15.0.1.0',
    'author': 'OPeru',
    'summary': 'Consulta Tipo de cambio Peru del día ',
    'description': '''  ''',
    'website': 'hhttp://www.operu.pe/facturacion-electronica',
    'depends': ['base','account'],
    "data": [
        'views/res_currency_view.xml',
        'data/ir_cron_data.xml',
        'views/res_config_settings_views.xml',
        'views/res_company_views.xml',
            ], 
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'sequence': 1,
    'support': 'modulos@operu.pe',
}
