{
    'name': 'POS Order Transfer',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Allow order transfer between POS',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_config_view.xml',
    ],
    'qweb': [
        'static/src/xml/pos_order_transfer.xml',
    ],
    'installable': True,
    'application': False,
}
