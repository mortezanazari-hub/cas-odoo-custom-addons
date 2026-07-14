# CAS Core

Technical foundation for Chodan Ara Shomal custom Odoo modules.

- Never modify Odoo Community core directly.
- Put business models in focused modules that depend on `cas_core`.
- Use Odoo inheritance and extension mechanisms.
- Add access-control files before adding persistent business models.
- Never commit secrets, database dumps, filestore data, or private keys.
