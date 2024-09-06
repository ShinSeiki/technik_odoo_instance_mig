{
    'name': 'Stock Lot Expiry Date',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Allow setting expiry date for lots during stock moves',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_move_line_views.xml',
    ],
    'installable': True,
    'application': False,
}
