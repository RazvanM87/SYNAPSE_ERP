import os, json, datetime, subprocess

def run_code_analysis():
    print('\n🧠  Rulare Analyze Code…')
    script = 'analyze_code.py'
    if os.path.exists(script): subprocess.run(['python',script],check=False)

EXPECTED_STRUCTURE = {
    'core': ['auth','config','validation','theming','notifications'],
    'operational': ['clients','suppliers','products','sales','purchases','invoices','payments','warehouse','accounting','costing','hr'],
    'automations': ['flows','triggers','qa'],
    'ai': ['learning','predictions','pricing','reconciliation','context_engine'],
    'extensions': ['connectors','docs','multisite'],
    'bi': ['dashboard','reports'],
    'frontend': ['ui','search','help_center'],
    'reports': ['unit','integration','qa']
}

def check_structure(base_path='.'):
    print('\n🔍 Verificare structură…')
    issues = []
    for folder, subs in EXPECTED_STRUCTURE.items():
        path = os.path.join(base_path, folder)
        if not os.path.exists(path):
            issues.append(f'❌ Lipsește: {folder}')
        elif subs:
            for s in subs:
                sp=os.path.join(path,s)
                if not os.path.exists(sp):
                    issues.append(f'⚠️ Subfolder lipsă: {folder}/{s}')
    if issues:
        [print(i) for i in issues]
        print('\n⚠️ Structura are abateri!')
    else:
        print('✅ Structura completă SYNAPSE ERP 2026 validă.')

def analyze_blueprint():
    if not os.path.exists('master_blueprint.json'):
        print('⚠️ Lipsă master_blueprint.json'); return
    data=json.load(open('master_blueprint.json','r',encoding='utf-8'))
    stats={'done':0,'in_progress':0,'skeleton':0,'not_started':0,'total':0}
    for w in data['waves']:
        for m in w['modules']:
            for f in m['functions']:
                s=f.get('status','not_started')
                stats['total']+=1; stats[s]+=1
    score=(stats['done']+stats['in_progress']*0.6+stats['skeleton']*0.3)/max(stats['total'],1)*100
    print('\n📊 PROGRES SYNAPSE ERP (Structură actuală)')
    for k,v in stats.items(): print(f'{k:<15}: {v}')
    print('------------------------------------')
    print(f'📈 Progres ponderat: {score:.1f}%\n⏱ {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n')

def main():
    run_code_analysis()
    check_structure()
    analyze_blueprint()

if __name__=='__main__': main()