from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path('/home/user/harvest')
HTML_FILES = sorted(ROOT.glob('*.html'))

required_checks = []

for path in HTML_FILES:
    soup = BeautifulSoup(path.read_text(), 'lxml')
    empty_src = [img for img in soup.find_all('img') if img.get('src', '').strip() == '']
    required_checks.append((path.name, 'empty_img_src', len(empty_src) == 0, len(empty_src)))
    skip_link = soup.find('a', class_='skip-link') is not None
    required_checks.append((path.name, 'skip_link', skip_link, 'present' if skip_link else 'missing'))
    main_id = soup.find('main', id='main-content') is not None
    required_checks.append((path.name, 'main_id', main_id, 'present' if main_id else 'missing'))

estimate = ROOT / 'estimate.html'
estimate_text = estimate.read_text()
required_checks.append(('estimate.html', 'duplicate_toggle_function_removed', estimate_text.count('function toggleProjectTypeOther()') == 1, estimate_text.count('function toggleProjectTypeOther()')))
required_checks.append(('estimate.html', 'preferred_contact_method_present', 'preferred_contact_method' in estimate_text, 'preferred_contact_method' in estimate_text))
required_checks.append(('index.html', 'video_poster_present', 'welcome-video-poster.jpg' in (ROOT / 'index.html').read_text(), 'welcome-video-poster.jpg' in (ROOT / 'index.html').read_text()))
required_checks.append(('proof-kit.html', 'noindex_present', 'noindex, nofollow' in (ROOT / 'proof-kit.html').read_text(), 'noindex, nofollow' in (ROOT / 'proof-kit.html').read_text()))
required_checks.append(('review-tracking-playbook.html', 'noindex_present', 'noindex, nofollow' in (ROOT / 'review-tracking-playbook.html').read_text(), 'noindex, nofollow' in (ROOT / 'review-tracking-playbook.html').read_text()))
required_checks.append(('style.css', 'focus_visible_present', ':focus-visible' in (ROOT / 'assets/style.css').read_text(), ':focus-visible' in (ROOT / 'assets/style.css').read_text()))

for row in required_checks:
    print('\t'.join(map(str, row)))

failed = [row for row in required_checks if not row[2]]
print(f'FAILED={len(failed)}')
