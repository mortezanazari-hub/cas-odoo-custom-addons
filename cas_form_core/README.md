# CAS Form Core

Technical foundation for the Chodan Ara organizational form platform on Odoo
19 Community.

## Scope of this first foundation release

- stable form identities;
- company-scoped definitions;
- immutable published revisions;
- persistent field UUIDs across revisions;
- typed field metadata;
- versioned option values;
- a versioned layout tree;
- schema fingerprints;
- controlled publish/archive operations;
- access groups and company record rules;
- backend tests for publication and revision cloning.

Runtime submissions, typed answers, conditional rules, workflow, approvals and
business-specific work reports are intentionally developed in subsequent
reviewable slices.

## Security principles

- published structures cannot be edited or deleted;
- technical identities are stable after publication;
- ordinary form users receive read-only definition access;
- only the publisher group may publish or archive a revision;
- all records are restricted to the user's allowed companies;
- JSON metadata is declarative and must never contain executable Python or
  JavaScript.

