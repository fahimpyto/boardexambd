from bs4 import BeautifulSoup
from pathlib import Path
import re

ARTICLES = [
    'hsc-2026-result.html', 'hsc-form-fillup-2027.html', 'hsc-practical-2026.html',
    'buet-admission-2026-27.html', 'du-a-unit-admission-2026-27.html',
    'gst-a-unit-admission-2026-27.html', 'ku-admission-2026-27.html',
    'medical-admission-2026-27.html', 'ru-admission-2026-27.html',
    'ruet-admission-2026-27.html', 'sust-admission-2026-27.html',
]

for name in ARTICLES:
    soup = BeautifulSoup(Path(name).read_text(encoding='utf-8'), 'html.parser')
    article = soup.find('article')
    print('\n' + '=' * 95 + '\n' + name)
    if not article:
        continue
    for section in article.find_all('section', recursive=False):
        heading = section.find(['h2', 'h3'])
        label = heading.get_text(' ', strip=True) if heading else '(key facts / note)'
        text = ' '.join(section.get_text(' ', strip=True).split())
        print('\n## ' + label)
        print(text[:1200])
PY