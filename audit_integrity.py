import os
import json
import re
from datetime import datetime

BLUEPRINT_FILE = 'master_blueprint.json'
SEARCH_DIRS = ['core', 'operational', 'frontend', 'ai', 'automations', 'bi', 'extensions']
MARKER_PATTERN = re.compile(r'@synapse-feature:\s*([A-Z0-9_.-]+)')


def load_blueprint():
    if not os.path.exists(BLUEPRINT_FILE):
        print(f"⚠️ Fișierul {BLUEPRINT_FILE} nu există — auditul este oprit.")
        return None
    with open(BLUEPRINT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_features_from_code():
    features = {}
    unmarked_files = []

    for base_dir in SEARCH_DIRS:
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.py'):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                        found = MARKER_PATTERN.findall(text)
                        if found:
                            for fid in found:
                                features.setdefault(fid, []).append(path)
                        else:
                            # exclude __init__.py sau fișiere complet goale
                            if '__init__' not in file and text.strip():
                                unmarked_files.append(path)
    return features, unmarked_files


def audit():
    data = load_blueprint()
    if not data:
        return

    print(f"\n🧾 AUDIT SYNAPSE ERP – Verificare coerență completă {datetime.now()}")

    blueprint_ids = set()
    for wave in data['waves']:
        for module in wave['modules']:
            for func in module['functions']:
                blueprint_ids.add(func['id'])

    code_features, unmarked = extract_features_from_code()
    code_ids = set(code_features.keys())

    # 🔸 Cazuri detectate
    missing_in_code = blueprint_ids - code_ids
    extra_in_code = code_ids - blueprint_ids

    print("\n📌 Rezultate audit:")
    print(f"- Funcționalități definite în Blueprint: {len(blueprint_ids)}")
    print(f"- Funcționalități detectate în cod: {len(code_ids)}")

    # 🔹 1. Funcționalități lipsă în cod
    if missing_in_code:
        print(f"\n❌ Funcționalități definite dar lipsă din cod:")
        for fid in sorted(missing_in_code):
            print(f"  - {fid}")
    else:
        print("✅ Toate funcționalitățile Blueprint au corespondent în cod.")

    # 🔹 2. Funcționalități extra în cod
    if extra_in_code:
        print(f"\n⚠️ Funcționalități non‑blueprint detectate în cod:")
        for fid in sorted(extra_in_code):
            print(f"  - {fid}")
    else:
        print("✅ Niciun ID neautorizat detectat în cod.")

    # 🔹 3. Fișiere Python nemarcate logic
    if unmarked:
        print(f"\n🚧 Fișiere Python fără @ synapse‑feature (dar cu conținut logic): {len(unmarked)}")
        for path in unmarked:
            print(f"  - {path}")
    else:
        print("✅ Toate fișierele relevante sunt corect marcate.")

    # 🔹 4. Rezumat final
    total_problems = len(missing_in_code) + len(extra_in_code) + len(unmarked)
    print("\n-------------------------------------------")
    if total_problems == 0:
        print(f"🟢 AUDIT COMPLET – Structură și logică perfect sincronizate.")
    else:
        print(f"🟠 AUDIT FINALIZAT CU AVERTISĂRI – {total_problems} neconcordanțe găsite.")
    print("-------------------------------------------\n")


if __name__ == '__main__':
    audit()