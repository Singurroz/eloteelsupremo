# -*- coding: utf-8 -*-
{
    'name': 'Elote El Supremo — Pago en Sucursal',
    'version': '19.0.2.0.0',
    'category': 'Accounting/Payment Providers',
    'summary': 'Proveedor de pago "Recarga / Pago en sucursal" sin pasarela',
    'author': 'Elote El Supremo y Emmanuel Cruz',
    'license': 'LGPL-3',
    'depends': ['eloteelsupremo_base', 'website_sale'],
    'data': [
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml',
    ],
    'installable': True,
    'application': False,
}
