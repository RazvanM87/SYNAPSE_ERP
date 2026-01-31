import json, os, re

BP_FILE = 'master_blueprint.json'
pattern = re.compile(r'@synapse-feature:\s*([A-Z0-9_.-]+)')

def verify_features():
    report = ["=== Feature Integrity Check ==="]
    declared_ids = []

    try:
        with open(BP_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for wave in data.get('waves', []):
                for module in wave.get('modules', []):
                    for func in module.get('functions', []):
                        declared_ids.append(func['id'])
    except FileNotFoundError:
        report.append('⚠️ Blueprintul nu a fost găsit.')

    found_ids = {}
    for root, _, files in os.walk('.'):
        for f in files:
            if f.endswith('.py'):
                text = open(os.path.join(root, f), encoding='utf-8', errors='ignore').read()
                found = pattern.findall(text)
                for fid in found:
                    if fid in found_ids:
                        report.append(f'⚠️ Duplicate feature ID: {fid} → {f} și {found_ids[fid]}')
                    found_ids[fid] = f

    declared_count = len(declared_ids)
    found_count = len(found_ids)
    missing = [fid for fid in declared_ids if fid not in found_ids]

    report.append(f'✅ Găsite în cod: {found_count} / Declarate în blueprint: {declared_count}')
    if missing:
        report.append(f'❌ Lipsă: {len(missing)} funcționalități neimplementate')
        report += ['   - ' + m for m in missing[:10]]
    else:
        report.append('✅ Toate funcționalitățile din blueprint sunt reprezentate în cod.')

    return '\n'.join(report)

if __name__ == '__main__':
    print(verify_features())