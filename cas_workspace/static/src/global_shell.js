/** @odoo-module **/

import { Component, onMounted, onWillStart, onWillUnmount, useExternalListener, useState } from "@odoo/owl";
import { useBus, useService } from "@web/core/utils/hooks";
import { routerBus } from "@web/core/browser/router";
import { WebClient } from "@web/webclient/webclient";

const SHELL_NAV_ITEMS = [
    { key: "workspace", label: "کارتابل من", icon: "fa-inbox", action: "cas_workspace.action_cas_workspace" },
    { key: "urgent", label: "اقدام‌های فوری", icon: "fa-bell-o", action: "cas_action_hub.action_cas_action_hub" },
    { key: "actions", label: "همه کارها", icon: "fa-calendar-check-o", action: "cas_action_hub.action_cas_action_hub_all_visible" },
    { key: "forms", label: "فرم‌ها", icon: "fa-file-text-o", action: "cas_form_core.action_cas_form_submission" },
    { key: "workflows", label: "گردش‌کارها", icon: "fa-sitemap", action: "cas_workflow_core.action_cas_workflow_instance" },
    { key: "letters", label: "مکاتبات", icon: "fa-envelope-o", action: "cas_correspondence.action_correspondence_letters" },
    { key: "attendance", label: "حضور و کارکرد", icon: "fa-clock-o", action: "cas_attendance_core.action_cas_my_attendance_day" },
];

export class CasGlobalSidebar extends Component {
    static template = "cas_workspace.GlobalSidebar";

    setup() {
        this.action = useService("action");
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.navItems = SHELL_NAV_ITEMS;
        this.previousDirection = document.documentElement.getAttribute("dir");
        this.state = useState({
            active: "workspace",
            mobileOpen: false,
            urgent: 0,
        });
        onWillStart(async () => {
            try {
                const data = await this.orm.call("cas.workspace.dashboard", "get_workspace_data", []);
                this.state.urgent = data.stats.urgent || 0;
            } catch {
                this.state.urgent = 0;
            }
        });
        onMounted(() => {
            document.body.classList.add("cas-global-theme");
            document.documentElement.setAttribute("dir", "rtl");
        });
        onWillUnmount(() => {
            document.body.classList.remove("cas-global-theme");
            if (this.previousDirection) document.documentElement.setAttribute("dir", this.previousDirection);
        });
        useExternalListener(window, "keydown", (event) => {
            if (event.key === "Escape") {
                this.state.mobileOpen = false;
            }
        });
        useBus(routerBus, "ROUTE_CHANGE", () => {
            this.state.mobileOpen = false;
        });
    }

    async navigate(item) {
        this.state.active = item.key;
        this.state.mobileOpen = false;
        try {
            await this.action.doAction(item.action, { clearBreadcrumbs: true });
        } catch {
            this.notification.add("این بخش برای حساب شما در دسترس نیست.", { type: "warning" });
        }
    }

    logout() {
        window.location.assign("/web/session/logout?redirect=/web/login");
    }
}

WebClient.components = { ...WebClient.components, CasGlobalSidebar };
