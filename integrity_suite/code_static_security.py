import os

# 🔹 Patternuri interzise în cod (instruțiuni potențial periculoase)
FORBIDDEN = [
    'eval(', 'exec(', 'os.system', 'subprocess.Popen', 'open("/etc/', 'pickle.load'
]

# 🔹 Excluderi — directoare și fișiere care nu trebuie verificate
EXCLUDED_PATHS = ['integrity_suite']  # nu scana propriile scripturi
EXCLUDED_FILE_PATTERNS = ['test_', '_mock']  # ignoră fișiere de test

def scan_code():
    report = ["=== Static Code Security Check ==="]
    issues = []

    for root, _, files in os.walk('.'):
        # Ignoră directoarele excluse (audit, QA etc.)
        if any(excl in root for excl in EXCLUDED_PATHS):
            continue

        for f in files:
            if not f.endswith('.py'):
                continue

            # Ignoră fișierele de test (ex: test_auth.py, user_mock.py)
            if any(pattern in f for pattern in EXCLUDED_FILE_PATTERNS):
                continue

            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as code:
                    text = code.read()
                    for pattern in FORBIDDEN:
                        if pattern in text:
                            issues.append(f'{pattern} → {path}')
            except Exception as e:
                issues.append(f'⚠️ Eroare la {path}: {e}')

    if issues:
        report.append('🚨 Probleme detectate:')
        report += [' - ' + i for i in issues]
    else:
        report.append('✅ Cod curat — fără vulnerabilități sau instrucțiuni riscante.')

    return '\n'.join(report)

if __name__ == '__main__':
    print(scan_code())