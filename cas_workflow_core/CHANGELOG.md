# CAS Workflow Core changelog

## 19.0.1.0.2 — Foundation RC3

- make automated tests use a dedicated active internal responsible user;
- pass the responsible user explicitly from test and smoke execution paths;
- add regression coverage for inactive and nonexistent responsible users;
- retain strict server-side responsible-user validation;
- distinguish workflow-version and workflow-state field labels;
- update RC3 deployment, verification and transactional smoke tooling.

## 19.0.1.0.1 — Foundation RC2

- change the workflow target-model deletion policy to the Odoo-supported mode;
- install the initial versioned and auditable workflow foundation.
# 19.0.1.0.3

- Added target-model authorization hooks for safely assigning a business-specific
  responsible user and executing explicitly delegated transitions.
- Kept the default workflow permission contract unchanged for models that do not
  implement these server-side hooks.
