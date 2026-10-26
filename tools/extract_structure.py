from bs4 import BeautifulSoup
from pathlib import Path

ARTICLES = [
    'ssc-2026-routine.html', 'ssc-2026-result.html',
    'ssc-form-fillup-2027.html', 'ssc-board-challenge-2026.html',
    'hsc-2026-routine.html', 'hsc-2026-result.html',
    'hsc-form-fillup-2027.html', 'hsc-practical-2026.html',
    'buet-admission-2026-27.html', 'du-a-unit-admission-2026-27.html',
    'gst-a-unit-admission-2026-27.html', 'ku-admission-2026-27.html',
    'medical-admission-2026-27.html', 'ru-admission-2026-27.html',
    'ruet-admission-2026-27.html', 'sust-admission-2026-27.html',
]

for name in ARTICLES:
    soup = BeautifulSoup(Path(name).read_text(encoding='utf-8'), 'html.parser')
    print('\n' + '=' * 90 + '\n' + name)
    h1 = soup.find('h1')
    print('H1:', h1.get_text(' ', strip=True) if h1 else None)
    hero = h1.find_parent('section') if h1 else None
    if hero:
        print('HERO:', ' '.join(hero.get_text(' ', strip=True).split())[:550])
    article = soup.find('article')
    if article:
        print('H2s:')
        for h in article.find_all('h2'):
            print('  -', h.get_text(' ', strip=True))
        print('H3s:')
        for h in article.find_all('h3'):
            print('  -', h.get_text(' ', strip=True))
        first = article.find('section')
        if first:
            print('FIRST SECTION:', ' '.join(first.get_text(' ', strip=True).split())[:700])

print('\n\n' + '#' * 90)
for name in ['index.html', 'ssc.html', 'hsc.html', 'admission.html']:
    soup = BeautifulSoup(Path(name).read_text(encoding='utf-8'), 'html.parser')
    print('\n' + '=' * 80 + '\n' + name)
    print('TITLE:', soup.title.get_text() if soup.title else '')
    h1 = soup.find('h1')
    print('H1:', h1.get_text(' ', strip=True) if h1 else None)
    for h in soup.find_all(['h2', 'h3']):
        print(h.name.upper() + ':', h.get_text(' ', strip=True))
