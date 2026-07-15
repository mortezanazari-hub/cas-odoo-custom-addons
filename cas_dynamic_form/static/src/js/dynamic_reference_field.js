/** @odoo-module **/

import { Component, onMounted, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class DynamicReferenceField extends Component {
    static template = "cas_dynamic_form.DynamicReferenceField";
    static props = {
        field: Object,
        value: { optional: true },
        readonly: { type: Boolean, optional: true },
        onChange: Function,
    };
    static defaultProps = { readonly: false };

    setup() {
        this.orm = useService("orm");
        this.state = useState({ loading: true, query: "", options: [] });
        this.searchTimer = null;
        // Reference lookup must never block the first OWL render. Odoo may
        // take a few seconds to answer name_search on a cold worker, so load
        // options only after the form has already been mounted.
        onMounted(() => {
            // Do not return the RPC promise to OWL's mounted hook. The form
            // must be committed to the DOM before reference options arrive.
            void this.loadOptions();
        });
    }

    get selectedId() {
        if (this.props.value && typeof this.props.value === "object") {
            return Number(this.props.value.id || 0);
        }
        return Number(this.props.value || 0);
    }

    async loadOptions() {
        this.state.loading = true;
        try {
            const options = await this.orm.call(
                "cas.form.field",
                "runtime_reference_options",
                [[this.props.field.id], this.state.query, 100]
            );
            const selected = this.props.value;
            if (
                selected &&
                typeof selected === "object" &&
                selected.id &&
                !options.some((option) => option.id === selected.id)
            ) {
                options.unshift({ id: selected.id, name: selected.display_name });
            }
            this.state.options = options;
        } catch {
            this.state.options = [];
        } finally {
            this.state.loading = false;
        }
    }

    onSearch(event) {
        this.state.query = event.target.value;
        clearTimeout(this.searchTimer);
        this.searchTimer = setTimeout(() => this.loadOptions(), 300);
    }

    onSelect(event) {
        const value = Number(event.target.value || 0);
        this.props.onChange(value || null);
    }
}
