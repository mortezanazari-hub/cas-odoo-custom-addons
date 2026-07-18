/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


export class CasActionHubSystray extends Component {
    static template = "cas_action_hub.Systray";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ open: 0, urgent: 0, overdue: 0, waiting: 0 });
        this.timer = null;
        onWillStart(async () => {
            await this.refresh();
            this.timer = setInterval(() => this.refresh(), 120000);
        });
        onWillUnmount(() => {
            if (this.timer) {
                clearInterval(this.timer);
            }
        });
    }

    async refresh() {
        const counts = await this.orm.call("cas.action.item", "get_my_counts", []);
        Object.assign(this.state, counts);
    }

    openHub() {
        return this.action.doAction("cas_action_hub.action_cas_action_hub");
    }
}

registry.category("systray").add("cas_action_hub.Systray", { Component: CasActionHubSystray }, { sequence: 25 });
