# Domain Model — CAS Workspace v8

| مشخصه | مقدار |
|---|---|
| وضعیت | `Consolidated` |
| نسخه | `v8 through iteration 12` |

## دامنه‌های اصلی

### Workspace Experience

- Workspace Shell
- Dashboard Configuration
- Widget Placement
- User UI Preference
- Command Palette
- Recent Resource Reference

### Personal Productivity

- Personal Task
- Personal Task Category

### Organizational Action

- Action Item
- Assignment to another person
- Action Lifecycle

### Organization

- Organization Unit
- Effective Assignment
- Reporting Relationship
- Delegation
- Scope Resolution

### Calendar

- Event
- Attendee
- Invitation
- Event Reminder

### Communication

- Conversation
- Message
- Mail Notification
- Correspondence، به‌عنوان دامنه رسمی جدا

### Work Reporting

- Work Report
- Work Report Section
- Report Profile
- Report Applicability
- Work Report Access Grant
- Evidence Relation
- Reporting Projection

### Dynamic Forms

- Form Definition
- Form Version
- Field/Section Definition
- Submission
- Answer
- Snapshot

### Process

- Workflow Definition/Instance
- Approval Request/Decision

### Activity Standardization

- Activity Definition
- Activity Proposal
- Evidence Policy
- KPI Mapping Reference

### Documents

- Attachment
- Document Metadata
- Evidence Binary

## روابط اصلی

```text
User/Employee
├── has Effective Assignments
├── owns Personal Tasks
├── attends Calendar Events
├── participates in Conversations
└── has Work Reports per Shift Occurrence

Shift Occurrence
└── identifies one Work Report per person

Work Report
├── contains one or more Sections
├── references Shift Snapshot
├── resolves Applicability
└── exposes State Projection

Work Report Section
├── references one Effective Assignment
├── pins one Form Version
├── references one Form Submission
├── resolves Reviewers
└── links Evidence and Activities

Access Grant
├── grants Operations
├── limits Scope
├── has Validity Period
└── is independent from Reporting Hierarchy
```

## Invariantها

1. هر Personal Task دقیقاً یک Owner دارد.
2. Task برای دیگری Personal Task نیست.
3. هر Work Report به یک شخص و Shift Occurrence یکتا متصل است.
4. هر Work Report Section به Assignment Snapshot معتبر متصل است.
5. Form Version گزارش تاریخی تغییر نمی‌کند.
6. Snapshot تاریخی Append-only یا Immutable است.
7. Access Grant منقضی یا لغوشده دسترسی ایجاد نمی‌کند.
8. Workspace هیچ Entity کسب‌وکاری بالا را کپی نمی‌کند.
9. Invitation به‌تنهایی Action ایجاد نمی‌کند.
10. Notification Record به‌تنهایی Business Action نیست.

## State Ownership

| State | مالک |
|---|---|
| Personal Task State | `cas_personal_task` |
| Action State | `cas_action_hub` |
| Event State | Calendar Domain |
| Message State | Odoo Mail/Discuss |
| Form Submission State | Form Engine |
| Workflow Process State | Workflow Core |
| Approval Decision | Approval Core |
| Work Report UX State | Projection در `cas_work_report` |

## Snapshotها

Snapshot باید برای این موارد حفظ شود:

- Assignment و Organization Context گزارش
- Shift start/end
- Form Version
- Activity title/description اولیه
- Report Profile Resolution
- Reviewer Resolution Source
- Evidence Policy مؤثر

Reopen یا Return نباید Snapshot تاریخی را پاک کند. Revision جدید باید قابل‌ردیابی باشد.

## Projectionها

Projection کپی مالکیت نیست و فقط برای Read/Reporting بهینه است. Projection باید:

- Source Record داشته باشد.
- Rebuildable باشد.
- Security Classification را حفظ کند.
- از Source of Truth مشتق شود.
- Lifecycle مستقل نسازد.