# CAS Workspace Design QA

## Reference and scope

- Target: the selected custom RTL workspace concept with a fixed right navigation rail.
- Failure evidence: five user screenshots captured on 2026-07-18 at desktop widths.
- Build under review: `cas_workspace` 19.0.2.0.0.

## Confirmed pre-build findings

1. The dashboard and backend lists used two different shells.
2. Navigation launched raw Odoo actions, so the custom sidebar appeared pasted onto standard pages.
3. Urgent actions changed a dashboard filter instead of navigating to a dedicated page.
4. Settings launched the Users action instead of a settings experience.
5. Sidebar direction, active state, responsive behavior, and scrolling were inconsistent.
6. Several developed CAS modules were absent from navigation.

## Implemented corrections

- One client-action shell and internal router for all CAS sections.
- Sixteen navigation destinations, including all current CAS product areas.
- Persistent desktop collapse/expand and a mobile off-canvas sidebar.
- RTL direction and right-edge placement owned by the custom shell.
- Independent vertical scrolling for main content and long sidebar navigation.
- Dedicated custom data pages, search, pagination, empty/unavailable states, and record detail drawer.
- Custom settings hub with users and installed-module inventory.
- Legacy global sidebar injection and raw Odoo action navigation removed.

## Technical verification

- Python compilation: passed.
- XML parsing: passed.
- JavaScript syntax: passed.
- Odoo module upgrade and module tests: passed.
- All 15 data routes: available on the live database.
- Odoo SCSS compilation: passed after replacing unsupported mixed-unit `min()` rules.
- Compiled browser assets contain the new workspace and exclude the legacy sidebar.

## Visual verification gap

The browser-control connection failed before a post-deployment screenshot could be captured. The supplied screenshots verify the old failure state, but a same-viewport after screenshot is still required to judge visual match, interaction behavior, and responsive reflow.

final result: blocked
