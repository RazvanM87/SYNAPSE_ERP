import json
import hashlib
import os
from datetime import datetime

BLUEPRINT_FILE = 'master_blueprint.json'
INDEX_FILE = 'reports/qa/blueprint_index.json'
REPORT_FILE = 'reports/qa/daily_report.txt'
SNAPSHOT_FILE = 'reports/qa/snapshot_ai_context.json'

def get_blueprint_hash():
    if not os.path.exists(BLUEPRINT_FILE):
        return 'missing'
    with open(BLUEPRINT_FILE, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]

def get_index_hash():
    if not os.path.exists(INDEX_FILE):
        return None
    with open(INDEX_FILE, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]

def get_latest_report_info():
    if not os.path.exists(REPORT_FILE):
        return {'progress_score': 0, 'last_lines': ['No report yet']}
    with open(REPORT_FILE, 'r', encoding='utf-8') as r:
        lines = r.readlines()
    last_lines = [l.strip() for l in lines[-10:]]
    progress_line = next((l for l in reversed(lines) if 'Progres' in l), None)
    score = 0
    if progress_line:
        try:
            score = float(progress_line.split(':')[-1].replace('%', '').strip())
        except Exception:
            pass
    return {'progress_score': score, 'last_lines': last_lines}

def get_focused_features():
    if not os.path.exists(BLUEPRINT_FILE):
        return []
    with open(BLUEPRINT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    focused = []
    for wave in data['waves']:
        for module in wave['modules']:
            for func in module['functions']:
                if func['status'] in ['in_progress', 'skeleton']:
                    focused.append({'id': func['id'], 'module': module['name']})
    return focused

def create_snapshot():
    os.makedirs(os.path.dirname(SNAPSHOT_FILE), exist_ok=True)

    report_info = get_latest_report_info()
    focused = get_focused_features()
    blueprint_hash = get_blueprint_hash()
    index_hash = get_index_hash()
    active_layers = sorted(list(set(f['module'].split('.')[0].lower() for f in focused)))

    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'ai_context': {
            'focused_features': [f['id'] for f in focused],
            'layers_in_focus': active_layers,
            'progress_score': report_info['progress_score'],
            'blueprint_hash': blueprint_hash,
            'index_hash': index_hash,
            'notes': 'Snapshot automat după ultima rulare sync_blueprint.py',
            'last_report_extract': report_info['last_lines']
        }
    }

    with open(SNAPSHOT_FILE, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    print(f"🧠 Snapshot AI actual salvat → {SNAPSHOT_FILE}")
    print(f"📘 Funcționalități în focus: {len(focused)}  |  Layere: {', '.join(active_layers)}")
    print(f"📈 Progres curent: {report_info['progress_score']}% | 🔐 Hash Blueprint: {blueprint_hash}\n")

if __name__ == '__main__':
    create_snapshot()