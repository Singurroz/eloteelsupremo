# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


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

    @api.model
    def _supreme_demo_ensure_spei_payment_method(self):
        """Crea el método de pago Transferencia SPEI para el ambiente demo."""
        PosPaymentMethod = self.env['pos.payment.method'].sudo()
        existing = PosPaymentMethod.search([('name', '=', 'Transferencia SPEI')], limit=1)
        if existing:
            method = existing
        else:
            journal = self.env['account.journal'].sudo().search([
                ('type', '=', 'bank'),
                ('company_id', '=', self.env.company.id),
            ], limit=1)
            vals = {
                'name': _('Transferencia SPEI'),
                'split_transactions': True,
            }
            if journal:
                vals['journal_id'] = journal.id
            method = PosPaymentMethod.create(vals)

        configs = self.search([])
        for config in configs:
            config.write({
                'payment_method_ids': [(4, method.id)],
                'supreme_qr_enabled': True,
            })
        return method
