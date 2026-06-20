import json
from pathlib import Path

FAV_PATH = Path('storage/favorites.json')


def load_favorites():
    try:
        if FAV_PATH.exists():
            return json.loads(FAV_PATH.read_text(encoding='utf-8'))
    except Exception:
        pass
    return []


def save_favorites(favs):
    FAV_PATH.parent.mkdir(exist_ok=True)
    FAV_PATH.write_text(json.dumps(sorted(set(favs)), ensure_ascii=False, indent=2), encoding='utf-8')


def toggle(symbol):
    s = symbol.upper().replace('.IS','')
    favs = load_favorites()
    if s in favs: favs.remove(s)
    else: favs.append(s)
    save_favorites(favs)
    return favs
