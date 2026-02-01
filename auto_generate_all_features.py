import os
import json
import sys
from datetime import datetime

# 🔹 Calea corectă către blueprint (în același folder cu scriptul)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BLUEPRINT_FILE = os.path.join(BASE_PATH, 'master_blueprint.json')

# ==============================================================
# 🔸 Încărcare blueprint existent
# ==============================================================
def load_blueprint():
    if not os.path.exists(BLUEPRINT_FILE):
        print(f"⚠️  Fișierul {BLUEPRINT_FILE} nu există. Rulează mai întâi generate_structure.py --update-blueprint.")
        return None
    with open(BLUEPRINT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# ==============================================================
# 🔸 Funcții auxiliare
# ==============================================================
def sanitize_filename(title):
    text = title.lower()
    replacements = {
        ' ': '_', '-': '_', 'ă': 'a', 'â': 'a', 'î': 'i',
        'ș': 's', 'ş': 's', 'ț': 't', 'ţ': 't'
    }
    for ch, rep in replacements.items():
        text = text.replace(ch, rep)
    return text

def generate_code(feature_id, layer, module, title, description, created):
    class_name = ''.join(word.capitalize() for word in sanitize_filename(title).split('_')) + 'Feature'

    header = f'''"""
====================================================
@synapse-feature: {feature_id}
@module         {layer}.{module}
@title          {title}
@description    {description}
@layer          {layer}
@dependencies   TODO: Completează dependențele relevante
@created        {created}
====================================================
"""\n\n'''

    body = f'''import json, logging\nfrom datetime import datetime\n\nlogger = logging.getLogger(__name__)\nlogger.setLevel(logging.INFO)\nif not logger.handlers:\n    handler = logging.StreamHandler()\n    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))\n    logger.addHandler(handler)\n\nclass {class_name}:\n    def execute(self):\n        logger.info('🧩  Pornire execuție {feature_id} – {title}')\n        # TODO: logica reală\n        return {{\n            'feature_id': '{feature_id}',\n            'status': 'skeleton',\n            'timestamp': datetime.now().isoformat()\n        }}\n\nif __name__ == '__main__':\n    feature = {class_name}()\n    print(json.dumps(feature.execute(), indent=2, ensure_ascii=False))\n'''

    return header + body

# ==============================================================
# 🔸 Creare fișier feature (cu opțiune overwrite)
# ==============================================================
def create_feature_file(base_dir, layer, module, feature_id, title, description, overwrite=False):
    layer_path = os.path.join(base_dir, layer)
    module_path = os.path.join(layer_path, module)
    os.makedirs(module_path, exist_ok=True)

    filename = sanitize_filename(title) + '.py'
    file_path = os.path.join(module_path, filename)

    created = datetime.now().strftime('%Y-%m-%d')
    code = generate_code(feature_id, layer, module, title, description, created)

    if os.path.exists(file_path):
        if not overwrite:
            print(f"📄 Există deja – omis: {file_path}")
            return False
        else:
            print(f"✏️  Suprascris: {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)

    return True

# ==============================================================
# 🔸 Funcția principală
# ==============================================================
def main():
    base_dir = os.path.abspath(BASE_PATH)
    blueprint = load_blueprint()
    if not blueprint:
        return

    overwrite = ('--overwrite' in sys.argv)
    count = 0

    for wave in blueprint.get('waves', []):
        for module in wave['modules']:
            for func in module['functions']:
                fid = func['id']
                title = func['title']
                layer = func['layer'].lower()
                module_name = module['name'].lower().replace(' ', '_')
                description = func.get('description', 'TODO: Adaugă descriere scurtă.')

                if layer not in ['core','operational','automations','ai','extensions','bi','frontend']:
                    continue

                if create_feature_file(base_dir, layer, module_name, fid, title, description, overwrite):
                    count += 1

    print(f"\n🏁 Generare finalizată: {count} fișiere {'actualizate' if overwrite else 'create'} complet cu antet și cod schelet.")

# ==============================================================
# 🔸 Punct de intrare
# ==============================================================
if __name__ == '__main__':
    print(f"\n🚀  CREARE AUTOMATĂ COD-SCHELET SYNAPSE ERP — {datetime.now():%Y-%m-%d %H:%M:%S}\n")
    main()