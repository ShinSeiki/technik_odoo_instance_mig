# -*- coding: utf-8 -*-
{
    'name': 'Pdf restore',
    'version': '13.0',
    'category': 'Discuss',
    'summary': 'Restore the pdf invoice if it has been delete from files of the system',
    'description': "Restore the pdf invoice if it has been delete from files of the system, it happend at bad db restoring",
    'website': 'https://www.odoo.com/page/discuss',
    'depends': ['base'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
#        'views/views.xml',
        'views/ir_cron.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,

    'application': True,   
    'license': 'LGPL-3',

}
