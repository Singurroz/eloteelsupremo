# -*- coding: utf-8 -*-
from odoo import fields, models


class LoyaltyCard(models.Model):
    _inherit = 'loyalty.card'

    supreme_member_number = fields.Char(
        related='partner_id.supreme_member_number',
        string='Número de miembro',
    )
