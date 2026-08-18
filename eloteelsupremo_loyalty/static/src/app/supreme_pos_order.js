/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { floatIsZero } from "@web/core/utils/numbers";

patch(PosOrder.prototype, {
    _getRewardLineValues({ reward, coupon_id, product, price, quantity, cost }) {
        const lineValues = super._getRewardLineValues({
            reward,
            coupon_id,
            product,
            price,
            quantity,
            cost,
        });
        if (!Array.isArray(lineValues)) {
            return lineValues;
        }
        const program = reward.program_id;
        if (
            program.program_type !== "ewallet" ||
            program.supreme_program_kind !== "moned"
        ) {
            return lineValues;
        }
        const config = this.config;
        const discountPercent = config.supreme_payment_discount_percent || 0;
        if (floatIsZero(discountPercent)) {
            return lineValues;
        }
        const productTotal = this.getOrderlines().reduce(
            (sum, line) => sum + line.price_subtotal_incl,
            0
        );
        const extraDiscount = productTotal * (discountPercent / 100);
        if (floatIsZero(extraDiscount)) {
            return lineValues;
        }
        for (const vals of lineValues) {
            vals.price_unit += extraDiscount;
        }
        return lineValues;
    },
});
