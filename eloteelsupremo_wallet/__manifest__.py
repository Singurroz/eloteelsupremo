# -*- coding: utf-8 -*-
{
    'name': 'Elote El Supremo — Moned Supreme (Wallet)',
    'version': '19.0.2.0.0',
    'category': 'Sales/Retail',
    'summary': 'Moned Supreme: recargas con bono, tarjeta virtual y tokens QR',
    'author': 'Elote El Supremo y Emmanuel Cruz',
    'license': 'LGPL-3',
    'depends': ['eloteelsupremo_base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/supreme_qr_token_views.xml',
        'views/loyalty_card_views.xml',
    ],
    'demo': [
        'demo/loyalty_card_demo.xml',
        'demo/supreme_qr_token_demo.xml',
    ],
    'installable': True,
    'application': False,
}
