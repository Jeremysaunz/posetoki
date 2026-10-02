"""Build the verified asset manifest. Missing images fail the build."""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'research/pose-library-120-catalog.json'
catalog = json.loads(source.read_text())
translations = {}
for line in (ROOT / 'scripts/pose-translations.tsv').read_text().splitlines():
    fields = line.split('|')
    assert len(fields) == 7, fields
    translations[fields[0]] = fields[1:]
assert len(translations) == 120
levels = {'초급': 'beginner', '중급': 'intermediate', '고급': 'advanced'}
records = []
for pose in catalog:
    identifier = pose['id']
    existing = pose['existing_asset']
    image_path = ('/assets/' + Path(existing).name) if existing else f'/assets/library/{identifier}.jpg'
    path = ROOT / 'dist' / image_path.lstrip('/')
    if not path.is_file():
        raise FileNotFoundError(f'{identifier}: {path}')
    with Image.open(path) as im:
        width, height = im.size
        thumb = im.convert('RGB')
        thumb.thumbnail((256, 256))
        target = ROOT / 'dist/assets/thumbs' / f'{identifier}.jpg'
        target.parent.mkdir(parents=True, exist_ok=True)
        thumb.save(target, quality=80, optimize=True)
    en, ja, zh, fen, fja, fzh = translations[identifier]
    records.append({
        'id': identifier, 'category': pose['category_code'],
        'name': {'ko': pose['name_ko'], 'en': en, 'ja': ja, 'zh-TW': zh},
        'focus': {'ko': pose['learning_focus'], 'en': fen, 'ja': fja, 'zh-TW': fzh},
        'level': levels[pose['difficulty']], 'seconds': pose['recommended_seconds'],
        'image': image_path, 'thumb': f'/assets/thumbs/{identifier}.jpg',
        'width': width, 'height': height, 'source': 'AI-generated',
        'legacy': int(Path(existing).stem.split('-')[1]) if existing else None,
    })
assert len(records) == 120
assert len({r['image'] for r in records}) == 120
payload = json.dumps(records, ensure_ascii=False, separators=(',', ':'))
(ROOT / 'dist/pose-library.json').write_text(payload + '\n')
(ROOT / 'dist/pose-library.js').write_text('window.PoseTokiPoses=' + payload + ';\n')
print(f'Built {len(records)} distinct asset records and thumbnails.')
