# -*- coding: utf-8 -*-
from odoo import _, http
from odoo.http import request


class SupremePwaController(http.Controller):

    @http.route('/eloteelsupremo/manifest.webmanifest', type='http', auth='public', website=True)
    def supreme_manifest(self):
        website = request.website
        name = website.name or _('Elote El Supremo')
        manifest = {
            'name': name,
            'short_name': _('Banco Supremo'),
            'description': _('Moned Supreme, Puntos Supremos y pagos con QR'),
            'start_url': '/my/banco-supremo',
            'scope': '/',
            'display': 'standalone',
            'background_color': '#ffffff',
            'theme_color': '#714B67',
            'lang': 'es-MX',
            'icons': [
                {
                    'src': '/web/static/img/odoo-icon-ios.png',
                    'sizes': '192x192',
                    'type': 'image/png',
                },
            ],
        }
        return request.make_json_response(manifest, headers={
            'Content-Type': 'application/manifest+json',
        })
