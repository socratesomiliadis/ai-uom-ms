"""Rebuild clean teaching distributions using only Python's standard library."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs'
IGNORED = {'.git', 'target', 'reports', '.eval-work', '__pycache__', '.venv', 'node_modules'}

for name in ['ai-production-lab', 'instructor-assets']:
    folder = ROOT / name
    with zipfile.ZipFile(OUT / (name + '.zip'), 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(folder.rglob('*')):
            relative = path.relative_to(folder)
            if not path.is_file() or any(part in IGNORED for part in relative.parts):
                continue
            if path.suffix in {'.log', '.pyc', '.pyo'}:
                continue
            archive.write(path, name + '/' + relative.as_posix())

with zipfile.ZipFile(OUT / 'lecture-teaching-kit.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(OUT.iterdir()):
        if path.is_file() and path.name != 'lecture-teaching-kit.zip':
            archive.write(path, path.name)

for name in ['ai-production-lab.zip', 'instructor-assets.zip', 'lecture-teaching-kit.zip']:
    with zipfile.ZipFile(OUT / name) as archive:
        assert archive.testzip() is None, name
    print('Created', OUT / name)
