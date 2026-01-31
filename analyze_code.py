import os
import json
import re
import io
from datetime import datetime

BLUEPRINT_FILE = 'master_blueprint.json'
SEARCH_DIRS = ['core', 'operational', 'ai', 'bi', 'automations', 'extensions', 'frontend']

# 🔹 Analiza logică pentru fișiere Python
FUNC_PATTERN = re.compile(r'def\s+[a-zA-Z_]+\s*\(')
CLASS_PATTERN = re.compile(r'class\s+[A-Z][a-zA-Z_]+')
COMMENT_PATTERN = re.compile(r'#\s*[A-Za-z]')
IMPORT_PATTERN = re.compile(r'^import\s+|^from\s+[a-zA-Z_]')


def evaluate_code_quality(files):
    """Evaluează completitudinea logică a fișierelor unui modul."""
    score = 0
    for path in files:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                code = f.read()
            lines = code.splitlines()

            func_count = len(FUNC_PATTERN.findall(code))
            class_count = len(CLASS_PATTERN.findall(code))
            comments = len(COMMENT_PATTERN.findall(code))
            imports = len(IMPORT_PATTERN.findall(code))
            length = len(lines)

            # Scor logic de 0–5 per fișier
            local_score = 0
            if func_count >= 2: local_score += 1
            if class_count >= 1: local_score += 1
            if comments >= 5: local_score += 1
            if imports >= 5 or length > 50: local_score += 1
            if not code.strip().endswith(':'):  # evită erori de sintaxă triviale
                local_score += 1

            score = max(score, local_score)  # Folosește cel mai mare scor între fișierele modulului
        except Exception as e:
            print(f"⚠️ Eroare la analiza fișierului {path}: {e}")
            continue
    return score


# 🔍 Extrage toate funcționalitățile detectate în cod (prin marker)
def extract_code_features():
    features = {}
    pattern = re.compile(r'@synapse-feature:\s*([A-Z0-9_.-]+)')
    for d in SEARCH_DIRS:
        for root, _, files in os.walk(d):
            for f in files:
                if f.endswith('.py'):
                    path = os.path.join(root, f)
                    with open(path, 'r', encoding='utf-8') as code:
                        text = code.read()
                        found = pattern.findall(text)
                        for fid in found:
                            features.setdefault(fid, []).append(path)
    return features


# 🧩 Analizează și actualizează Blueprintul complet (+ scoruri logice)
def analyze_and_update():
    if not os.path.exists(BLUEPRINT_FILE):
        print("⚠️ Fișierul master_blueprint.json nu există. Analiza oprită.")
        return

    with open(BLUEPRINT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    code_features = extract_code_features()
    all_ids = []
    logic_summary = {"done": 0, "in_progress": 0, "skeleton": 0, "missing": 0}

    for wave in data['waves']:
        for module in wave['modules']:
            for func in module['functions']:
                fid = func['id']
                all_ids.append(fid)

                if fid in code_features:
                    score = evaluate_code_quality(code_features[fid])

                    if score >= 5:
                        func['status'] = 'done'
                        logic_summary["done"] += 1
                    elif 3 <= score < 5:
                        func['status'] = 'in_progress'
                        logic_summary["in_progress"] += 1
                    elif 1 <= score < 3:
                        func['status'] = 'skeleton'
                        logic_summary["skeleton"] += 1
                    else:
                        func['status'] = 'not_started'
                        logic_summary["missing"] += 1
                else:
                    func['status'] = 'not_started'
                    logic_summary["missing"] += 1

    extras = [fid for fid in code_features if fid not in all_ids]

    # 💾 Backup sigur (înainte de scriere)
    backup_file = 'master_blueprint.bak'
    if os.path.exists(BLUEPRINT_FILE):
        os.replace(BLUEPRINT_FILE, backup_file)
        print(f'💾 Backup creat: {backup_file}')

    # 🧱 Scriere sigură (end-of-line controlate)
    with io.open(BLUEPRINT_FILE, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

    # 🧾 Raportare completă
    print("\n🧠 Analiză logică completă ↔ Blueprint actualizat")
    print(f"📘 Funcționalități definite în JSON: {len(all_ids)}")
    print(f"📂 Module analizate: {len(code_features)}")

    if extras:
        print("⚠️ Funcționalități neautorizate detectate în cod:")
        for e in extras:
            print(f"  - {e}")
    else:
        print("✅ Nicio funcționalitate neautorizată detectată.")

    print("\n📊 Rezumat logic:")
    for k, v in logic_summary.items():
        print(f"  {k.capitalize():<12}: {v}")

    total = len(all_ids)
    done = logic_summary['done']
    prog = logic_summary['in_progress']
    skeleton = logic_summary['skeleton']

    progress_score = (done + prog * 0.6 + skeleton * 0.3) / total * 100
    print(f"\n📈 Progres ponderat logic: {progress_score:.1f}%")
    print(f"📄 Blueprint actualizat automat la: {datetime.now()}\n")


if __name__ == '__main__':
    analyze_and_update()