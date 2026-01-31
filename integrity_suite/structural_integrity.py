import os

REQUIRED_DIRS = [
    'core', 'operational', 'ai', 'frontend', 'automations', 'bi', 'extensions'
]
REQUIRED_FILES = ['master_blueprint.json']

def check_structure():
    report = ["=== Structural Integrity Check ==="]
    missing_dirs = [d for d in REQUIRED_DIRS if not os.path.isdir(d)]
    missing_files = [f for f in REQUIRED_FILES if not os.path.isfile(f)]

    if not missing_dirs and not missing_files:
        report.append('✅ Structura ERP este completă.')
    else:
        if missing_dirs:
            report.append(f'⚠️ Foldere lipsă: {", ".join(missing_dirs)}')
        if missing_files:
            report.append(f'⚠️ Fișiere lipsă: {", ".join(missing_files)}')
    return '\n'.join(report)

if __name__ == '__main__':
    print(check_structure())