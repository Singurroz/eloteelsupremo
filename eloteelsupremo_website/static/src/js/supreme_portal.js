/** @odoo-module **/

import { Interaction } from '@web/public/interaction';
import { registry } from '@web/core/registry';
import { rpc } from '@web/core/network/rpc';
import { _t } from '@web/core/l10n/translation';

function qrCodeSrc(payload, size = 256) {
    return `/report/barcode/QR/${encodeURIComponent(payload)}?width=${size}&height=${size}`;
}

function renderQrBox(container, payload) {
    if (!container || !payload) {
        return;
    }
    container.classList.remove('d-none');
    container.innerHTML = `
        <img src="${qrCodeSrc(payload)}"
             alt="${_t('QR Banco Supremo')}"
             class="o_supreme_qr_image border rounded bg-white p-2"
             width="256" height="256"/>
        <p class="small text-muted mt-2 mb-0">
            ${_t('Escanea con la caja Elote El Supremo')}
        </p>
    `;
}

export class SupremePortal extends Interaction {
    static selector = '.o_supreme_portal';

    setup() {
        const identifyBox = this.el.querySelector('#supreme_identify_qr');
        if (identifyBox?.dataset.payload) {
            renderQrBox(identifyBox, identifyBox.dataset.payload);
        }

        const generateBtn = this.el.querySelector('#supreme_generate_payment_qr');
        generateBtn?.addEventListener('click', () => this._generatePaymentQr());
    }

    async _generatePaymentQr() {
        const amountInput = this.el.querySelector('#supreme_payment_amount');
        const errorEl = this.el.querySelector('#supreme_payment_qr_error');
        const expireEl = this.el.querySelector('#supreme_payment_qr_expire');
        const qrBox = this.el.querySelector('#supreme_payment_qr');
        const amount = parseFloat(amountInput?.value || '0');

        errorEl?.classList.add('d-none');
        expireEl?.classList.add('d-none');

        if (!amount || amount <= 0) {
            if (errorEl) {
                errorEl.textContent = _t('Ingresa un monto válido.');
                errorEl.classList.remove('d-none');
            }
            return;
        }

        const result = await rpc('/my/banco-supremo/qr/payment', { amount });
        if (!result.success) {
            if (errorEl) {
                errorEl.textContent = result.error || _t('No se pudo generar el QR.');
                errorEl.classList.remove('d-none');
            }
            return;
        }

        renderQrBox(qrBox, result.payload);
        if (expireEl && result.expire_at) {
            expireEl.textContent = _t('Válido hasta: %s', new Date(result.expire_at).toLocaleString());
            expireEl.classList.remove('d-none');
        }
    }
}

registry.category('public.interactions').add('eloteelsupremo_website.supreme_portal', SupremePortal);
