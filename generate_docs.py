import os

OUTPUT_FILE = 'PROJECT_STRUCTURE.md'
TARGET_DIRS = ['core', 'operational', 'ai', 'bi', 'tests']

def generate_docs():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        out.write('# 📘 SYNAPSE ERP – Documentație structură proiect\n\n')
        for d in TARGET_DIRS:
            out.write(f'## {d.capitalize()}\n')
            for root, _, files in os.walk(d):
                level = root.replace(d, '').count(os.sep)
                indent = '  ' * level
                out.write(f'{indent}- **{root}/**\n')
                for f in files:
                    out.write(f'{indent}    - {f}\n')
            out.write('\n')
    print(f'📄 Documentație generată → {OUTPUT_FILE}')

if __name__ == '__main__':
    generate_docs()