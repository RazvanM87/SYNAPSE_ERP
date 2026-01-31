import os
import json
import re
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BLUEPRINT_FILE = 'master_blueprint.json'
SEARCH_DIRS = ['core', 'operational', 'frontend', 'ai', 'automations', 'bi', 'extensions']
REPORT_DIR = 'reports/qa'
REPORT_FILE = os.path.join(REPORT_DIR, 'qa_semantic_report.txt')

# 🔹 Vocabular cheie de business ERP / financiar-fiscal
BUSINESS_KEYWORDS = {
    'general': ['contabilitate', 'bilant', 'balanta', 'factura', 'client', 'plata', 'tva', 'reconciliere', 'salariu', 'impozit', 'd112', 'cashflow', 'cost', 'venit', 'cheltuiala', 'anexa', 'registru'],
    'finance': ['factura', 'banca', 'reconciliere', 'balanta', 'bilanț', 'cont'],
    'hr': ['angajat', 'contract', 'salariu', 'd112', 'impozit', 'CAS', 'CASS'],
    'ai': ['prediction', 'model', 'training', 'recommendation', 'learning', 'forecast'],
}

# 🔹 Funcție pentru vectorizare + scor de similaritate semantică simplă
def calc_similarity(text1, text2):
    if not text1 or not text2:
        return 0.0
    vec = TfidfVectorizer().fit([text1, text2])
    tfidf = vec.transform([text1, text2])
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(float(sim), 2)

# 🔹 Determină categoria business a unui ID ERP (heuristic)
def detect_category(fid):
    if fid.startswith('E3.FIN') or 'FIN' in fid:
        return 'finance'
    if 'HR' in fid:
        return 'hr'
    if 'AI' in fid:
        return 'ai'
    return 'general'

# 🔹 Extrage docstring‑urile și comentariile unui fișier
def extract_comments(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        # Comentarii și docstringuri multiline
        comments = re.findall(r'"""(.*?)"""', code, re.DOTALL)
        comments += re.findall(r"#\s*(?:[A-Za-z].*)", code)
        return " ".join(comments)
    except:
        return ''

# 🔹 Analiză semantică completă pentru fiecare funcționalitate
def perform_semantic_audit():
    if not os.path.exists(BLUEPRINT_FILE):
        print(f"⚠️ Nu s-a găsit {BLUEPRINT_FILE}. QA semantic oprit.")
        return

    with open(BLUEPRINT_FILE, 'r', encoding='utf-8') as f:
        blueprint = json.load(f)

    results = []
    for wave in blueprint['waves']:
        for module in wave['modules']:
            for func in module['functions']:
                fid = func['id']
                title = func['title']
                category = detect_category(fid)
                keyword_set = BUSINESS_KEYWORDS[category]

                # căutăm fișiere marcate @synapse-feature: fid
                doc_text = ''
                matched_files = []
                for d in SEARCH_DIRS:
                    for root, _, files in os.walk(d):
                        for f_name in files:
                            if f_name.endswith('.py'):
                                path = os.path.join(root, f_name)
                                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                                    code = f.read()
                                    if fid in code:
                                        matched_files.append(path)
                                        doc_text += extract_comments(path)

                # scor semnatic simplu (descriere ↔ comentarii)
                sim_score = calc_similarity(title.lower(), doc_text.lower())

                # scor business (procent de termeni fiscali/ERP găsiți în cod)
                found_terms = sum(1 for k in keyword_set if k.lower() in doc_text.lower())
                business_score = round((found_terms / max(1, len(keyword_set))) * 1.0, 2)

                # scor total (ponderat)
                total_score = round((sim_score * 0.6 + business_score * 0.4), 2)

                results.append({
                    'id': fid,
                    'title': title,
                    'category': category,
                    'similarity': sim_score,
                    'business_match': business_score,
                    'total': total_score,
                    'files': matched_files or ['N/A']
                })

    # 📄 Generează raportul text complet
    os.makedirs(REPORT_DIR, exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as r:
        r.write(f"===== QA SEMANTIC SYNAPSE ERP – {datetime.now()} =====\n\n")
        for item in results:
            status = '✅ OK' if item['total'] >= 0.8 else ('⚠️ Revizuire' if item['total'] >= 0.6 else '❌ Nealiniat')
            r.write(f"{item['id']} – {item['title']}\n")
            r.write(f"  Categorie: {item['category']}\n")
            r.write(f"  Semantica code/blueprint: {item['similarity']}\n")
            r.write(f"  Business match: {item['business_match']}\n")
            r.write(f"  Scor total: {item['total']} → {status}\n")
            r.write(f"  Fișiere asociate: {', '.join(item['files'])}\n")
            r.write("------------------------------------------\n")

    print(f"📘 Raport QA semantic salvat în: {REPORT_FILE}")

if __name__ == '__main__':
    perform_semantic_audit()