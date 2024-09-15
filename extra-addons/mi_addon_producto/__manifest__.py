{
    'name': 'Producto Kanban Transparente',
    'version': '13.0.1.0.0',
    'category': 'Customizations',
    'summary': 'Modifica la vista kanban de productos',
    'author': 'Tu Nombre',
    'website': 'https://www.tuempresa.com',
    'depends': ['product', 'web'],
    'data': [
        'views/product_template_views.xml',
    ],
    'qweb': [],
    'application': False,
    'installable': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'mi_addon_producto/static/src/scss/product_kanban.scss',
        ],
    },
}
