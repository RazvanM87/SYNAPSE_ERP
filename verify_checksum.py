import hashlib
import os
import json
from datetime import datetime

WATCHED_FILES = [
    'master_blueprint.json', 'master_blueprint.bak', 'sync_blueprint.py', 'generate_structure.py',
    'analyze_code.py', 'audit_integrity.py', 'daily_report.py', 'apply_headers.py', 'generate_docs.py',
    'extensions/docs/file_cabinet.py', 'ai/context_engine/dependency_mapper.py',
    'reports/qa/daily_report.txt', 'reports/qa/blueprint_index.json', 'reports/qa/snapshot_ai_context.json'
]

CHECKSUM_FILE = 'reports/qa/checksums.json'

# 🔹 Fișiere de exclus din verificare (backupuri, zipuri etc.)
EXCLUDE_PATTERNS = ['.zip', '.bak', '.tmp', '.log', '.pyc', '__pycache__']

def should_ignore(path):
    path_lower = path.lower()
    return any(p in path_lower for p in EXCLUDE_PATTERNS)

def generate_md5(path):
    try:
        if should_ignore(path):
            return None
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        return f'error: {e}'

def load_previous():
    if os.path.exists(CHECKSUM_FILE):
        with open(CHECKSUM_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_checksums(checksums):
    os.makedirs(os.path.dirname(CHECKSUM_FILE), exist_ok=True)
    with open(CHECKSUM_FILE, 'w', encoding='utf-8') as f:
        json.dump(checksums, f, indent=2)

def verify():
    print(f"\n🔐 VERIFICARE INTEGRITATE SYNAPSE ERP – {datetime.now():%Y-%m-%d %H:%M:%S}")

    previous, current, changed, missing, new_files = load_previous(), {}, [], [], []

    for path in WATCHED_FILES:
        if should_ignore(path):
            continue
        if not os.path.exists(path):
            missing.append(path)
            continue
        md5 = generate_md5(path)
        if md5 is None:
            continue
        current[path] = md5
        if path not in previous:
            new_files.append(path)
        elif previous[path] != md5:
            changed.append(path)

    if changed:
        print('\n⚠️  Fișiere modificate:')
        for c in changed:
            print(f'  - {c}')
    else:
        print('✅  Nicio modificare detectată.')

    if new_files:
        print('\n🆕  Fișiere noi:')
        for f in new_files:
            print(f'  - {f}')

    if missing:
        print('\n❌  Fișiere lipsă:')
        for f in missing:
            print(f'  - {f}')

    save_checksums(current)

    print('\n----------------------------------------------')
    if not changed and not missing:
        print('🟢  Integritate garantată. (Checksum OK)')
    else:
        print('🟠  Avertismente: Verificați modificările.')
    print('----------------------------------------------\n')

if __name__ == '__main__':
    verify()