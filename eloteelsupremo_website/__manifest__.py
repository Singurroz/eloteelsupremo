# -*- coding: utf-8 -*-
{
    'name': 'Elote El Supremo — Portal Web',
    'version': '19.0.2.0.0',
    'category': 'Website/Website',
    'summary': 'Portal del cliente: saldo Moned Supreme, QR identificación y pago',
    'author': 'Elote El Supremo y Emmanuel Cruz',
    'license': 'LGPL-3',
    'depends': ['eloteelsupremo_wallet', 'eloteelsupremo_loyalty', 'website'],
    'data': [
        'views/portal_templates.xml',
        'views/pwa_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'eloteelsupremo_website/static/src/js/supreme_portal.js',
            'eloteelsupremo_website/static/src/scss/supreme_portal.scss',
        ],
    },
    'installable': True,
    'application': False,
}
