import os
import zipfile
from datetime import datetime

# 🔹 Fișierele cheie care trebuie transmise zilnic
FILES_TO_PACKAGE = [
    'master_blueprint.json',
    'reports/qa/daily_report.txt',
    'reports/qa/snapshot_ai_context.json',
    'reports/qa/blueprint_index.json',
    'reports/qa/qa_semantic_report.txt'   # 🆕 nou inclus în pachetul ZIP
]

OUTPUT_DIR = 'reports/qa/packages'

def create_snapshot_package():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_name = os.path.join(OUTPUT_DIR, f'synapse_snapshot_{timestamp}.zip')

    missing_files = []
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in FILES_TO_PACKAGE:
            if os.path.exists(file):
                arcname = os.path.join('snapshot', os.path.basename(file))
                zipf.write(file, arcname=arcname)
                print(f"📄 Adăugat în pachet: {file}")
            else:
                missing_files.append(file)

    print("\n--------------------------------------")
    if missing_files:
        print("⚠️ Avertisment: următoarele fișiere lipsesc și NU au fost incluse:")
        for m in missing_files:
            print(f"  - {m}")
    else:
        print("✅ Toate fișierele necesare au fost incluse în pachetul ZIP.")

    print(f"📦 Pachet creat cu succes → {zip_name}")
    print("--------------------------------------\n")

if __name__ == '__main__':
    create_snapshot_package()