# -*- coding: utf-8 -*-
import hashlib
import hmac
import secrets
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SupremeQrToken(models.Model):
    _name = 'supreme.qr.token'
    _description = 'Token QR Banco Supremo'
    _order = 'create_date desc'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        required=True,
        ondelete='cascade',
        index=True,
    )
    token_type = fields.Selection(
        selection=[
            ('identify', 'Identificación'),
            ('payment', 'Pago'),
        ],
        string='Tipo',
        required=True,
        default='payment',
    )
    amount = fields.Monetary(
        string='Monto',
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id,
    )
    token = fields.Char(required=True, index=True, copy=False)
    payload = fields.Char(string='Payload QR', copy=False)
    state = fields.Selection(
        selection=[
            ('active', 'Vigente'),
            ('reserved', 'Reservado'),
            ('used', 'Usado'),
            ('expired', 'Expirado'),
            ('cancelled', 'Cancelado'),
        ],
        default='active',
        required=True,
        index=True,
    )
    expire_at = fields.Datetime(string='Expira')
    pos_order_id = fields.Many2one(comodel_name='pos.order', string='Orden POS', readonly=True)
    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Pedido web', readonly=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company,
    )

    _token_unique = models.Constraint('UNIQUE(token)', 'El token QR debe ser único.')

    @api.model
    def _get_secret(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'eloteelsupremo.qr_secret',
        )
        if not param:
            param = secrets.token_hex(32)
            self.env['ir.config_parameter'].sudo().set_param('eloteelsupremo.qr_secret', param)
        return param

    @api.model
    def _get_ttl_minutes(self):
        return int(self.env['ir.config_parameter'].sudo().get_param(
            'eloteelsupremo.qr_token_ttl_minutes', '5',
        ))

    @api.model
    def _sign_payload(self, payload):
        signature = hmac.new(
            self._get_secret().encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()[:16]
        return f'{payload}:{signature}'

    @api.model
    def _verify_payload(self, full_payload):
        if ':' not in full_payload:
            raise ValidationError(_('QR inválido.'))
        payload, signature = full_payload.rsplit(':', 1)
        expected = hmac.new(
            self._get_secret().encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()[:16]
        if not hmac.compare_digest(signature, expected):
            raise ValidationError(_('QR no auténtico o alterado.'))
        return payload

    @api.model
    def _parse_payload(self, full_payload):
        payload = self._verify_payload(full_payload)
        parts = payload.split(':')
        if len(parts) < 3 or parts[0] != 'SUPREMO':
            raise ValidationError(_('Formato de QR no reconocido.'))
        return {
            'kind': parts[1],
            'partner_id': int(parts[2]),
            'extra': parts[3:],
        }

    def _check_payment_token_valid(self):
        self.ensure_one()
        if self.state not in ('active', 'reserved'):
            raise UserError(_('Este QR de pago ya fue utilizado o expiró.'))
        if self.expire_at and self.expire_at < fields.Datetime.now():
            self.state = 'expired'
            raise UserError(_('El QR de pago expiró. Genere uno nuevo.'))

    def _mark_used_for_pos_order(self, pos_order):
        """Marca el token como usado; el débito lo realiza la línea eWallet del POS."""
        self.ensure_one()
        self._check_payment_token_valid()
        self.write({
            'state': 'used',
            'pos_order_id': pos_order.id,
        })

    @api.model
    def generate_identify_qr(self, partner):
        partner.ensure_one()
        partner._ensure_supreme_cards()
        payload = f'SUPREMO:ID:{partner.id}:{partner.supreme_member_number or ""}'
        signed = self._sign_payload(payload)
        return {
            'payload': signed,
            'partner': partner,
            'moned_balance': partner._get_supreme_moned_card().points,
            'points_balance': partner._get_supreme_points_card().points,
        }

    @api.model
    def generate_payment_qr(self, partner, amount):
        partner.ensure_one()
        if amount <= 0:
            raise UserError(_('El monto del QR de pago debe ser mayor a cero.'))
        card = partner._get_supreme_moned_card()
        if not card or card.points < amount:
            raise UserError(_('Saldo insuficiente de Moned Supreme.'))
        token_value = secrets.token_urlsafe(16)
        ttl = self._get_ttl_minutes()
        expire_at = fields.Datetime.now() + timedelta(minutes=ttl)
        token_rec = self.sudo().create({
            'partner_id': partner.id,
            'token_type': 'payment',
            'amount': amount,
            'token': token_value,
            'expire_at': expire_at,
        })
        payload = f'SUPREMO:PAY:{partner.id}:{amount}:{token_value}'
        signed = self._sign_payload(payload)
        token_rec.payload = signed
        return {
            'payload': signed,
            'token_id': token_rec.id,
            'expire_at': expire_at,
            'amount': amount,
        }

    @api.model
    def _get_payment_token_from_payload(self, parsed):
        amount = float(parsed['extra'][0])
        token_value = parsed['extra'][1]
        token_rec = self.sudo().search([
            ('token', '=', token_value),
            ('partner_id', '=', parsed['partner_id']),
            ('token_type', '=', 'payment'),
        ], limit=1)
        if not token_rec:
            raise UserError(_('Token de pago no encontrado.'))
        if abs(token_rec.amount - amount) > 0.01:
            raise UserError(_('El monto del QR no coincide.'))
        token_rec._check_payment_token_valid()
        return token_rec

    @api.model
    def process_scanned_qr(self, full_payload, pos_order=None, reserve_for_pos=False):
        parsed = self._parse_payload(full_payload)
        partner = self.env['res.partner'].browse(parsed['partner_id']).exists()
        if not partner:
            raise UserError(_('Cliente no encontrado.'))

        if parsed['kind'] == 'ID':
            partner._ensure_supreme_cards()
            return {
                'type': 'identify',
                'partner_id': partner.id,
                'partner_name': partner.name,
                'member_number': partner.supreme_member_number,
                'moned_balance': partner._get_supreme_moned_card().points,
                'points_balance': partner._get_supreme_points_card().points,
                'message': _(
                    'Cliente %(name)s #%(number)s — Bienvenido. '
                    'Saldo Moned Supreme: %(moned)s | Puntos Supremos: %(points)s',
                    name=partner.name,
                    number=partner.supreme_member_number or '-',
                    moned=partner._get_supreme_moned_card().points,
                    points=partner._get_supreme_points_card().points,
                ),
            }

        if parsed['kind'] == 'PAY':
            token_rec = self._get_payment_token_from_payload(parsed)
            card = partner._get_supreme_moned_card()
            if not card or card.points < token_rec.amount:
                raise UserError(_('Saldo insuficiente de Moned Supreme.'))

            if reserve_for_pos:
                token_rec.write({'state': 'reserved'})
                return {
                    'type': 'payment',
                    'partner_id': partner.id,
                    'amount': token_rec.amount,
                    'token_id': token_rec.id,
                    'remaining_balance': card.points - token_rec.amount,
                    'message': _(
                        'QR válido: %(amount)s MS para %(name)s. Aplicando pago a la orden…',
                        amount=token_rec.amount,
                        name=partner.name,
                    ),
                }

            token_rec._consume_standalone()
            return {
                'type': 'payment',
                'partner_id': partner.id,
                'amount': token_rec.amount,
                'remaining_balance': card.points - token_rec.amount,
                'message': _(
                    'Pago recibido: %(amount)s MS. Saldo restante: %(balance)s',
                    amount=token_rec.amount,
                    balance=card.points,
                ),
            }

        raise UserError(_('Tipo de QR no soportado.'))

    def _consume_standalone(self):
        self.ensure_one()
        self._check_payment_token_valid()
        card = self.partner_id._get_supreme_moned_card()
        if not card or card.points < self.amount:
            raise UserError(_('Saldo insuficiente de Moned Supreme.'))
        card.sudo().with_context(loyalty_no_mail=True).write({
            'points': card.points - self.amount,
        })
        self.env['loyalty.history'].sudo().create({
            'card_id': card.id,
            'description': _('Pago QR Banco Supremo'),
            'used': self.amount,
            'issued': 0,
            'order_model': 'supreme.qr.token',
            'order_id': self.id,
        })
        self.write({'state': 'used'})

    @api.model
    def reserve_payment_token(self, token_id):
        token = self.browse(token_id).exists()
        if not token:
            raise UserError(_('Token de pago no encontrado.'))
        token._check_payment_token_valid()
        token.write({'state': 'reserved'})
        return token.id

    @api.model
    def cancel_reserved_token(self, token_id):
        token = self.browse(token_id).exists()
        if token and token.state == 'reserved':
            token.write({'state': 'active'})

    @api.model
    def _cron_expire_tokens(self):
        expired = self.search([
            ('state', 'in', ('active', 'reserved')),
            ('expire_at', '<', fields.Datetime.now()),
        ])
        expired.write({'state': 'expired'})
