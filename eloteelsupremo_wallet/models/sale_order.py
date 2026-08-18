# -*- coding: utf-8 -*-
from odoo import _, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _supreme_apply_recharge_bonus(self):
        self.ensure_one()
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

        recharged_amount = sum(
            line.price_total
            for line in self.order_line
            if line.product_id == recharge_product and not line.is_reward_line
        )
        if recharged_amount <= 0 or not self.partner_id:
            return

        bonus_points = recharged_amount * (bonus_percent / 100.0)
        self.partner_id._ensure_supreme_cards()
        card = self.partner_id._get_supreme_moned_card()
        if not card:
            return

        card.sudo().with_context(loyalty_no_mail=True).write({
            'points': card.points + bonus_points,
        })
        self.env['loyalty.history'].sudo().create({
            'card_id': card.id,
            'order_model': self._name,
            'order_id': self.id,
            'description': _('Bono recarga Moned Supreme (%s%%)', bonus_percent),
            'used': 0,
            'issued': bonus_points,
        })

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            order._supreme_apply_recharge_bonus()
        return res
