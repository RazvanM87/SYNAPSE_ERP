import os, datetime

HEADER_TEMPLATE = 'header_template.txt'
TARGET_DIRS = ['core', 'operational', 'ai', 'bi', 'tests']


def apply_headers():
    with open(HEADER_TEMPLATE, 'r') as f:
        header = f.read()

    for folder in TARGET_DIRS:
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(('.py', '.ts', '.js')):
                    path = os.path.join(root, file)
                    with open(path, 'r+', encoding='utf-8') as current:
                        content = current.read()
                        if 'SYNAPSE ERP – File Header' not in content:
                            current.seek(0)
                            current.write(header.format(
                                filename=file,
                                module=root.replace('\\', '/'),
                                date=datetime.datetime.now()
                            ) + '\n' + content)
                            print(f'🧾 Antet adăugat: {path}')

def main():
    apply_headers()

if __name__ == '__main__':
    main()