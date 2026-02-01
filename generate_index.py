import os
import json
from datetime import datetime

BLUEPRINT_FILE = 'master_blueprint.json'
INDEX_FILE = 'reports/qa/blueprint_index.json'

MAP_RULES = {
    'core': ['auth', 'config', 'validation', 'theming', 'notifications'],
    'operational': ['clients', 'suppliers', 'products', 'sales', 'purchases', 'invoices', 'payments', 'warehouse', 'accounting', 'costing', 'hr'],
    'automations': ['flows', 'triggers', 'qa'],
    'ai': ['learning', 'predictions', 'pricing', 'reconciliation', 'context_engine'],
    'extensions': ['connectors', 'docs', 'multisite'],
    'bi': ['dashboard', 'reports'],
    'frontend': ['ui', 'search', 'help_center']
}

def generate_index():
    if not os.path.exists(BLUEPRINT_FILE):
        print(f"⚠️ Fișierul {BLUEPRINT_FILE} nu există – indexarea oprită.")
        return

    with open(BLUEPRINT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    index = {}
    for wave in data['waves']:
        stage = wave.get('stage', 'undefined')
        for module in wave['modules']:
            module_name = module['name']
            for func in module['functions']:
                fid = func['id']
                status = func.get('status', 'not_started')
                layer_guess = next((layer for layer, sub in MAP_RULES.items() if any(x.lower() in module_name.lower() for x in sub)), 'core')
                matching_category = next((cat for cat, sub in MAP_RULES.items() if module_name.lower() in sub), None)
                file_path = f"{layer_guess}/{module_name.lower()}/"
                index[fid] = {
                    'stage': stage,
                    'layer': layer_guess,
                    'module': module_name,
                    'status': status,
                    'suggested_path': file_path
                }

    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    with open(INDEX_FILE, 'w', encoding='utf-8') as out:
        json.dump(index, out, indent=2, ensure_ascii=False)

    print(f"📘 Blueprint Index generat → {INDEX_FILE} ({len(index)} funcționalități)")
    print(f"🕓 Timp execuție: {datetime.now()}\n")

if __name__ == '__main__':
    generate_index()