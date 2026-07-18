/** @odoo-module **/

import { Component, onWillStart, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const NODE_TYPES = [
    { kind: "initial", label: "شروع", icon: "fa-play", color: "green" },
    { kind: "normal", label: "مرحله", icon: "fa-square-o", color: "blue" },
    { kind: "final", label: "پایان موفق", icon: "fa-check", color: "purple" },
    { kind: "cancelled", label: "لغو", icon: "fa-times", color: "red" },
];

export class CasWorkflowNodeDesigner extends Component {
    static template = "cas_workflow_designer.NodeDesigner";

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");
        this.canvas = useRef("canvas");
        this.versionId = this.props.action.context.active_id;
        this.nodeTypes = NODE_TYPES;
        this.state = useState({
            loading: true, saving: false, graph: null,
            selectedNodeKey: null, selectedEdgeKey: null,
            connectingFrom: null, drag: null,
        });
        onWillStart(() => this.load());
    }

    get editable() { return this.state.graph?.state === "draft"; }
    get selectedNode() { return this.state.graph?.nodes.find((node) => node.key === this.state.selectedNodeKey); }
    get selectedEdge() { return this.state.graph?.edges.find((edge) => edge.key === this.state.selectedEdgeKey); }

    async load() {
        this.state.loading = true;
        this.state.graph = await this.orm.call("cas.workflow.version", "designer_get_graph", [[this.versionId]]);
        if (!this.state.graph.nodes.length && this.editable) this.seedGraph();
        this.state.loading = false;
    }

    seedGraph() {
        this.state.graph.nodes.push(
            { key: "start", name: "شروع", kind: "initial", x: 100, y: 260, color: "green", sla_hours: 0, fold: false },
            { key: "done", name: "پایان", kind: "final", x: 600, y: 260, color: "purple", sla_hours: 0, fold: false },
        );
        this.state.graph.edges.push({ key: "complete", name: "تکمیل", from: "start", to: "done", responsible_mode: "keep", note_required: false });
    }

    uniqueKey(prefix, collection) {
        const used = new Set(collection.map((item) => item.key));
        let index = 1;
        while (used.has(`${prefix}_${index}`)) index++;
        return `${prefix}_${index}`;
    }

    addNode(kind) {
        if (!this.editable) return;
        if (kind === "initial" && this.state.graph.nodes.some((node) => node.kind === "initial")) {
            this.notification.add("گراف فقط می‌تواند یک نود آغازین داشته باشد.", { type: "warning" });
            return;
        }
        const type = NODE_TYPES.find((item) => item.kind === kind);
        const key = this.uniqueKey(kind === "normal" ? "step" : kind, this.state.graph.nodes);
        const offset = this.state.graph.nodes.length * 28;
        this.state.graph.nodes.push({
            key, name: type.label, kind, x: 140 + (offset % 720), y: 120 + (offset % 420),
            color: type.color, sla_hours: 0, fold: false,
        });
        this.selectNode(key);
    }

    selectNode(key) {
        this.state.selectedNodeKey = key;
        this.state.selectedEdgeKey = null;
        if (this.state.connectingFrom && this.state.connectingFrom !== key) {
            this.addEdge(this.state.connectingFrom, key);
            this.state.connectingFrom = null;
        }
    }

    selectEdge(key) {
        this.state.selectedEdgeKey = key;
        this.state.selectedNodeKey = null;
        this.state.connectingFrom = null;
    }

    startConnection(key) {
        if (!this.editable) return;
        this.state.connectingFrom = this.state.connectingFrom === key ? null : key;
        this.state.selectedNodeKey = key;
    }

    addEdge(source, target) {
        if (source === target || this.state.graph.edges.some((edge) => edge.from === source && edge.to === target)) return;
        const key = this.uniqueKey("transition", this.state.graph.edges);
        this.state.graph.edges.push({ key, name: "انتقال جدید", from: source, to: target, responsible_mode: "keep", note_required: false });
        this.selectEdge(key);
    }

    deleteNode(key) {
        if (!this.editable) return;
        this.state.graph.nodes = this.state.graph.nodes.filter((node) => node.key !== key);
        this.state.graph.edges = this.state.graph.edges.filter((edge) => edge.from !== key && edge.to !== key);
        this.state.selectedNodeKey = null;
        if (this.state.connectingFrom === key) this.state.connectingFrom = null;
    }

    deleteEdge(key) {
        if (!this.editable) return;
        this.state.graph.edges = this.state.graph.edges.filter((edge) => edge.key !== key);
        this.state.selectedEdgeKey = null;
    }

    onNodePointerDown(ev, node) {
        if (!this.editable || ev.button !== 0 || ev.target.closest("button")) return;
        this.selectNode(node.key);
        this.state.drag = { key: node.key, startX: ev.clientX, startY: ev.clientY, nodeX: node.x, nodeY: node.y };
        ev.currentTarget.setPointerCapture(ev.pointerId);
    }

    onNodePointerMove(ev, node) {
        const drag = this.state.drag;
        if (!drag || drag.key !== node.key) return;
        node.x = Math.max(0, Math.min(4880, drag.nodeX + ev.clientX - drag.startX));
        node.y = Math.max(0, Math.min(4910, drag.nodeY + ev.clientY - drag.startY));
    }

    onNodePointerUp() { this.state.drag = null; }

    edgeLine(edge) {
        const source = this.state.graph.nodes.find((node) => node.key === edge.from);
        const target = this.state.graph.nodes.find((node) => node.key === edge.to);
        if (!source || !target) return { x1: 0, y1: 0, x2: 0, y2: 0, mx: 0, my: 0 };
        const x1 = source.x + 85, y1 = source.y + 45, x2 = target.x + 85, y2 = target.y + 45;
        return { x1, y1, x2, y2, mx: (x1 + x2) / 2, my: (y1 + y2) / 2 };
    }

    updateNode(ev, property) {
        const node = this.selectedNode;
        if (!node) return;
        let value = property === "fold" ? ev.target.checked : ev.target.value;
        if (property === "sla_hours") value = Number(value);
        if (property === "key") {
            const old = node.key;
            this.state.selectedNodeKey = value;
            for (const edge of this.state.graph.edges) {
                if (edge.from === old) edge.from = value;
                if (edge.to === old) edge.to = value;
            }
        }
        node[property] = value;
    }

    updateEdge(ev, property) {
        const edge = this.selectedEdge;
        if (!edge) return;
        const value = property === "note_required" ? ev.target.checked : ev.target.value;
        if (property === "key") this.state.selectedEdgeKey = value;
        edge[property] = value;
    }

    async save() {
        if (!this.editable || this.state.saving) return;
        this.state.saving = true;
        try {
            const payload = { nodes: this.state.graph.nodes, edges: this.state.graph.edges };
            this.state.graph = await this.orm.call(
                "cas.workflow.version", "designer_save_graph", [[this.versionId], payload, this.state.graph.revision]
            );
            this.notification.add("طراحی گردش‌کار ذخیره شد.", { type: "success" });
        } finally {
            this.state.saving = false;
        }
    }

    back() {
        this.action.doAction({ type: "ir.actions.act_window", res_model: "cas.workflow.version", res_id: this.versionId, views: [[false, "form"]] });
    }
}

registry.category("actions").add("cas_workflow_designer.node_designer", CasWorkflowNodeDesigner);
