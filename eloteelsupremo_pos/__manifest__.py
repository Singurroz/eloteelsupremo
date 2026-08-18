# -*- coding: utf-8 -*-
{
    'name': 'Elote El Supremo — POS QR',
    'version': '19.0.2.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Escaneo de QR Banco Supremo en punto de venta',
    'author': 'Elote El Supremo y Emmanuel Cruz',
    'license': 'LGPL-3',
    'depends': ['eloteelsupremo_loyalty', 'point_of_sale', 'pos_loyalty'],
    'data': [
        'views/pos_config_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'eloteelsupremo_pos/static/src/app/supreme_pos_store.js',
            'eloteelsupremo_pos/static/src/app/supreme_pos_order.js',
        ],
    },
    'demo': [
        'demo/pos_payment_method_demo.xml',
    ],
    'installable': True,
    'application': False,
}
