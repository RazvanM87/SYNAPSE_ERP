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

BUSINESS_KEYWORDS = {
    'general': ['factură', 'client', 'TVA', 'cost', 'document', 'raport', 'configurație'],
    'finance': ['bilanț', 'balanță', 'bancă', 'factură', 'cont', 'cashflow', 'SAF-T'],
    'hr': ['salariu', 'angajat', 'pontaj', 'deducere', 'CASS', 'contract'],
    'ai': ['model', 'forecast', 'training', 'prediction', 'anomaly'],
    'bi': ['raport', 'dashboard', 'KPI', 'metric', 'alertă'],
    'automation': ['cron', 'workflow', 'task', 'trigger']
}

def calc_similarity(t1, t2):
    if not t1 or not t2: return 0.0
    vec = TfidfVectorizer().fit([t1, t2])
    tfidf = vec.transform([t1, t2])
    return round(float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]), 2)

def detect_category(fid):
    key_map = {'FIN': 'finance', 'HR': 'hr', 'AI': 'ai', 'BI': 'bi', 'WORK': 'automation'}
    for key, cat in key_map.items():
        if key in fid: return cat
    return 'general'

pattern_comments = re.compile(r'(""".*?"""|#.*)', re.DOTALL)

def perform_semantic_audit():
    if not os.path.exists(BLUEPRINT_FILE):
        print(f'⚠️ {BLUEPRINT_FILE} lipsește. QA semantic oprit.')
        return

    with open(BLUEPRINT_FILE, 'r', encoding='utf-8') as f:
        blueprint = json.load(f)

    results = []
    for wave in blueprint['waves']:
        for module in wave['modules']:
            for func in module['functions']:
                fid, title = func['id'], func['title']
                category = detect_category(fid)
                keywords = BUSINESS_KEYWORDS.get(category, [])

                matched_files, comments = [], ''
                for d in SEARCH_DIRS:
                    for root, _, files in os.walk(d):
                        for name in files:
                            if name.endswith('.py'):
                                path = os.path.join(root, name)
                                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                                    text = f.read()
                                    if fid in text:
                                        matched_files.append(path)
                                        comments += ' '.join(pattern_comments.findall(text))

                sim_score = calc_similarity(title.lower(), comments.lower())
                business_score = sum(1 for k in keywords if k.lower() in comments.lower()) / max(1, len(keywords))
                total_score = round((sim_score * 0.4 + business_score * 0.6), 2)

                results.append({
                    'id': fid,
                    'category': category,
                    'title': title,
                    'similarity': sim_score,
                    'business_match': round(business_score, 2),
                    'total': total_score,
                    'files': matched_files or ['N/A']
                })

    os.makedirs(REPORT_DIR, exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as r:
        r.write(f"===== QA SEMANTIC SYNAPSE ERP {datetime.now()} =====\n")
        for item in results:
            status = '✅ OK' if item['total'] >= 0.8 else ('⚠️ Revizuire' if item['total'] >= 0.6 else '❌ Nealiniat')
            r.write(f"{item['id']} – {item['title']}\nCategorie: {item['category']}\nTotal: {item['total']} {status}\nFișiere: {', '.join(item['files'])}\n--------------------------------\n")
    print(f"📘 Raport QA semantic salvat → {REPORT_FILE}")

if __name__ == '__main__':
    perform_semantic_audit()