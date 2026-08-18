# -*- coding: utf-8 -*-
from odoo import _, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    supreme_qr_token_id = fields.Many2one(
        comodel_name='supreme.qr.token',
        string='Token QR de pago',
        readonly=True,
        copy=False,
    )

    def confirm_coupon_programs(self, coupon_data):
        result = super().confirm_coupon_programs(coupon_data)
        self._supreme_apply_recharge_bonus()
        self._supreme_consume_pending_qr_tokens()
        return result

    def _supreme_apply_recharge_bonus(self):
        program = self.env['loyalty.program']._get_supreme_moned_program(self.env)
        if not program:
            return
        bonus_percent = float(self.env['ir.config_parameter'].sudo().get_param(
            'eloteelsupremo.recharge_bonus_percent', '10',
        ))
        if bonus_percent <= 0:
            return
        recharge_product = self.env.ref(
            'eloteelsupremo_base.product_recharge_moned_supreme',
            raise_if_not_found=False,
        )
        if not recharge_product:
            return

        for order in self:
            recharged_amount = sum(
                line.price_subtotal_incl
                for line in order.lines
                if line.product_id == recharge_product and not line.is_reward_line
            )
            if recharged_amount <= 0 or not order.partner_id:
                continue

            bonus_points = recharged_amount * (bonus_percent / 100.0)
            order.partner_id._ensure_supreme_cards()
            card = order.partner_id._get_supreme_moned_card()
            if not card:
                continue

            card.sudo().with_context(loyalty_no_mail=True).write({
                'points': card.points + bonus_points,
            })
            self.env['loyalty.history'].sudo().create({
                'card_id': card.id,
                'order_model': order._name,
                'order_id': order.id,
                'description': _('Bono recarga Moned Supreme (%s%%)', bonus_percent),
                'used': 0,
                'issued': bonus_points,
            })

    def _supreme_consume_pending_qr_tokens(self):
        """Consume tokens QR reservados al validar la orden POS."""
        for order in self.filtered('supreme_qr_token_id'):
            token = order.supreme_qr_token_id
            if token.state in ('reserved', 'active'):
                token._mark_used_for_pos_order(order)
