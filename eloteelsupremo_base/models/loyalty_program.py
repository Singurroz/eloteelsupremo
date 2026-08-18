# -*- coding: utf-8 -*-
from odoo import fields, models


class LoyaltyProgram(models.Model):
    _inherit = 'loyalty.program'

    supreme_program_kind = fields.Selection(
        selection=[
            ('moned', 'Moned Supreme'),
            ('puntos', 'Puntos Supremos'),
        ],
        string='Tipo Banco Supremo',
        copy=False,
    )

    def _is_supreme_moned_program(self):
        self.ensure_one()
        return self.supreme_program_kind == 'moned'

    def _is_supreme_points_program(self):
        self.ensure_one()
        return self.supreme_program_kind == 'puntos'

    @classmethod
    def _get_supreme_moned_program(cls, env):
        return env.ref('eloteelsupremo_base.loyalty_program_moned_supreme', raise_if_not_found=False)

    @classmethod
    def _get_supreme_points_program(cls, env):
        return env.ref('eloteelsupremo_base.loyalty_program_puntos_supremos', raise_if_not_found=False)
