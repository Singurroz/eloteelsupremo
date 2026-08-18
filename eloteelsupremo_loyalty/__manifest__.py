# -*- coding: utf-8 -*-
{
    'name': 'Elote El Supremo — Puntos Supremos',
    'version': '19.0.2.0.0',
    'category': 'Sales/Retail',
    'summary': 'Reglas 5% descuento + 5% Puntos Supremos al pagar con Moned Supreme',
    'author': 'Elote El Supremo y Emmanuel Cruz',
    'license': 'LGPL-3',
    'depends': ['eloteelsupremo_wallet', 'pos_loyalty'],
    'assets': {
        'point_of_sale._assets_pos': [
            'eloteelsupremo_loyalty/static/src/app/supreme_pos_order.js',
        ],
    },
    'installable': True,
    'application': False,
}
