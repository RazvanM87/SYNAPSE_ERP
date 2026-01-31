import subprocess, datetime, os

SCRIPTS = [
    'structural_integrity.py',
    'code_static_security.py',
    'feature_integrity.py',
    'dependency_check.py'
]

def run_script(script):
    result = subprocess.run(['python', f'integrity_suite/{script}'], capture_output=True, text=True)
    section = f"\n=== {script} ===\n" + result.stdout + result.stderr
    return section

if __name__ == '__main__':
    print('\n=== SYNAPSE ERP – Code Integrity Suite ===\n')
    output_log = [run_script(s) for s in SCRIPTS]

    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    txt_path = f'integrity_suite/report_integrity_{now}.txt'
    html_path = f'integrity_suite/report_integrity_{now}.html'

    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_log))

    html = ['<html><head><title>Integrity Report</title><style>',
            'body{font-family:monospace;background:#1e1e1e;color:#c7c7c7;white-space:pre;}',
            'h2{color:#58a6ff;}', '</style></head><body>']

    for section in output_log:
        title = section.splitlines()[0] if section.splitlines() else 'Section'
        content = os.linesep.join(section.splitlines()[1:])
        html.append(f'<h2>{title}</h2><pre>{content}</pre><hr>')

    html.append('</body></html>')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))

    print(f'\n🏁 Verificare completă. Rapoarte generate:\n - {txt_path}\n - {html_path}')