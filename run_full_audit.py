import subprocess
import datetime
import os

# 🔹 Ordinea de rulare a verificărilor
PIPELINE = [
    ('Pre‑Setup', 'pre_feature_setup.py --fix'),
    ('Analyze Code', 'analyze_code.py'),
    ('Generate Index', 'generate_index.py'),
    ('QA Semantic', 'qa_semantic.py'),
    ('Audit Integrity', 'audit_integrity.py'),
    ('Daily Report', 'daily_report.py'),
    ('Snapshot AI Context', 'snapshot_ai_context.py'),
    ('Verify Checksum', 'verify_checksum.py'),
    ('Package Snapshot', 'snapshot_packager.py')
]

LOG_FILE = 'reports/qa/full_audit_log.txt'

def run_stage(name, command):
    start_time = datetime.datetime.now()
    print(f"\n🧩 {name} → {command}")

    # Separate command & params safely (e.g., for --fix)
    parts = ['python'] + command.split()

    # Check main file exists (ignore parameters)
    base_script = command.split()[0]
    if not os.path.exists(base_script):
        print(f"⚠️ Fisierul {base_script} lipseste — etapa omisă.")
        return {'stage': name, 'status': 'skipped', 'duration': 0}

    try:
        subprocess.run(parts, check=False)
        status = 'done'
    except Exception as e:
        print(f"❌ Eroare la rularea {base_script}: {e}")
        status = 'error'

    duration = (datetime.datetime.now() - start_time).seconds
    return {'stage': name, 'status': status, 'duration': duration}

def generate_summary(results):
    ok = sum(1 for r in results if r['status'] == 'done')
    skipped = sum(1 for r in results if r['status'] == 'skipped')
    errors = sum(1 for r in results if r['status'] == 'error')

    print('\n============================================')
    print(f"🧾  Raport final SYNAPSE ERP FULL AUDIT — {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f' Etape finalizate: {ok}, Ocolite: {skipped}, Erori: {errors}')
    print(' Detalii:')
    for r in results:
        print(f"  - {r['stage']:<20} {r['status']:<10} ({r['duration']}s)")
    print('============================================\n')

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as log:
        log.write(f"===== SYNAPSE ERP FULL AUDIT {datetime.datetime.now()} =====\n")
        for r in results:
            log.write(f"{r['stage']:<20} {r['status']:<10} ({r['duration']}s)\n")
        log.write('\n\n')

def main():
    print(f"\n🚀 PORNIRE AUDIT COMPLET SYNAPSE ERP {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n")
    results = []
    for name, script in PIPELINE:
        results.append(run_stage(name, script))
    generate_summary(results)
    print('🏁 Proces complet finalizat. Verificați `reports/qa` pentru toate rapoartele.')

if __name__ == '__main__':
    main()