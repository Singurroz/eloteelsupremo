# -*- coding: utf-8 -*-
from odoo import _, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _supreme_get_config_percents(self):
        icp = self.env['ir.config_parameter'].sudo()
        return {
            'discount': float(icp.get_param('eloteelsupremo.payment_discount_percent', '5')),
            'points': float(icp.get_param('eloteelsupremo.payment_points_percent', '5')),
        }

    def _supreme_moned_program(self):
        return self.env['loyalty.program']._get_supreme_moned_program(self.env)

    def _supreme_points_program(self):
        return self.env['loyalty.program']._get_supreme_points_program(self.env)

    def _supreme_get_moned_spent_amount(self):
        self.ensure_one()
        moned_program = self._supreme_moned_program()
        if not moned_program:
            return 0.0
        spent = 0.0
        for line in self.order_line.filtered('is_reward_line'):
            if line.coupon_id.program_id == moned_program:
                spent += abs(line.price_total)
        return spent

    def _supreme_get_product_total(self):
        self.ensure_one()
        return sum(
            line.price_total
            for line in self.order_line
            if not line.is_reward_line and not line.display_type
        )

    def _supreme_credit_points_on_moned_payment(self):
        for order in self:
            spent = order._supreme_get_moned_spent_amount()
            if spent <= 0 or not order.partner_id:
                continue
            percents = order._supreme_get_config_percents()
            if percents['points'] <= 0:
                continue
            base_total = order._supreme_get_product_total()
            points_to_issue = base_total * (percents['points'] / 100.0)
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
                    percents['points'],
                ),
                'used': 0,
                'issued': points_to_issue,
            })

    def _get_reward_values_discount(self, reward, coupon, **kwargs):
        res = super()._get_reward_values_discount(reward, coupon, **kwargs)
        moned_program = self._supreme_moned_program()
        if not moned_program or coupon.program_id != moned_program:
            return res
        percents = self._supreme_get_config_percents()
        extra_discount_percent = percents['discount']
        if extra_discount_percent <= 0:
            return res
        product_total = self._supreme_get_product_total()
        extra_discount = product_total * (extra_discount_percent / 100.0)
        if extra_discount <= 0:
            return res
        for vals in res:
            vals['price_unit'] -= extra_discount / max(vals.get('product_uom_qty', 1), 1)
        return res

    def action_confirm(self):
        res = super().action_confirm()
        self._supreme_credit_points_on_moned_payment()
        return res
