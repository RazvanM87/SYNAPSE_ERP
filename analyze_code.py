import os
import json
import re
import io
from datetime import datetime

BLUEPRINT_FILE = 'master_blueprint.json'
SEARCH_DIRS = ['core', 'operational', 'ai', 'bi', 'automations', 'extensions', 'frontend']
FUNC_PATTERN = re.compile(r'def\s+[A-Za-z_]+\s*\(')
CLASS_PATTERN = re.compile(r'class\s+[A-Za-z_]+')
COMMENT_PATTERN = re.compile(r'#\s*[A-Za-z]')
IMPORT_PATTERN = re.compile(r'^(?:from|import)\s+[A-Za-z_]', re.MULTILINE)

LAYER_WEIGHTS = {
    'core': 1.0, 'operational': 1.2, 'ai': 1.5, 'bi': 1.1,
    'automations': 1.3, 'extensions': 1.0, 'frontend': 0.8
}

def evaluate_code_quality(files):
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

            local_score = sum([
                func_count >= 2,
                class_count >= 1,
                comments >= 5,
                imports >= 3,
                length > 40
            ])
            score = max(score, local_score)
        except Exception as e:
            print(f"⚠️ Eroare la analiza {path}: {e}")
    return score

def extract_code_features():
    features = {}
    pattern = re.compile(r'@synapse-feature:\s*([A-Z0-9_.-]+)')
    for d in SEARCH_DIRS:
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith('.py'):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8', errors='ignore') as code:
                        text = code.read()
                        found = pattern.findall(text)
                        for fid in found:
                            features.setdefault(fid, []).append(path)
    return features

def analyze_and_update():
    if not os.path.exists(BLUEPRINT_FILE):
        print('⚠️ master_blueprint.json lipsește.')
        return

    with open(BLUEPRINT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    code_features = extract_code_features()
    logic_summary = {k: 0 for k in ['done', 'in_progress', 'skeleton', 'not_started']}

    for wave in data['waves']:
        for module in wave['modules']:
            for func in module['functions']:
                fid = func['id']
                if fid in code_features:
                    score = evaluate_code_quality(code_features[fid])
                    if score == 5:
                        func['status'] = 'done'
                        logic_summary['done'] += 1
                    elif score == 4:
                        func['status'] = 'in_progress'
                        logic_summary['in_progress'] += 1
                    elif score == 3:
                        func['status'] = 'partial'
                        logic_summary['skeleton'] += 1
                    else:
                        func['status'] = 'skeleton'
                        logic_summary['skeleton'] += 1
                else:
                    func['status'] = 'not_started'
                    logic_summary['not_started'] += 1

    backup_file = 'master_blueprint.bak'
    if os.path.exists(BLUEPRINT_FILE):
        os.replace(BLUEPRINT_FILE, backup_file)
        print(f'💾 Backup creat: {backup_file}')

    with io.open(BLUEPRINT_FILE, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

    total = sum(logic_summary.values())
    done = logic_summary['done']
    prog = logic_summary['in_progress']
    skeleton = logic_summary['skeleton']
    progress_score = (done + prog * 0.3 + skeleton * 0.05) / total * 100

    print(f"\n📈 Progres logic total: {progress_score:.1f}%  | Total funcții: {total}")

if __name__ == '__main__':
    analyze_and_update()