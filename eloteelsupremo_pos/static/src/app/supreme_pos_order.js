/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    setup(vals) {
        super.setup(...arguments);
        if (vals.supreme_qr_token_id) {
            this.supreme_qr_token_id = vals.supreme_qr_token_id;
        }
    },

    serializeForORM(opts = {}) {
        const data = super.serializeForORM(opts);
        if (this.supreme_qr_token_id) {
            data.supreme_qr_token_id = this.supreme_qr_token_id;
        }
        return data;
    },
});
