#!/usr/bin/env bash
set -euo pipefail
DB="${1:-cas_odoo_dev}"
: "${CAS_DEMO_PASSWORD:=Demo@1405!}"
export CAS_DEMO_PASSWORD
/opt/odoo/venv/bin/python3 /opt/odoo/odoo/odoo-bin shell --config=/etc/odoo/odoo.conf -d "${DB}" --no-http < /opt/odoo/custom-addons/scripts/cas_full_demo.py
