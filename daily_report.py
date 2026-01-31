import json
import datetime
import os

BLUEPRINT_FILE = 'master_blueprint.json'
REPORT_DIR = 'reports/qa'
REPORT_PATH = os.path.join(REPORT_DIR, 'daily_report.txt')

# 🔹 Încărcare blueprint actual
def load_blueprint():
    if not os.path.exists(BLUEPRINT_FILE):
        print(f"⚠️ Fișierul {BLUEPRINT_FILE} nu există!")
        return None
    with open(BLUEPRINT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# 🔹 Analizează blueprintul și calculează progresul logic ponderat
def analyze_progress(data):
    stats = {"done": 0, "in_progress": 0, "skeleton": 0, "not_started": 0, "total": 0}

    for wave in data['waves']:
        for module in wave['modules']:
            for func in module['functions']:
                stats['total'] += 1
                status = func.get('status', 'not_started')
                if status not in stats:
                    stats[status] = 0
                stats[status] += 1

    # Calcul ponderat (done = 1.0, in_progress = 0.6, skeleton = 0.3)
    score = (stats['done'] + stats['in_progress'] * 0.6 + stats['skeleton'] * 0.3) / stats['total'] * 100

    return stats, round(score, 1)

# 🔹 Generează raport zilnic text

def generate_report():
    data = load_blueprint()
    if not data:
        return

    stats, score = analyze_progress(data)

    os.makedirs(REPORT_DIR, exist_ok=True)

    with open(REPORT_PATH, 'a', encoding='utf-8') as r:
        r.write(f"===== RAPORT ZILNIC SYNAPSE ERP =====\n")
        r.write(f"Data: {datetime.datetime.now()}\n")
        r.write(f"Total funcționalități: {stats['total']}\n")
        r.write(f"✔️  Terminate (done): {stats['done']}\n")
        r.write(f"⚙️  În curs (in_progress): {stats['in_progress']}\n")
        r.write(f"🧩  Schelet logic (skeleton): {stats['skeleton']}\n")
        r.write(f"❌  Lipsă (not_started): {stats['not_started']}\n")
        r.write(f"------------------------------------\n")
        r.write(f"📈  Progres ponderat logic: {score}%\n")
        r.write("====================================\n\n")

    print(f"📄 Raport zilnic salvat în: {REPORT_PATH}")
    print(f"📊 Progres global logic: {score}%")

# 🔹 Execuție principală
if __name__ == '__main__':
    generate_report()