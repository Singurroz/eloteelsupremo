# -*- coding: utf-8 -*-
from odoo import _, models
from odoo.exceptions import UserError


class PosSession(models.Model):
    _inherit = 'pos.session'

    def supreme_process_qr(self, payload, pos_order_uuid=False):
        """Procesa QR escaneado desde el POS."""
        self.ensure_one()
        if not self.config_id.supreme_qr_enabled:
            return {'success': False, 'message': _('QR Banco Supremo deshabilitado en este POS.')}
        try:
            is_payment = ':PAY:' in payload
            result = self.env['supreme.qr.token'].sudo().process_scanned_qr(
                payload,
                reserve_for_pos=bool(pos_order_uuid and is_payment),
            )
            return {'success': True, **result}
        except UserError as exc:
            return {'success': False, 'message': str(exc)}
        except Exception as exc:
            return {'success': False, 'message': str(exc)}

    def supreme_link_qr_token(self, token_id, pos_order_uuid):
        """Confirma reserva del token para una orden POS (UUID frontend)."""
        self.ensure_one()
        token = self.env['supreme.qr.token'].sudo().browse(token_id).exists()
        if not token:
            return {'success': False, 'message': _('Token no encontrado.')}
        try:
            token._check_payment_token_valid()
            if token.state == 'active':
                token.write({'state': 'reserved'})
            elif token.state != 'reserved':
                raise UserError(_('Token QR no disponible.'))
            return {
                'success': True,
                'token_id': token.id,
                'partner_id': token.partner_id.id,
                'amount': token.amount,
            }
        except UserError as exc:
            return {'success': False, 'message': str(exc)}
