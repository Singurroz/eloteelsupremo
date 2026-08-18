# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    supreme_member_number = fields.Char(
        string='Número de miembro Supremo',
        copy=False,
        readonly=True,
        index=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        partners._assign_supreme_member_number()
        return partners

    def _assign_supreme_member_number(self):
        partners = self.filtered(lambda p: not p.supreme_member_number and not p.is_company)
        for partner in partners:
            partner.supreme_member_number = self.env['ir.sequence'].next_by_code('supreme.member')

    def _get_supreme_moned_card(self):
        self.ensure_one()
        program = self.env.ref(
            'eloteelsupremo_base.loyalty_program_moned_supreme',
            raise_if_not_found=False,
        )
        if not program:
            return self.env['loyalty.card']
        return self.env['loyalty.card'].search([
            ('partner_id', '=', self.id),
            ('program_id', '=', program.id),
        ], limit=1)

    def _get_supreme_points_card(self):
        self.ensure_one()
        program = self.env.ref(
            'eloteelsupremo_base.loyalty_program_puntos_supremos',
            raise_if_not_found=False,
        )
        if not program:
            return self.env['loyalty.card']
        return self.env['loyalty.card'].search([
            ('partner_id', '=', self.id),
            ('program_id', '=', program.id),
        ], limit=1)

    def _ensure_supreme_cards(self):
        """Crea las tarjetas Moned Supreme y Puntos Supremos si no existen."""
        LoyaltyCard = self.env['loyalty.card'].sudo()
        for partner in self:
            for program_xmlid in (
                'eloteelsupremo_base.loyalty_program_moned_supreme',
                'eloteelsupremo_base.loyalty_program_puntos_supremos',
            ):
                program = self.env.ref(program_xmlid, raise_if_not_found=False)
                if not program:
                    continue
                card = LoyaltyCard.search([
                    ('partner_id', '=', partner.id),
                    ('program_id', '=', program.id),
                ], limit=1)
                if not card:
                    LoyaltyCard.with_context(loyalty_no_mail=True).create({
                        'program_id': program.id,
                        'partner_id': partner.id,
                        'points': 0,
                    })
