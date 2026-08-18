# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    supreme_qr_enabled = fields.Boolean(
        string='QR Banco Supremo',
        default=True,
        help='Habilita el escaneo de QR de identificación y pago Moned Supreme.',
    )
    supreme_payment_discount_percent = fields.Float(
        string='Descuento Moned Supreme (%)',
        compute='_compute_supreme_config',
    )
    supreme_payment_points_percent = fields.Float(
        string='Puntos Moned Supreme (%)',
        compute='_compute_supreme_config',
    )
    supreme_recharge_bonus_percent = fields.Float(
        string='Bono recarga (%)',
        compute='_compute_supreme_config',
    )

    @api.depends()
    def _compute_supreme_config(self):
        icp = self.env['ir.config_parameter'].sudo()
        discount = float(icp.get_param('eloteelsupremo.payment_discount_percent', '5'))
        points = float(icp.get_param('eloteelsupremo.payment_points_percent', '5'))
        bonus = float(icp.get_param('eloteelsupremo.recharge_bonus_percent', '10'))
        for config in self:
            config.supreme_payment_discount_percent = discount
            config.supreme_payment_points_percent = points
            config.supreme_recharge_bonus_percent = bonus

    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        for fname in (
            'supreme_qr_enabled',
            'supreme_payment_discount_percent',
            'supreme_payment_points_percent',
            'supreme_recharge_bonus_percent',
        ):
            if fname not in fields:
                fields.append(fname)
        return fields
