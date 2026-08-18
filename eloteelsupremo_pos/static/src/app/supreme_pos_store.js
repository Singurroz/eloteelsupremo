/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { _t } from "@web/core/l10n/translation";
import { barcodeReaderService } from "@point_of_sale/app/services/barcode_reader_service";

if (!barcodeReaderService.dependencies.includes("pos")) {
    barcodeReaderService.dependencies.push("pos");
}

patch(PosStore.prototype, {
    getSupremeMonedProgram() {
        return this.models["loyalty.program"].find((p) => p.supreme_program_kind === "moned");
    },

    async supremeProcessQr(code) {
        if (!this.config.supreme_qr_enabled) {
            this.notification.add(_t("QR Banco Supremo deshabilitado en este punto de venta."), {
                type: "warning",
            });
            return;
        }

        const order = this.getOrder();
        const orderUuid = order && !order.finalized ? order.uuid : false;

        let result;
        try {
            result = await this.data.call("pos.session", "supreme_process_qr", [
                [this.session.id],
                code,
                orderUuid,
            ]);
        } catch (error) {
            this.notification.add(error.message || _t("Error al procesar QR."), { type: "danger" });
            return;
        }

        if (!result.success) {
            this.notification.add(result.message || _t("QR no válido."), { type: "danger" });
            return;
        }

        if (result.type === "identify") {
            await this._supremeSetPartner(result.partner_id);
            this.notification.add(result.message, { type: "info", title: _t("Banco Supremo") });
            return;
        }

        if (result.type === "payment") {
            await this._supremeApplyPaymentQr(result);
        }
    },

    async _supremeSetPartner(partnerId) {
        const order = this.getOrder();
        if (!order || order.finalized) {
            return;
        }
        const partner = this.models["res.partner"].get(partnerId);
        if (partner) {
            order.setPartner(partner);
            await this.updateRewards();
        }
    },

    async _supremeApplyPaymentQr(result) {
        const order = this.getOrder();
        const hasOrderLines = order && order.getOrderlines().length > 0;
        const orderDue = order ? order.priceIncl : 0;

        if (order && hasOrderLines && orderDue > 0) {
            await this._supremeSetPartner(result.partner_id);
            order.supreme_qr_token_id = result.token_id;
            const applyResult = await this._supremeApplyMonedEwallet(order);
            if (applyResult !== true) {
                await this.data.call("supreme.qr.token", "cancel_reserved_token", [result.token_id]);
                order.supreme_qr_token_id = false;
                this.notification.add(applyResult || _t("No se pudo aplicar Moned Supreme."), {
                    type: "danger",
                });
                return;
            }
            await this.updateRewards();
            this.notification.add(result.message, { type: "success", title: _t("Banco Supremo") });
            return;
        }

        this.notification.add(result.message, { type: "success", title: _t("Banco Supremo") });
    },

    async _supremeApplyMonedEwallet(order) {
        const monedProgram = this.getSupremeMonedProgram();
        if (!monedProgram) {
            return _t("Programa Moned Supreme no configurado.");
        }
        await this.updateRewards();
        const claimable = order.getClaimableRewards();
        const ewalletEntry = claimable.find(
            (entry) =>
                entry.reward.program_id.id === monedProgram.id &&
                entry.reward.program_id.program_type === "ewallet"
        );
        if (!ewalletEntry) {
            return _t("El cliente no tiene saldo Moned Supreme disponible.");
        }
        const applyResult = order._applyReward(
            ewalletEntry.reward,
            ewalletEntry.coupon_id,
            {}
        );
        return applyResult;
    },
});

const _barcodeStart = barcodeReaderService.start.bind(barcodeReaderService);
barcodeReaderService.start = async function (env, deps) {
    const reader = await _barcodeStart(env, deps);
    const pos = deps.pos;
    const originalScan = reader._scan.bind(reader);
    reader._scan = async function (code) {
        if (code && code.includes("SUPREMO:")) {
            if (pos) {
                await pos.supremeProcessQr(code);
            }
            return;
        }
        return originalScan(code);
    };
    return reader;
};
