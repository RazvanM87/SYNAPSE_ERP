import hashlib
import os
import json
from datetime import datetime

# 🔹 Fișiere critice urmărite (poți adăuga altele dacă dorești)
WATCHED_FILES = [
    'master_blueprint.json',
    'master_blueprint.bak',
    'sync_blueprint.py',
    'analyze_code.py',
    'daily_report.py',
    'audit_integrity.py',
    'generate_structure.py',
    'reports/qa/daily_report.txt'
]

CHECKSUM_FILE = 'reports/qa/checksums.json'

# 🧠 Generează hash MD5 al unui fișier
def generate_md5(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        return f"error: {e}"

# 🔍 Încarcă sau creează fișierul de referință al checksumurilor
def load_previous():
    if os.path.exists(CHECKSUM_FILE):
        with open(CHECKSUM_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 💾 Salvează noile checksumuri
def save_checksums(checksums):
    os.makedirs(os.path.dirname(CHECKSUM_FILE), exist_ok=True)
    with open(CHECKSUM_FILE, 'w', encoding='utf-8') as f:
        json.dump(checksums, f, indent=2)

# 🩺 Verifică integritatea actuală
def verify():
    print(f"\n🔐 VERIFICARE INTEGRITATE – {datetime.now()}")

    previous = load_previous()
    current = {}
    changed = []
    new_files = []
    missing = []

    for path in WATCHED_FILES:
        if not os.path.exists(path):
            missing.append(path)
            continue

        md5 = generate_md5(path)
        current[path] = md5

        if path not in previous:
            new_files.append(path)
        elif previous[path] != md5:
            changed.append(path)

    # 📊 Rezumat vizual
    if changed:
        print(f"\n⚠️ Fișiere modificate față de ultimul audit:")
        for c in changed:
            print(f"  - {c}")
    else:
        print("✅ Nicio modificare detectată în fișierele existente.")

    if new_files:
        print(f"\n🆕 Fișiere noi adăugate în listă de verificare:")
        for n in new_files:
            print(f"  - {n}")

    if missing:
        print(f"\n❌ Fișiere lipsă detectate:")
        for m in missing:
            print(f"  - {m}")

    # 💾 Actualizare referință pentru rulările următoare
    save_checksums(current)

    print("\n--------------------------------------")
    if not changed and not missing:
        print("🟢 Integritatea datelor este garantată. (Checksum OK)")
    else:
        print("🟠 Avertismente: Verificați fișierele listate mai sus.")
    print("--------------------------------------\n")


if __name__ == '__main__':
    verify()