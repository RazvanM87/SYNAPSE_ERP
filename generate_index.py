import os
import json
from datetime import datetime

BLUEPRINT_FILE = 'master_blueprint.json'
INDEX_FILE = 'reports/qa/blueprint_index.json'

# 🔹 Mapează fiecare ID din Blueprint la locația sa logică (folder și fișier)
def generate_index():
    if not os.path.exists(BLUEPRINT_FILE):
        print(f"⚠️ Fișierul {BLUEPRINT_FILE} nu există – indexarea oprită.")
        return

    with open(BLUEPRINT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    index = {}

    for wave in data['waves']:
        stage = wave['stage']
        for module in wave['modules']:
            module_name = module['name']
            for func in module['functions']:
                fid = func['id']
                status = func.get('status', 'not_started')

                # Căutare rapidă a fișierului corespunzător (heuristică după layere)
                file_guess = None
                if 'AI' in fid or 'ai' in module_name.lower():
                    file_guess = 'ai/'
                elif 'HR' in fid:
                    file_guess = 'operational/hr/'
                elif 'FIN' in fid or 'PAY' in fid:
                    file_guess = 'operational/payments/'
                elif 'CLIENT' in module_name.upper() or 'CLI' in fid:
                    file_guess = 'operational/clients/'
                elif 'SUP' in fid:
                    file_guess = 'operational/suppliers/'
                elif 'PRD' in fid or 'PRODUCT' in module_name.upper():
                    file_guess = 'operational/products/'
                elif 'HELP' in fid:
                    file_guess = 'frontend/help_center/'
                elif 'SEARCH' in fid:
                    file_guess = 'frontend/search/'
                elif 'UI' in fid:
                    file_guess = 'frontend/ui/'
                elif 'BI' in fid:
                    file_guess = 'bi/dashboard/'
                elif 'AUTR' in fid or 'FLOW' in fid:
                    file_guess = 'automations/flows/'
                elif 'DOCS' in fid:
                    file_guess = 'extensions/docs/'
                else:
                    file_guess = 'core/'

                index[fid] = {
                    'stage': stage,
                    'module': module_name,
                    'status': status,
                    'suggested_path': file_guess
                }

    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    with open(INDEX_FILE, 'w', encoding='utf-8') as out:
        json.dump(index, out, indent=2, ensure_ascii=False)
    print(f"📘 Blueprint Index generat → {INDEX_FILE} ({len(index)} funcționalități)")
    print(f"🕓 Timp execuție: {datetime.now()}\n")

if __name__ == '__main__':
    generate_index()