/** @odoo-module **/

import { Component, onMounted, onWillStart, onWillUnmount, useExternalListener, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useBus, useService } from "@web/core/utils/hooks";
import { routerBus } from "@web/core/browser/router";
import { WebClient } from "@web/webclient/webclient";
import { NavBar } from "@web/webclient/navbar/navbar";

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
        this.menu = useService("menu");
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.root = useRef("root");
        this.navItems = SHELL_NAV_ITEMS;
        this.previousDirection = document.documentElement.getAttribute("dir");
        this.state = useState({
            active: "workspace",
            appsOpen: false,
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
                this.state.appsOpen = false;
                this.state.mobileOpen = false;
            }
        });
        useExternalListener(window, "click", (event) => {
            if (this.state.appsOpen && !event.target.closest(".cas-global-apps") && !event.target.closest(".cas-global-sidebar__apps-button")) {
                this.state.appsOpen = false;
            }
        });
        useBus(routerBus, "ROUTE_CHANGE", () => {
            this.state.mobileOpen = false;
        });
    }

    get apps() {
        return this.menu.getApps();
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

    async openApp(app) {
        this.state.appsOpen = false;
        this.state.mobileOpen = false;
        await this.menu.selectMenu(app);
    }

    toggleApps(event) {
        event.stopPropagation();
        this.state.appsOpen = !this.state.appsOpen;
    }

    logout() {
        window.location.assign("/web/session/logout?redirect=/web/login");
    }
}

export class CasGlobalSearch extends Component {
    static template = "cas_workspace.GlobalSearch";

    setup() {
        this.notification = useService("notification");
        this.input = useRef("input");
        this.state = useState({ query: "" });
        useExternalListener(window, "keydown", (event) => {
            if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
                event.preventDefault();
                this.input.el?.focus();
            }
        });
    }

    runSearch(event) {
        if (event.key !== "Enter") return;
        const target = document.querySelector(".o_action_manager .o_searchview_input");
        if (!target) {
            this.notification.add("در این صفحه جست‌وجوی سراسری وجود ندارد.", { type: "info" });
            return;
        }
        const valueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value")?.set;
        valueSetter?.call(target, this.state.query);
        target.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "insertText", data: this.state.query }));
        target.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", code: "Enter", bubbles: true }));
        target.focus();
    }
}

WebClient.components = { ...WebClient.components, CasGlobalSidebar };
NavBar.components = { ...NavBar.components, CasGlobalSearch };

registry.category("main_components").add("cas_workspace.global_theme_marker", {
    Component: class extends Component {
        static template = "cas_workspace.ThemeMarker";
    },
});
