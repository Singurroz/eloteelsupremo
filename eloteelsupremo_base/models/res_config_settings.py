# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    supreme_recharge_bonus_percent = fields.Float(
        string='Bono recarga Moned Supreme (%)',
        config_parameter='eloteelsupremo.recharge_bonus_percent',
        default=10.0,
    )
    supreme_payment_discount_percent = fields.Float(
        string='Descuento al pagar con Moned Supreme (%)',
        config_parameter='eloteelsupremo.payment_discount_percent',
        default=5.0,
    )
    supreme_payment_points_percent = fields.Float(
        string='Puntos Supremos por compra con Moned Supreme (%)',
        config_parameter='eloteelsupremo.payment_points_percent',
        default=5.0,
    )
    supreme_qr_token_ttl_minutes = fields.Integer(
        string='Vigencia QR de pago (minutos)',
        config_parameter='eloteelsupremo.qr_token_ttl_minutes',
        default=5,
    )
