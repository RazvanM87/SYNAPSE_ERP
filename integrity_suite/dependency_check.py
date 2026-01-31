import os, ast

def check_import_cycles():
    report = ["=== Dependency Check ==="]
    imports = {}

    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                module = path.replace(os.sep, '.')[:-3]
                try:
                    tree = ast.parse(open(path, 'r', encoding='utf-8').read())
                    imp = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module]
                    imports[module] = imp
                except SyntaxError as e:
                    report.append(f'⚠️ Syntax error în {path}: {e}')

    for mod, deps in imports.items():
        for dep in deps:
            if dep in imports and mod in imports[dep]:
                report.append(f'🔁 Import circular între {mod} ↔ {dep}')

    if len(report) == 1:
        report.append('✅ Nicio dependență circulară găsită.')
    return '\n'.join(report)

if __name__ == '__main__':
    print(check_import_cycles())