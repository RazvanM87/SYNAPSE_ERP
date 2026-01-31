import os
import json
import datetime
import subprocess

# 1️⃣ Rulează automat analiza codului

def run_code_analysis():
    print("\n🧠 Rulare automată Analyze Code…")
    script = 'analyze_code.py'
    if os.path.exists(script):
        try:
            subprocess.run(['python', script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Eroare la rularea {script}: {e}")
    else:
        print("⚠️ Fișierul analyze_code.py nu a fost găsit. Se continuă fără analiza logică.")

# 2️⃣ Structura completă conform SYNAPSE ERP Blueprint
EXPECTED_STRUCTURE = {
    'core': ['auth', 'config', 'validation', 'theming'],
    'operational': ['clients', 'suppliers', 'products', 'invoices', 'payments', 'hr'],
    'frontend': ['ui', 'search', 'help_center'],
    'ai': ['predictions', 'pricing', 'reconciliation', 'learning'],
    'automations': ['flows', 'qa'],
    'bi': ['dashboard', 'reports'],
    'extensions': ['connectors', 'multisite', 'docs'],
    'tests': ['core', 'operational', 'frontend', 'ai', 'bi'],
    'reports': ['unit', 'integration', 'qa'],
    'master_blueprint.json': None,
    'sync_blueprint.py': None,
    'generate_structure.py': None,
    'daily_report.py': None,
    'analyze_code.py': None,
    'apply_headers.py': None,
    'generate_docs.py': None,
    'header_template.txt': None,
    'PROJECT_STRUCTURE.md': None
}

# 3️⃣ Verificarea structurii complete
def check_structure(base_path="."):
    print("\n🔍 Verificare structură…")
    issues = []

    for expected in EXPECTED_STRUCTURE:
        path = os.path.join(base_path, expected)
        if not os.path.exists(path):
            issues.append(f"❌ Lipsește: {expected}")
        elif EXPECTED_STRUCTURE[expected]:
            for sub in EXPECTED_STRUCTURE[expected]:
                subpath = os.path.join(path, sub)
                if not os.path.exists(subpath):
                    issues.append(f"⚠️ Subfolder lipsă: {expected}/{sub}")

    extra = [f for f in os.listdir(base_path) if f not in EXPECTED_STRUCTURE]
    for ex in extra:
        if os.path.isdir(ex) and ex not in EXPECTED_STRUCTURE:
            issues.append(f"🚫 Element neprevăzut detectat: {ex}")

    if issues:
        print("\n".join(issues))
        print("\n⚠️ Structura proiectului are abateri!")
    else:
        print("✅ Structura este intactă.")

# 4️⃣ Analiză blueprint + progres logic defalcat
def analyze_blueprint():
    if not os.path.exists('master_blueprint.json'):
        print("⚠️ Fișierul master_blueprint.json nu a fost găsit.")
        return

    with open('master_blueprint.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    stats = {"done": 0, "in_progress": 0, "skeleton": 0, "not_started": 0, "total": 0}

    for wave in data['waves']:
        for module in wave['modules']:
            for func in module['functions']:
                stats['total'] += 1
                status = func.get('status', 'not_started')
                if status not in stats:
                    stats[status] = 0
                stats[status] += 1

    # 🧮 Calcul progres ponderat
    score = (stats['done'] + stats['in_progress'] * 0.6 + stats['skeleton'] * 0.3) / stats['total'] * 100

    print("\n📊 Raport SYNAPSE ERP – Progres logic combinat:")
    print(f"Funcționalități totale: {stats['total']}")
    print(f"✔️  Gata (done): {stats['done']}")
    print(f"⚙️  În curs (in_progress): {stats['in_progress']}")
    print(f"🧩  Schelet logic (skeleton): {stats['skeleton']}")
    print(f"❌  Lipsă (not_started): {stats['not_started']}")
    print(f"------------------------------------")
    print(f"📈  Progres ponderat logic: {score:.1f}%")
    print(f"\nTimp execuție: {datetime.datetime.now()}\n")

# 5️⃣ Flux principal
def main():
    run_code_analysis()
    check_structure()
    analyze_blueprint()

if __name__ == '__main__':
    main()