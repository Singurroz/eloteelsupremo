# -*- coding: utf-8 -*-
from odoo import api, models


class LoyaltyProgram(models.Model):
    _inherit = 'loyalty.program'

    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        if 'supreme_program_kind' not in fields:
            fields.append('supreme_program_kind')
        return fields
