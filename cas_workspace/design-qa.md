# CAS Workspace Global Design System QA

- source visual truth path: `C:\Users\pishtazantech.com\.codex\generated_images\019f6a8f-7ff7-7773-ad20-fe7dc61dae73\exec-f562272b-7451-4880-abf3-53fb51a9d156.png`
- implementation URL: `http://192.168.1.227:8069/web#action=cas_workspace.action_cas_workspace`
- implementation screenshot path: unavailable because the Codex in-app browser runtime failed before browser initialization
- target viewport: 1487 x 1058 desktop
- state: authenticated internal user, global WebClient shell plus organizational workspace client action

## Full-view comparison evidence

The source image was opened at its original resolution and used to measure the full-screen RTL shell, 176 px navy right sidebar, 78 px top bar, urgent-action table, correspondence card, and daily-progress card. The same shell and token system were extended across Odoo list, form, kanban, activity, calendar, pivot, graph, settings, dialog, dropdown, chatter, visual form-builder, workflow-designer, responsive, print, and login surfaces. The live implementation could not be captured in the required in-app browser because the browser runtime returned `failed to write kernel assets: The system cannot find the path specified` before a tab could be created. A visual side-by-side comparison is therefore blocked.

## Focused region comparison evidence

Blocked for the same reason. The reference regions were inspected directly, but no browser-rendered implementation crop exists for typography, dense table alignment, or responsive-state comparison.

## Functional verification evidence

- Odoo module install and tagged module tests passed.
- The authenticated `cas.workspace.dashboard/get_workspace_data` RPC passed.
- The client action resolved as `ir.actions.client` with tag `cas_workspace.organizational_workspace`.
- The compiled Odoo JavaScript bundle contains the workspace action registration.
- The compiled Odoo CSS bundle contains the workspace styles.
- The compiled Odoo JavaScript bundle contains the global sidebar and global search components.
- The compiled Odoo CSS bundle contains the global shell and shared view-system styles and returns no CSS compilation error.
- The public frontend bundle contains the CAS login theme.
- All seven fixed sidebar destinations resolved successfully for the verification user.
- The web client returned HTTP 200.
- Primary interactions represented in code: global search, priority filters, refresh, action opening, correspondence opening, module navigation, account menu, and logout.
- Browser console errors checked: no, blocked before browser initialization.

## Findings

- [P1] Browser-rendered visual comparison unavailable
  - Location: full workspace.
  - Evidence: the source image is available, but no implementation screenshot could be captured.
  - Impact: exact fidelity of fonts, spacing, wrapping, and viewport behavior cannot be approved.
  - Fix: restore the Codex in-app browser runtime, capture the live action at 1487 x 1058, and compare both images in one visual input.

- [P2] Global page coverage lacks browser screenshots
  - Location: list, form, kanban, settings, builders, dialogs, mobile navigation, and login.
  - Evidence: the compiled bundles contain the intended selectors and components, but the blocked browser runtime prevented rendered captures.
  - Impact: dense tables, long Persian labels, overlays, and responsive breakpoints remain visually unapproved.
  - Fix: repeat capture on representative pages with realistic records after the browser runtime is restored.

## Required fidelity surfaces

- Fonts and typography: Vazirmatn-first Persian stack implemented globally; browser rendering and font availability remain unverified.
- Spacing and layout rhythm: measured desktop proportions and right-column offsets implemented for all backend actions; screenshot comparison remains blocked.
- Colors and visual tokens: navy, teal, white, border, warning, and danger tokens match the source direction; pixel sampling against a rendered capture remains blocked.
- Image quality and asset fidelity: generated CAS app icon is installed as a real PNG; UI icons use Font Awesome; browser sharpness and crop remain unverified.
- Copy and content: Persian labels and operational terminology match the selected concept and existing CAS modules; live populated wrapping across all view types remains unverified.

## Comparison history

- Iteration 1: source opened and implementation installed; browser capture failed before initialization. No visual fixes could be evidence-driven.
- Iteration 2: global WebClient shell and shared design tokens were installed. The first CSS build exposed an incompatible Sass `min()` expression; it was replaced with width plus max-width, and the rebuilt debug bundle returned no CSS error. Browser capture remained unavailable.
- Iteration 3: the user reported broken responsiveness and inconsistent menu behavior. Code review identified three structural causes: a custom search component injected into Odoo's responsive Navbar, a second custom apps menu competing with Odoo's own menu system, and physical right/left offsets plus forced component dimensions. The injected search and duplicate apps menu were removed, the Navbar was returned to Odoo ownership, sidebar offsets were converted to logical RTL properties, and forced navbar, control-panel, list-row, form-padding, kanban-padding, calendar-padding, and dialog-overflow rules were removed. Version 19.0.1.2.0 rebuilt with no CSS error and the debug JavaScript bundle no longer contains the removed global-search component. Browser capture remained unavailable.
- Iteration 4: the user reported that the sidebar still appeared on different sides in different actions. The remaining cause was that CSS logical `inline-start` depends on the computed direction of each Odoo container, and some actions intentionally use LTR containers. Both the global sidebar and the standalone workspace sidebar were changed to physical `right: 0; left: auto`, while navbar and action-manager offsets were changed to physical right margins. Odoo RTL compiler ignore directives were added around every physical positioning rule. The compiled Odoo debug CSS was inspected after deployment and preserves `right: 0`, `left: auto`, `margin-right: 176px`, and `margin-left: 0` with no CSS error. Browser capture remained unavailable.

## Implementation checklist

- Restore the in-app browser runtime.
- Capture the live workspace, one dense list, one long form, one kanban, both visual builders, one dialog, settings, and login at representative breakpoints.
- Compare the source and implementation together.
- Fix any P1/P2 visual differences and repeat the capture.

## Follow-up polish

- Validate the collapsed sidebar at tablet width and the stacked action cards at mobile width after desktop fidelity passes.

final result: blocked
