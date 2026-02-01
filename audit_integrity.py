import os, json, re
from datetime import datetime

BLUEPRINT_FILE = 'master_blueprint.json'
SEARCH_DIRS = ['core','operational','automations','ai','extensions','bi','frontend']
MARKER_PATTERN = re.compile(r'@synapse-feature:\s*([A-Z0-9_.\-]+)')

def load_blueprint():
    if not os.path.exists(BLUEPRINT_FILE):
        print(f"⚠️ Fișierul {BLUEPRINT_FILE} nu există — audit oprit.")
        return None
    with open(BLUEPRINT_FILE,'r',encoding='utf-8') as f:
        return json.load(f)

def extract_features_from_code():
    features, unmarked = {}, []
    for base_dir in SEARCH_DIRS:
        if not os.path.exists(base_dir):
            continue
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.py'):
                    path = os.path.join(root, file)
                    with open(path,'r',encoding='utf-8',errors='ignore') as f:
                        text = f.read()
                    found = MARKER_PATTERN.findall(text)
                    if found:
                        for fid in found:
                            features.setdefault(fid, []).append(path)
                    elif '__init__' not in file and text.strip():
                        unmarked.append(path)
    return features, unmarked

def audit():
    data = load_blueprint()
    if not data: return

    print(f"\n🧾 AUDIT SYNAPSE ERP – {datetime.now():%Y-%m-%d %H:%M:%S}")

    blueprint_ids = {f['id'] for w in data['waves'] for m in w['modules'] for f in m['functions']}
    code_features, unmarked = extract_features_from_code()
    code_ids = set(code_features.keys())

    missing, extra = blueprint_ids - code_ids, code_ids - blueprint_ids

    print(f"\n📋 Funcționalități definite: {len(blueprint_ids)}  |  Detectate în cod: {len(code_ids)}")

    if missing:
        print('\n❌ Lipsă în cod:')
        for i in sorted(missing): print(f'  - {i}')
    if extra:
        print('\n⚠️ Extra în cod:')
        for i in sorted(extra): print(f'  - {i}')
    if unmarked:
        print(f"\n🚧 Fișiere nemarcate ({len(unmarked)}):")
        for u in unmarked: print(f'  - {u}')

    total = len(missing) + len(extra) + len(unmarked)
    print('\n-------------------------------------------')
    if total == 0:
        print('🟢 Perfect sincronizat între blueprint și cod.')
    else:
        print(f'🟠 {total} neconcordanțe găsite în total.')
    print('-------------------------------------------\n')

if __name__ == '__main__':
    audit()