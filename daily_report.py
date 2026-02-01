import json, os, datetime

BLUEPRINT_FILE = 'master_blueprint.json'
REPORT_DIR = 'reports/qa'
REPORT_PATH = os.path.join(REPORT_DIR,'daily_report.txt')

def load_blueprint():
    if not os.path.exists(BLUEPRINT_FILE):
        print(f'⚠️ Fișierul {BLUEPRINT_FILE} nu există.'); return None
    return json.load(open(BLUEPRINT_FILE,'r',encoding='utf-8'))

def analyze_progress(data):
    stats={k:0 for k in ['done','in_progress','skeleton','not_started','total']}
    for w in data['waves']:
        for m in w['modules']:
            for f in m['functions']:
                s=f.get('status','not_started')
                stats['total']+=1
                stats[s]+=1
    score=(stats['done']+stats['in_progress']*0.6+stats['skeleton']*0.3)/max(stats['total'],1)*100
    return stats, round(score,1)

def generate_report():
    data=load_blueprint();
    if not data: return
    stats,score=analyze_progress(data)
    os.makedirs(REPORT_DIR, exist_ok=True)

    with open(REPORT_PATH,'a',encoding='utf-8') as r:
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        r.write('===== RAPORT ZILNIC SYNAPSE ERP =====\n')
        r.write(f'Data: {now}\n')
        for k,v in stats.items():
            if k!='total': r.write(f'{k:<15}: {v}\n')
        r.write('------------------------------------\n')
        r.write(f'📈 Progres ponderat: {score}%\n====================================\n\n')

    print(f'📄 Raport generat: {REPORT_PATH}\n📊 Progres global: {score}%')

if __name__=='__main__':
    generate_report()