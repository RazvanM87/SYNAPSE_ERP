import os
import json
import sys
from datetime import datetime

# ==============================================================
# SYNAPSE ERP – MASTER STRUCTURE GENERATOR (2026)
# ==============================================================
# Creează structura completă de directoare și fișiere conform
# blueprintului ERP SYNAPSE 2026, incluzând fișiere __init__.py
# ==============================================================

STRUCTURE = {
    # --- LAYER 1: CORE SYSTEM ---
    "core": {
        "auth": ["auth_service.py", "auth_controller.py", "roles_permissions.py", "audit_log_service.py"],
        "config": [
            "settings_service.py", "preferences_service.py", "globals_manager.py",
            "db_connect.py", "db_builder.py",
            "metadata/forms_manager.py", "metadata/fields_manager.py", "metadata/relationships_map.py"
        ],
        "validation": ["validators.py", "formats_global.py"],
        "theming": ["theme_manager.py", "color_schemes.py"],
        "notifications": ["alerts_service.py"]
    },

    # --- LAYER 2: OPERATIONAL ---
    "operational": {
        "clients": ["client_service.py", "client_controller.py", "client_pricing.py"],
        "suppliers": ["supplier_service.py", "supplier_controller.py"],
        "products": ["product_service.py", "product_pricing.py", "bom_service.py"],
        "sales": ["sales_order.py", "offer.py", "delivery_note.py"],
        "purchases": ["purchase_request.py", "purchase_order.py", "receipt_note.py"],
        "invoices": ["invoice_service.py", "invoice_controller.py"],
        "payments": ["payment_service.py", "payment_ai.py"],
        "warehouse": ["inventory_service.py", "stock_transfer.py", "inventory_adjustment.py"],
        "accounting": ["chart_of_accounts.py", "general_ledger.py", "journal_entries.py", "cash_register.py", "bank_statement.py", "accounting_reports.py"],
        "costing": ["cost_centers.py", "cost_calculation.py", "internal_orders.py"],
        "hr": ["hr_data.py", "payroll.py", "salary_auto.py", "timesheet.py", "leave_management.py", "d112_ai.py", "revisal_export.py"]
    },

    # --- LAYER 3: AUTOMATIONS ---
    "automations": {
        "flows": ["workflow_designer.py", "ai_recommendations.py", "cron_jobs.py", "task_flow.py"],
        "triggers": ["config_event_service.py", "workflow_triggers.py", "scheduler_jobs.py"],
        "qa": ["auto_tests.py"]
    },

    # --- LAYER 4: AI SYSTEM ---
    "ai": {
        "learning": ["ai_extensions.py", "shadow_training_ai.py"],
        "predictions": ["sales_model.py", "ledger_forecast_ai.py"],
        "pricing": ["pricing_ai.py"],
        "reconciliation": ["payment_reconcile_ai.py"],
        "context_engine": ["dependency_mapper.py", "retraining_service.py", "ai_events_bridge.py"]
    },

    # --- LAYER 5: EXTENSIONS ---
    "extensions": {
        "connectors": ["api_connector.py", "webhook_orchestrator.py", "import_export_ai.py"],
        "docs": ["file_cabinet.py", "documentation_service.py"],
        "multisite": ["multitenant_core.py", "tenant_settings.py"]
    },

    # --- LAYER 6: BI ---
    "bi": {
        "dashboard": ["finance_dashboard.py", "drilldown_modules.py"],
        "reports": ["report_export.py", "alert_system.py", "financial_reporting.py"]
    },

    # --- LAYER 7: FRONTEND ---
    "frontend": {
        "ui": ["layout_manager.js", "theme_switcher.js", "user_preferences.js", "ui_settings_adapter.js"],
        "search": ["global_search_ai.js", "search_recommendations.js"],
        "help_center": ["help_center_ai.py", "tutorials_manager.py"]
    },

    # --- LAYER 8: TESTS ---
    "tests": {
        "core": ["test_auth.py", "test_rbac.py"],
        "operational": ["test_clients.py", "test_invoices.py", "test_hr.py"],
        "frontend": ["test_search_ai.py", "test_ui_theming.py"],
        "ai": ["test_pricing_ai.py", "test_sales_predictions.py"],
        "bi": ["test_dashboard.py", "test_drilldown.py", "test_finance_dashboard.py"]
    },

    # --- LAYER 9: REPORTS ---
    "reports": {
        "unit": [],
        "integration": [],
        "qa": []
    }
}

STATIC_FILES = [
    "master_blueprint.json",
    "sync_blueprint.py",
    "analyze_code.py",
    "daily_report.py",
    "apply_headers.py",
    "generate_docs.py",
    "header_template.txt"
]

def create_init_files(base_path):
    for root, dirs, files in os.walk(base_path):
        if "__pycache__" in root:
            continue
        if any(fname.endswith(".py") for fname in files):
            init_path = os.path.join(root, "__init__.py")
            if not os.path.exists(init_path):
                with open(init_path, "w", encoding="utf-8") as f:
                    f.write("# Generated __init__.py for Python package context\n")

def create_structure(base_path="."):
    print("\n🧱 Generare structură completă SYNAPSE ERP 2026...\n")

    for folder, subitems in STRUCTURE.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        if isinstance(subitems, dict):
            for subfolder, files in subitems.items():
                sub_path = os.path.join(folder_path, subfolder)
                os.makedirs(sub_path, exist_ok=True)

                for f in files:
                    file_path = os.path.join(sub_path, f)
                    if not os.path.exists(file_path):
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        with open(file_path, 'w', encoding='utf-8') as nf:
                            nf.write(f"# Placeholder for {f}\n")
                    else:
                        print(f"📄 Deja existent — omis: {file_path}")

    for f in STATIC_FILES:
        f_path = os.path.join(base_path, f)
        if not os.path.exists(f_path):
            open(f_path, 'w').close()

    create_init_files(base_path)
    print("\n✅ Structura completă SYNAPSE ERP 2026 și fișierele __init__.py au fost generate cu succes!\n")

# ==============================================================
# 🔹 FUNCȚIA OPȚIONALĂ DE ACTUALIZARE BLUEPRINT EXISTENT
# ==============================================================

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BLUEPRINT_FILE = os.path.join(BASE_PATH, "master_blueprint.json")
BACKUP_FILE = os.path.join(BASE_PATH, "master_blueprint.bak")

LAYER_MAP = {
    'core': 'Core',
    'operational': 'Operational',
    'automations': 'Automations',
    'ai': 'AI',
    'extensions': 'Extensions',
    'bi': 'BI',
    'frontend': 'Frontend'
}

def load_blueprint():
    if not os.path.exists(BLUEPRINT_FILE):
        print(f"⚠️  Fișierul {BLUEPRINT_FILE} nu există. Se va crea unul nou.")
        return {"project": "SYNAPSE ERP", "version": "1.1-auto", "waves": []}
    with open(BLUEPRINT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_blueprint(data):
    with open(BLUEPRINT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def create_backup():
    if os.path.exists(BLUEPRINT_FILE):
        os.replace(BLUEPRINT_FILE, BACKUP_FILE)
        print(f"💾 Backup creat: {BACKUP_FILE}")

def update_blueprint():
    data = load_blueprint()
    existing_ids = {f['id'] for w in data.get('waves', []) for m in w.get('modules', []) for f in m.get('functions', [])}
    added_count = 0

    for layer in STRUCTURE.keys():
        if layer not in LAYER_MAP:
            continue

        wave_entry = next((w for w in data['waves'] if w.get('title', '').lower() == layer.lower()), None)
        if not wave_entry:
            stage_num = len(data.get('waves', [])) + 1
            wave_entry = {
                'stage': f'E{stage_num}',
                'title': LAYER_MAP[layer],
                'modules': []
            }
            data['waves'].append(wave_entry)

        for module, files in STRUCTURE[layer].items():
            mod_entry = next((m for m in wave_entry['modules'] if m['name'] == module.capitalize()), None)
            if not mod_entry:
                mod_entry = {'name': module.capitalize(), 'functions': []}
                wave_entry['modules'].append(mod_entry)

            for f in files:
                if f.endswith('.py') and not f.startswith('__'):
                    fid = f"E{len(existing_ids)+added_count+1:02d}.{module[:3].upper()}.{layer[:3].upper()}.{len(existing_ids)+added_count+100:03d}"
                    title = f.replace('_', ' ').replace('.py', '').capitalize()
                    func_entry = {
                        'id': fid,
                        'title': title,
                        'layer': LAYER_MAP[layer],
                        'status': 'not_started'
                    }
                    mod_entry['functions'].append(func_entry)
                    added_count += 1

    save_blueprint(data)
    print(f"✅ Blueprint actualizat cu {added_count} funcționalități noi.")
    print(f"📄 Fișier actualizat: {BLUEPRINT_FILE}\n")

# ==============================================================
# 🏁 EXECUȚIE LOGICĂ PRINCIPALĂ
# ==============================================================
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--update-blueprint':
        print(f"\n🚀 ACTUALIZARE BLUEPRINT SYNAPSE ERP — {datetime.now():%Y-%m-%d %H:%M:%S}")
        create_backup()
        update_blueprint()
    else:
        create_structure("SYNAPSE_ERP")