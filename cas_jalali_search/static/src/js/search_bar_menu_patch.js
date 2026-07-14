/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { SearchBarMenu } from "@web/search/search_bar_menu/search_bar_menu";

import { JalaliDateFilterDialog } from "./jalali_date_filter_dialog";

function dateFieldRank(field) {
    const preferredNames = [
        "date",
        "date_from",
        "date_start",
        "start_date",
        "birthday",
        "create_date",
        "write_date",
    ];
    const index = preferredNames.indexOf(field.name);
    return index === -1 ? preferredNames.length : index;
}

patch(SearchBarMenu.prototype, {
    setup() {
        super.setup(...arguments);
        this.jalaliDialogService = useService("dialog");
    },

    get jalaliDateFields() {
        const fields = [];

        for (const [name, definition] of Object.entries(
            this.env.searchModel.searchViewFields || {}
        )) {
            if (!["date", "datetime"].includes(definition.type)) {
                continue;
            }
            if (definition.searchable === false) {
                continue;
            }

            fields.push({
                name,
                string: definition.string || name,
                type: definition.type,
            });
        }

        return fields.sort((left, right) => {
            const rankDifference =
                dateFieldRank(left) - dateFieldRank(right);
            if (rankDifference) {
                return rankDifference;
            }
            return left.string.localeCompare(right.string, "fa");
        });
    },

    get hasJalaliDateFields() {
        return this.jalaliDateFields.length > 0;
    },

    onAddJalaliDateFilterClick() {
        const fields = this.jalaliDateFields;
        if (!fields.length) {
            return;
        }

        this.jalaliDialogService.add(JalaliDateFilterDialog, {
            fields,
            onApply: ({ description, domain }) => {
                this.env.searchModel.createNewFilters([
                    {
                        description,
                        domain,
                    },
                ]);
            },
        });
    },
});
