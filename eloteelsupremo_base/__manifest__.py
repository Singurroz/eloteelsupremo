# -*- coding: utf-8 -*-
{
    'name': 'Elote El Supremo — Base',
    'version': '19.0.2.0.0',
    'category': 'Sales/Retail',
    'summary': 'Configuración base de Banco Supremo: Moned Supreme y Puntos Supremos',
    'description': """
Base del ecosistema Elote El Supremo.

* Programas de fidelidad: Moned Supreme (eWallet) y Puntos Supremos.
* Producto de recarga tipo tiempo aire.
* Tarjeta virtual por cliente (número de miembro).
* Parámetros configurables (bono recarga, descuento, puntos).
    """,
    'author': 'Elote El Supremo y Emmanuel Cruz',
    'license': 'LGPL-3',
    'depends': [
        'loyalty',
        'sale_loyalty',
        'website_sale_loyalty',
        'pos_loyalty',
        'payment_custom',
        'website_sale',
    ],
    'data': [
        'security/eloteelsupremo_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/product_data.xml',
        'data/loyalty_program_data.xml',
        'data/ir_config_parameter_data.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
        'views/loyalty_program_views.xml',
        'views/eloteelsupremo_menus.xml',
    ],
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/res_users_demo.xml',
        'demo/product_demo.xml',
    ],
    'installable': True,
    'application': False,
}
