/** @odoo-module **/

import { Component, onMounted, onWillStart, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const NAV_ITEMS = [
    { key: "workspace", label: "کارتابل من", icon: "fa-inbox", active: true },
    { key: "urgent", label: "اقدام‌های فوری", icon: "fa-bell-o" },
    { key: "actions", label: "همه کارها", icon: "fa-calendar-check-o", action: "cas_action_hub.action_cas_action_hub_all_visible" },
    { key: "forms", label: "فرم‌ها", icon: "fa-file-text-o", action: "cas_form_core.action_cas_form_submission" },
    { key: "workflows", label: "گردش‌کارها", icon: "fa-sitemap", action: "cas_workflow_core.action_cas_workflow_instance" },
    { key: "letters", label: "مکاتبات", icon: "fa-envelope-o", action: "cas_correspondence.action_correspondence_letters" },
    { key: "attendance", label: "حضور و کارکرد", icon: "fa-clock-o", action: "cas_attendance_core.action_cas_my_attendance_day" },
];

export class CasOrganizationalWorkspace extends Component {
    static template = "cas_workspace.OrganizationalWorkspace";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.searchInput = useRef("searchInput");
        this.navItems = NAV_ITEMS;
        this.state = useState({
            loading: true,
            refreshing: false,
            query: "",
            priority: "all",
            userMenu: false,
            data: { user: {}, actions: [], letters: [], stats: {}, today: null },
        });
        onWillStart(() => this.load());
        onMounted(() => this.searchInput.el?.focus());
    }

    get filteredActions() {
        const query = this.state.query.trim().toLocaleLowerCase("fa");
        return this.state.data.actions.filter((item) => {
            const matchesPriority = this.state.priority === "all" || item.priority === this.state.priority;
            const haystack = `${item.title} ${item.source} ${item.owner}`.toLocaleLowerCase("fa");
            return matchesPriority && (!query || haystack.includes(query));
        });
    }

    get persianToday() {
        const raw = this.state.data.today;
        if (!raw) return "امروز";
        return new Intl.DateTimeFormat("fa-IR", { weekday: "long", day: "numeric", month: "long", year: "numeric" }).format(new Date(`${raw}T12:00:00`));
    }

    async load(refresh = false) {
        this.state.refreshing = refresh;
        if (!refresh) this.state.loading = true;
        try {
            this.state.data = await this.orm.call("cas.workspace.dashboard", "get_workspace_data", []);
        } catch (error) {
            this.notification.add("بارگذاری فضای کار انجام نشد. دوباره تلاش کنید.", { type: "danger" });
            throw error;
        } finally {
            this.state.loading = false;
            this.state.refreshing = false;
        }
    }

    formatDate(value, includeTime = false) {
        if (!value) return "بدون مهلت";
        const date = new Date(value.replace(" ", "T") + "Z");
        const options = includeTime
            ? { day: "numeric", month: "long", hour: "2-digit", minute: "2-digit" }
            : { year: "numeric", month: "2-digit", day: "2-digit" };
        return new Intl.DateTimeFormat("fa-IR", options).format(date);
    }

    async openItem(item) {
        const result = await this.orm.call("cas.workspace.dashboard", "open_action_item", [item.id]);
        if (result) await this.action.doAction(result);
    }

    async openLetter(letter) {
        const result = await this.orm.call("cas.workspace.dashboard", "open_letter", [letter.id]);
        if (result) await this.action.doAction(result);
    }

    async navigate(item) {
        if (item.key === "workspace") return;
        if (item.key === "urgent") {
            this.state.priority = "immediate";
            return;
        }
        try {
            await this.action.doAction(item.action);
        } catch {
            this.notification.add("این بخش برای حساب شما در دسترس نیست.", { type: "warning" });
        }
    }

    showAllActions() {
        return this.action.doAction("cas_action_hub.action_cas_action_hub_all_visible");
    }

    showAllLetters() {
        return this.action.doAction("cas_correspondence.action_correspondence_letters");
    }

    clearFilters() {
        this.state.query = "";
        this.state.priority = "all";
        this.searchInput.el?.focus();
    }

    logout() {
        window.location.assign("/web/session/logout?redirect=/web/login");
    }
}

registry.category("actions").add("cas_workspace.organizational_workspace", CasOrganizationalWorkspace);
