/** @odoo-module **/

import { Component, onMounted, onWillStart, useExternalListener, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const GROUP_LABELS = {
    main: "فضای من",
    process: "فرم و فرایند",
    records: "اسناد و تأیید",
    operations: "عملیات منابع انسانی",
    reports: "گزارش و کنترل",
};

export class CasOrganizationalWorkspace extends Component {
    static template = "cas_workspace.OrganizationalWorkspace";

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.searchInput = useRef("searchInput");
        this.groupLabels = GROUP_LABELS;
        this.state = useState({
            loading: true,
            pageLoading: false,
            refreshing: false,
            route: "dashboard",
            query: "",
            sidebarCollapsed: false,
            mobileOpen: false,
            userMenu: false,
            detail: null,
            navigation: { items: [], installed_modules: [] },
            data: { user: {}, actions: [], letters: [], stats: {}, today: null },
            page: { title: "", subtitle: "", icon: "fa-circle-o", rows: [], columns: [], total: 0, offset: 0, limit: 25, available: true },
        });
        onWillStart(async () => {
            const saved = window.localStorage.getItem("cas.workspace.sidebar.collapsed");
            this.state.sidebarCollapsed = saved === "1";
            await Promise.all([this.loadDashboard(), this.loadNavigation()]);
            this.state.loading = false;
        });
        onMounted(() => this.searchInput.el?.focus());
        useExternalListener(window, "keydown", (event) => this.onKeydown(event));
    }

    get navGroups() {
        const groups = [];
        for (const key of ["main", "process", "records", "operations", "reports"]) {
            const items = this.state.navigation.items.filter((item) => item.group === key);
            if (items.length) groups.push({ key, label: GROUP_LABELS[key], items });
        }
        return groups;
    }

    get settingsItem() {
        return this.state.navigation.items.find((item) => item.key === "settings");
    }

    get totalPages() {
        return Math.max(1, Math.ceil((this.state.page.total || 0) / this.state.page.limit));
    }

    get currentPage() {
        return Math.floor((this.state.page.offset || 0) / this.state.page.limit) + 1;
    }

    get persianToday() {
        const raw = this.state.data.today;
        if (!raw) return "امروز";
        return new Intl.DateTimeFormat("fa-IR", { weekday: "long", day: "numeric", month: "long", year: "numeric" }).format(new Date(`${raw}T12:00:00`));
    }

    async loadNavigation() {
        this.state.navigation = await this.orm.call("cas.workspace.dashboard", "get_navigation", []);
    }

    async loadDashboard(refresh = false) {
        this.state.refreshing = refresh;
        try {
            this.state.data = await this.orm.call("cas.workspace.dashboard", "get_workspace_data", []);
        } catch (error) {
            this.notification.add("بارگذاری فضای کار انجام نشد. دوباره تلاش کنید.", { type: "danger" });
            throw error;
        } finally {
            this.state.refreshing = false;
        }
    }

    async loadPage() {
        if (this.state.route === "dashboard") return;
        this.state.pageLoading = true;
        try {
            this.state.page = await this.orm.call("cas.workspace.dashboard", "get_page_data", [
                this.state.route,
                this.state.query,
                this.state.page.offset || 0,
                this.state.page.limit || 25,
            ]);
        } catch (error) {
            this.notification.add("اطلاعات این بخش بارگذاری نشد.", { type: "danger" });
            throw error;
        } finally {
            this.state.pageLoading = false;
        }
    }

    async navigate(route) {
        this.state.route = route;
        this.state.query = "";
        this.state.detail = null;
        this.state.mobileOpen = false;
        this.state.userMenu = false;
        this.state.page = { title: "", subtitle: "", icon: "fa-circle-o", rows: [], columns: [], total: 0, offset: 0, limit: 25, available: true };
        if (route === "dashboard") {
            await this.loadDashboard();
        } else {
            await this.loadPage();
        }
        requestAnimationFrame(() => document.querySelector(".cas-workspace__scroll")?.scrollTo({ top: 0 }));
    }

    async submitSearch() {
        if (this.state.route === "dashboard") {
            await this.navigate("actions");
            return;
        }
        this.state.page.offset = 0;
        await this.loadPage();
    }

    async changePage(direction) {
        const next = Math.max(0, this.state.page.offset + direction * this.state.page.limit);
        if (next >= this.state.page.total && direction > 0) return;
        this.state.page.offset = next;
        await this.loadPage();
        document.querySelector(".cas-workspace__scroll")?.scrollTo({ top: 0, behavior: "smooth" });
    }

    async openDetail(route, id) {
        this.state.detail = { loading: true, title: "در حال بارگذاری…", fields: [] };
        const detail = await this.orm.call("cas.workspace.dashboard", "get_record_detail", [route, id]);
        this.state.detail = detail || null;
    }

    onRowKeydown(event, row) {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            this.openDetail(this.state.route, row.id);
        }
    }

    async openDashboardAction(item) {
        await this.navigate("actions");
        await this.openDetail("actions", item.id);
    }

    async openDashboardLetter(letter) {
        await this.navigate("letters");
        await this.openDetail("letters", letter.id);
    }

    toggleSidebar() {
        this.state.sidebarCollapsed = !this.state.sidebarCollapsed;
        window.localStorage.setItem("cas.workspace.sidebar.collapsed", this.state.sidebarCollapsed ? "1" : "0");
    }

    onKeydown(event) {
        if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
            event.preventDefault();
            this.searchInput.el?.focus();
        }
        if (event.key === "Escape") {
            this.state.detail = null;
            this.state.mobileOpen = false;
            this.state.userMenu = false;
        }
    }

    formatDate(value, includeTime = false) {
        if (!value) return "بدون مهلت";
        const normalized = value.includes("T") ? value : value.replace(" ", "T") + (value.includes(":") ? "Z" : "T12:00:00");
        const date = new Date(normalized);
        const options = includeTime ? { day: "numeric", month: "long", hour: "2-digit", minute: "2-digit" } : { year: "numeric", month: "2-digit", day: "2-digit" };
        return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat("fa-IR", options).format(date);
    }

    logout() {
        window.location.assign("/web/session/logout?redirect=/web/login");
    }
}

registry.category("actions").add("cas_workspace.organizational_workspace", CasOrganizationalWorkspace);
