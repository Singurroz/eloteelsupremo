# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    custom_mode = fields.Selection(
        selection_add=[('store_payment', 'Pago en sucursal')],
        ondelete={
            'store_payment': lambda providers: providers.write({'custom_mode': 'wire_transfer'}),
        },
    )

    @api.model
    def _get_provider_domain(self, provider_code, *, custom_mode='', **kwargs):
        res = super()._get_provider_domain(provider_code, custom_mode=custom_mode, **kwargs)
        if provider_code == 'custom' and custom_mode == 'store_payment':
            from odoo.fields import Domain
            return Domain.AND([res, [('custom_mode', '=', 'store_payment')]])
        return res

    def _get_default_payment_method_codes(self):
        self.ensure_one()
        if self.code == 'custom' and self.custom_mode == 'store_payment':
            return ['store_payment']
        return super()._get_default_payment_method_codes()
