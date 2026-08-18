# -*- coding: utf-8 -*-

from odoo import http
from odoo.exceptions import UserError, ValidationError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class SupremePortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        partner._ensure_supreme_cards()
        values.update({
            'supreme_member_number': partner.supreme_member_number,
            'supreme_moned_balance': partner._get_supreme_moned_card().points,
            'supreme_points_balance': partner._get_supreme_points_card().points,
        })
        return values

    @http.route('/my/banco-supremo', type='http', auth='user', website=True)
    def portal_banco_supremo(self, **kw):
        partner = request.env.user.partner_id
        partner._ensure_supreme_cards()
        moned_card = partner._get_supreme_moned_card()
        points_card = partner._get_supreme_points_card()
        identify_qr = request.env['supreme.qr.token'].sudo().generate_identify_qr(partner)
        values = {
            'page_name': 'banco_supremo',
            'partner': partner,
            'moned_card': moned_card,
            'points_card': points_card,
            'identify_qr_payload': identify_qr['payload'],
        }
        return request.render('eloteelsupremo_website.portal_banco_supremo', values)

    @http.route('/my/banco-supremo/qr/payment', type='jsonrpc', auth='user')
    def portal_generate_payment_qr(self, amount):
        partner = request.env.user.partner_id
        try:
            result = request.env['supreme.qr.token'].sudo().generate_payment_qr(partner, float(amount))
            return {
                'success': True,
                'payload': result['payload'],
                'amount': result['amount'],
                'expire_at': result['expire_at'].isoformat() if result['expire_at'] else False,
            }
        except (UserError, ValidationError) as exc:
            return {'success': False, 'error': str(exc)}
