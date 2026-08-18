# -*- coding: utf-8 -*-
{
    'name': 'Elote El Supremo',
    'version': '19.0.2.0.0',
    'category': 'Sales/Retail',
    'summary': 'Banco Supremo: Moned Supreme, Puntos Supremos, QR y pago en sucursal',
    'description': """
Ecosistema completo Elote El Supremo para Odoo 19 Community.

* Moned Supreme (moneda interna / eWallet)
* Puntos Supremos (programa de lealtad)
* Recargas en sucursal con bono del 10%
* Descuento 5% + puntos 5% al pagar con Moned Supreme
* QR de identificación y pago en tienda
* Pago en sucursal en eCommerce (sin pasarela)
    """,
    'author': 'Elote El Supremo y Emmanuel Cruz',
    'license': 'LGPL-3',
    'depends': [
        'eloteelsupremo_base',
        'eloteelsupremo_wallet',
        'eloteelsupremo_loyalty',
        'eloteelsupremo_payment',
        'eloteelsupremo_website',
        'eloteelsupremo_pos',
    ],
    'installable': True,
    'application': True,
}
