# -*- coding: utf-8 -*-
from odoo import _, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def confirm_coupon_programs(self, coupon_data):
        result = super().confirm_coupon_programs(coupon_data)
        self._supreme_credit_points_on_moned_payment()
        return result

    def _supreme_moned_program(self):
        return self.env['loyalty.program']._get_supreme_moned_program(self.env)

    def _supreme_credit_points_on_moned_payment(self):
        moned_program = self._supreme_moned_program()
        if not moned_program:
            return
        percents = float(self.env['ir.config_parameter'].sudo().get_param(
            'eloteelsupremo.payment_points_percent', '5',
        ))
        if percents <= 0:
            return

        for order in self:
            moned_spent = sum(
                abs(line.price_subtotal_incl)
                for line in order.lines
                if line.is_reward_line
                and line.coupon_id.program_id == moned_program
            )
            if moned_spent <= 0 or not order.partner_id:
                continue

            product_total = sum(
                line.price_subtotal_incl
                for line in order.lines
                if not line.is_reward_line
            )
            points_to_issue = product_total * (percents / 100.0)
            if points_to_issue <= 0:
                continue

            order.partner_id._ensure_supreme_cards()
            points_card = order.partner_id._get_supreme_points_card()
            if not points_card:
                continue

            points_card.sudo().with_context(loyalty_no_mail=True).write({
                'points': points_card.points + points_to_issue,
            })
            self.env['loyalty.history'].sudo().create({
                'card_id': points_card.id,
                'order_model': order._name,
                'order_id': order.id,
                'description': _(
                    'Puntos Supremos por compra con Moned Supreme (%s%%)',
                    percents,
                ),
                'used': 0,
                'issued': points_to_issue,
            })
