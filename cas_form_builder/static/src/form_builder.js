/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const PALETTE = [
    ["short_text", "متن کوتاه", "fa-font"], ["long_text", "متن بلند", "fa-align-right"],
    ["integer", "عدد صحیح", "fa-hashtag"], ["decimal", "عدد اعشاری", "fa-calculator"],
    ["boolean", "بله / خیر", "fa-toggle-on"], ["date", "تاریخ", "fa-calendar"],
    ["datetime", "تاریخ و ساعت", "fa-clock-o"], ["dropdown", "فهرست کشویی", "fa-list"],
    ["radio", "انتخاب رادیویی", "fa-dot-circle-o"], ["file", "فایل", "fa-paperclip"],
    ["image", "تصویر", "fa-image"], ["employee", "کارمند", "fa-user"],
    ["department", "واحد سازمانی", "fa-sitemap"], ["display", "متن نمایشی", "fa-info-circle"],
].map(([type, label, icon]) => ({ type, label, icon }));

export class CasVisualFormBuilder extends Component {
    static template = "cas_form_builder.VisualDesigner";

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");
        this.versionId = this.props.action.context.active_id;
        this.palette = PALETTE;
        this.state = useState({ loading: true, saving: false, schema: null, selectedKey: null, draggedKey: null });
        onWillStart(() => this.load());
    }

    get editable() { return this.state.schema?.state === "draft"; }
    get selected() { return this.state.schema?.fields.find((item) => item.key === this.state.selectedKey); }

    async load() {
        this.state.loading = true;
        this.state.schema = await this.orm.call("cas.form.version", "designer_get_schema", [[this.versionId]]);
        this.state.loading = false;
    }

    uniqueKey(prefix) {
        const used = new Set([
            ...this.state.schema.fields.map((item) => item.key),
            ...this.state.schema.sections.map((item) => item.key),
        ]);
        let index = 1;
        while (used.has(`${prefix}_${index}`)) index++;
        return `${prefix}_${index}`;
    }

    addField(type, sectionKey = null) {
        if (!this.editable) return;
        const palette = this.palette.find((item) => item.type === type) || this.palette[0];
        const key = this.uniqueKey(type === "short_text" ? "field" : type);
        const optionType = ["single_select", "multi_select", "radio", "dropdown", "tag"].includes(type);
        this.state.schema.fields.push({
            key, label: palette.label, type, required: false, readonly: false, reportable: true,
            placeholder: "", help_text: "", allowed_model: "", column_span: 1,
            section_key: sectionKey || this.state.schema.sections[0].key,
            options: optionType ? [{ key: "option_1", label: "گزینه ۱" }] : [],
        });
        this.state.selectedKey = key;
    }

    addSection() {
        if (!this.editable) return;
        const key = this.uniqueKey("section");
        this.state.schema.sections.push({ key, title: "بخش جدید", columns: 2 });
    }

    selectField(key) { this.state.selectedKey = key; }
    dragPalette(ev, type) { ev.dataTransfer.setData("text/plain", `palette:${type}`); }
    dragField(ev, key) { this.state.draggedKey = key; ev.dataTransfer.setData("text/plain", `field:${key}`); }
    dropSection(ev, sectionKey) {
        if (!this.editable) return;
        const data = ev.dataTransfer.getData("text/plain");
        if (data.startsWith("palette:")) this.addField(data.slice(8), sectionKey);
        if (data.startsWith("field:")) {
            const field = this.state.schema.fields.find((item) => item.key === data.slice(6));
            if (field) field.section_key = sectionKey;
        }
    }

    moveField(key, direction) {
        const fields = this.state.schema.fields;
        const index = fields.findIndex((item) => item.key === key);
        const target = index + direction;
        if (index >= 0 && target >= 0 && target < fields.length) [fields[index], fields[target]] = [fields[target], fields[index]];
    }

    removeField(key) {
        if (!this.editable) return;
        this.state.schema.fields = this.state.schema.fields.filter((item) => item.key !== key);
        if (this.state.selectedKey === key) this.state.selectedKey = null;
    }

    removeSection(key) {
        if (!this.editable || this.state.schema.sections.length === 1) return;
        const fallback = this.state.schema.sections.find((item) => item.key !== key).key;
        for (const field of this.state.schema.fields) if (field.section_key === key) field.section_key = fallback;
        this.state.schema.sections = this.state.schema.sections.filter((item) => item.key !== key);
    }

    updateSelected(ev, property) {
        if (!this.selected) return;
        const field = this.selected;
        let value = ["required", "readonly", "reportable"].includes(property) ? ev.target.checked : ev.target.value;
        if (property === "column_span") value = Number(value);
        if (property === "key") this.state.selectedKey = value;
        if (property === "type") {
            const optionType = ["single_select", "multi_select", "radio", "dropdown", "tag"].includes(value);
            if (optionType && !field.options.length) field.options.push({ key: "option_1", label: "گزینه ۱" });
            if (!optionType) field.options = [];
        }
        field[property] = value;
    }

    updateSection(ev, section, property) { section[property] = property === "columns" ? Number(ev.target.value) : ev.target.value; }
    addOption() { this.selected.options.push({ key: `option_${this.selected.options.length + 1}`, label: `گزینه ${this.selected.options.length + 1}` }); }
    removeOption(index) { this.selected.options.splice(index, 1); }
    updateOption(ev, index, property) { this.selected.options[index][property] = ev.target.value; }

    async save() {
        if (!this.editable || this.state.saving) return;
        this.state.saving = true;
        try {
            const payload = { sections: this.state.schema.sections, fields: this.state.schema.fields };
            this.state.schema = await this.orm.call(
                "cas.form.version", "designer_save_schema", [[this.versionId], payload, this.state.schema.revision]
            );
            this.notification.add("طراحی فرم ذخیره شد.", { type: "success" });
        } finally { this.state.saving = false; }
    }

    back() { this.action.doAction({ type: "ir.actions.act_window", res_model: "cas.form.version", res_id: this.versionId, views: [[false, "form"]] }); }
}

registry.category("actions").add("cas_form_builder.visual_designer", CasVisualFormBuilder);
