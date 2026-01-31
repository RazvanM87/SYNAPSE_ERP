import os

STRUCTURE = {
    # --- LAYER 1: CORE SYSTEM ---
    "core": {
        "auth": ["auth_service.py", "auth_controller.py"],
        "config": ["settings_service.py", "preferences_service.py"],
        "validation": ["validators.py", "formats_global.py"],
        "theming": ["theme_manager.py", "color_schemes.py"]
    },

    # --- LAYER 2: OPERAȚIONAL ---
    "operational": {
        "clients": ["client_service.py", "client_controller.py"],
        "suppliers": ["supplier_service.py", "supplier_controller.py"],
        "products": ["product_service.py", "product_controller.py", "bom_service.py"],
        "invoices": ["invoice_service.py", "invoice_controller.py"],
        "payments": ["payment_service.py", "payment_ai.py"],
        "hr": ["hr_data.py", "salary_auto.py", "d112_ai.py"]
    },

    # --- LAYER 3: FRONTEND ---
    "frontend": {
        "ui": ["theme_switcher.js", "layout_manager.js", "user_preferences.js"],
        "search": ["global_search_ai.js", "search_recommendations.js"],
        "help_center": ["help_center_ai.py", "tutorials_manager.py"]
    },

    # --- LAYER 4: AI ---
    "ai": {
        "predictions": ["sales_model.py"],
        "pricing": ["pricing_ai.py"],
        "reconciliation": ["payment_reconcile_ai.py"],
        "learning": ["ai_extensions.py", "shadow_training_ai.py"]
    },

    # --- LAYER 5: AUTOMATIZĂRI ---
    "automations": {
        "flows": ["workflow_designer.py", "drag_drop_engine.py", "ai_recommendations.py"],
        "qa": ["auto_tests.py"]
    },

    # --- LAYER 6: BI ---
    "bi": {
        "dashboard": ["finance_dashboard.py", "drilldown_modules.py"],
        "reports": ["report_export.py", "alert_system.py"]
    },

    # --- LAYER 7: EXTENSII ---
    "extensions": {
        "connectors": ["api_connector.py", "webhook_orchestrator.py"],
        "multisite": ["multitenant_core.py"],
        "docs": ["auto_blueprint_doc.py"]
    },

    # --- LAYER 8: TESTE ---
    "tests": {
        "core": ["test_auth.py", "test_rbac.py"],
        "operational": ["test_clients.py", "test_invoices.py", "test_hr.py"],
        "frontend": ["test_search_ai.py", "test_ui_theming.py"],
        "ai": ["test_pricing_ai.py"],
        "bi": ["test_dashboard.py", "test_drilldown.py"]
    },

    # --- LAYER 9: RAPOARTE ---
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

def create_structure(base_path="."):
    print("\n🧱 Generare structură COMPLETĂ SYNAPSE ERP (Frontend + AI Features)…\n")

    for folder, subitems in STRUCTURE.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        if isinstance(subitems, dict):
            for subfolder, files in subitems.items():
                sub_path = os.path.join(folder_path, subfolder)
                os.makedirs(sub_path, exist_ok=True)
                for f in files:
                    f_path = os.path.join(sub_path, f)
                    if not os.path.exists(f_path):
                        with open(f_path, 'w') as nf:
                            nf.write(f"# Placeholder for {f}\n")
                    else:
                        print(f"📄 Deja existent – omis: {f_path}")

    for f in STATIC_FILES:
        if not os.path.exists(os.path.join(base_path, f)):
            open(os.path.join(base_path, f), 'w').close()

    print("✅ Structura extinsă a fost generată complet!")

if __name__ == "__main__":
    create_structure()