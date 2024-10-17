# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name': 'POS Order On Account',
    'version': '13.0.1.1.0',
    'license': 'OPL-1',
    'summary': 'Reserve Order and Product with not paying any amount',
    'category': 'Point of Sale',
    'description': '''
        Reserve Order and Product on customer account without paying any amount 
        and when customer pay amount of order then order is confirm.
        create sale order from pos front end
    ''',
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'https://www.caretit.com',
    'depends': ['point_of_sale', 'sale_management'],
    'data': ['views/pos_template.xml'],
    'images': ['static/description/banner.jpg'],
    'price': 19.00,
    'currency': 'EUR',
    'qweb': ['static/src/xml/on_account.xml'],
}
