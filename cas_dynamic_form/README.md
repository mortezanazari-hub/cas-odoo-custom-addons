# CAS Dynamic Form Runtime

End-user runtime for the versioned CAS form engine on Odoo 19 Community.

## Version 1.0 scope

- Persian, RTL and responsive OWL client action;
- catalog of published forms;
- start a new submission and resume personal drafts;
- display recent submitted forms in read-only mode;
- render versioned pages, sections, groups, text and field nodes;
- short/long text, integer, decimal, percentage, monetary, Boolean, single and
  multiple options, radio, dropdown, tag, time and controlled record-reference
  inputs;
- Jalali Date and Datetime input with Gregorian/UTC persistence;
- client-side completion hints and basic validation;
- definitive server-side validation through `cas_form_core`;
- manual draft save, final submit, tracking number and immutable snapshot;
- secure bounded reference lookup under the caller's ACL and record rules.

## Explicitly deferred

- conditional rules and dynamic visibility;
- multi-step wizard navigation and per-step validation;
- attachment/image/signature widgets;
- autosave and offline recovery;
- workflow and approvals;
- department-specific availability, which belongs to the work-report/business
  layer;
- drag-and-drop builder and workflow designer.

## Security

The browser never writes `cas.form.answer` directly. All mutations pass through
the version-pinned submission service in `cas_form_core`. Related-record search
uses a backend whitelist and the current user's real Odoo access rights.
