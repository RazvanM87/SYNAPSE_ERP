import os
import subprocess
import json
import sys
from datetime import datetime

def section(title):
    print(f"\n{'='*60}\n🧱 {title}\n{'='*60}")

def check_file(path, critical=False, autofix=False):
    if os.path.exists(path):
        print(f"✅ {path}")
        return True
    else:
        status = "❌" if critical else "⚠️"
        print(f"{status} {path} – lipsește")
        if autofix:
            if path.endswith('/') or path.endswith('\\'):
                os.makedirs(path, exist_ok=True)
                print(f"   🔧 Creat folder: {path}")
            else:
                open(path, 'w', encoding='utf-8').write('')
                print(f"   🧩 Creat fișier gol: {path}")
        return False

def check_command(cmd, label):
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"✅ {label} funcționează")
        return True
    except Exception:
        print(f"⚠️ {label} nu este disponibil")
        return False

def create_env_examples():
    example = """# SYNAPSE ERP Environment Example
DB_URL=postgresql://user:password@localhost:5432/synapse
JWT_SECRET=CHANGE_ME
LOG_LEVEL=INFO
"""
    for env_name in ['.env.dev', '.env.qa', '.env.prod']:
        if not os.path.exists(env_name):
            with open(env_name, 'w', encoding='utf-8') as f:
                f.write(example)
                print(f"   🔧 Creat fișier config: {env_name}")

def pre_feature_checklist(autofix=False):
    print(f"\n🚀 PORNIRE CHECKLIST SYNAPSE ERP – {datetime.now():%Y-%m-%d %H:%M:%S}\n")
    results = {}

    # 1️⃣ Structură esențială
    section("STRUCTURĂ DE BAZĂ")
    core_files = [
        'master_blueprint.json',
        'run_full_audit.py',
        'snapshot_packager.py',
        'sync_blueprint.py'
    ]
    results['structure'] = all(check_file(f, True, autofix) for f in core_files)

    # 2️⃣ QA / CI/CD pregătire
    section("QA && CI/CD")
    qa_tools = [
        'analyze_code.py',
        'generate_index.py',
        'qa_semantic.py',
        'audit_integrity.py',
        'verify_checksum.py'
    ]
    results['qa'] = all(check_file(f, False, autofix) for f in qa_tools)
    check_command(['git', '--version'], 'Git')
    check_command(['pytest', '--version'], 'Pytest')

    # 3️⃣ AI & ML layer
    section("AI LAYER")
    ai_paths = [
        'ai/learning/',
        'ai/context_engine/',
        'ai/predictions/'
    ]
    for p in ai_paths:
        ok = os.path.exists(p)
        print(f"{'✅' if ok else '⚠️'} {p}")
        if not ok and autofix:
            os.makedirs(p, exist_ok=True)
            print(f"   🔧 Creat folder AI: {p}")
    results['ai'] = all(os.path.exists(p) for p in ai_paths)

    # 4️⃣ Documentație
    section("DOCUMENTAȚIE & BLUEPRINT")
    results['docs'] = all(check_file(p, False, autofix) for p in [
        'extensions/docs/documentation_service.py',
        'docs/'
    ])

    if os.path.exists('docs/'):
        print("📘 Documentația există – completare ReDoc/Sphinx recomandată.")

    # 5️⃣ Medii și .env
    section("MEDII DE EXECUȚIE")
    env_files = [p for p in os.listdir('.') if p.startswith('.env')]
    if env_files:
        print(f"✅ Fişiere .env detectate: {', '.join(env_files)}")
        results['env'] = True
    else:
        print("⚠️ Nu există fişiere .env – se pot crea automate...")
        if autofix:
            create_env_examples()
        results['env'] = autofix

    # 6️⃣ Rezumat final
    section("REZUMAT FINAL")
    all_ok = all(results.values())
    for key, val in results.items():
        print(f"{key:<12}: {'✅' if val else '⚠️'}")

    print("\n------------------------------------------")
    if all_ok:
        print("🟢 Sistem pregătit complet: poți începe dezvoltarea funcționalităților.")
    else:
        print("🟠 Unele componente lipsesc — rulează scriptul cu --fix sau adaugă manual.")
    print("------------------------------------------\n")

if __name__ == '__main__':
    autofix = '--fix' in sys.argv
    pre_feature_checklist(autofix)