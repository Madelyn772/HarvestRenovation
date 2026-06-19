from pathlib import Path
import json
import re
from bs4 import BeautifulSoup

ROOT = Path('/home/user/harvest')
ASSETS = ROOT / 'assets'
BASE_URL = ''
PHONE = '+18329440267'
DISPLAY_PHONE = '(832) 944-0267'
MAPS_URL = 'https://www.google.com/maps/place/?q=place_id:ChIJs7OEKzydDKwRJuC_EZywum0'
REVIEWS_URL = MAPS_URL
FACEBOOK_URL = 'https://www.facebook.com/profile.php?id=61551641154186'
INSTAGRAM_URL = 'https://www.instagram.com/harvestrenovation/'
LOGO_URL = BASE_URL + '/assets/harvest-logo.png'
OG_IMAGE = BASE_URL + '/assets/1A44778A-CFC5-4E64-9116-0873704C0077.PNG'

PAGE_META = {
    'index.html': {
        'title': 'Houston Remodeling Contractor | Kitchens, Baths & Renovations | Harvest Renovation',
        'share_title': 'Harvest Renovation - Residential & Commercial Remodeling',
        'description': 'Harvest Renovation is a Houston remodeling contractor serving Houston, South Houston, and surrounding communities for kitchen remodeling, bathroom remodeling, flooring, interior painting, and full home renovations.',
        'canonical': BASE_URL + '/',
    },
    'estimate.html': {
        'title': 'Request a Free Remodeling Estimate | Harvest Renovation Houston',
        'description': 'Request a free remodeling estimate from Harvest Renovation in Houston. Share your project details, service-area ZIP code, and preferred contact method for a faster follow-up.',
        'canonical': BASE_URL + '/estimate.html',
    },
    'kitchen-remodeling.html': {
        'title': 'Kitchen Remodeling in Houston | Harvest Renovation',
        'description': 'Kitchen remodeling in Houston, South Houston, and surrounding communities with cabinetry, countertops, lighting, flooring, and finish updates by Harvest Renovation.',
        'canonical': BASE_URL + '/kitchen-remodeling.html',
    },
    'bathroom-remodeling.html': {
        'title': 'Bathroom Remodeling in Houston | Harvest Renovation',
        'description': 'Bathroom remodeling in Houston, South Houston, and surrounding communities with tile, vanity, lighting, storage, and finish upgrades by Harvest Renovation.',
        'canonical': BASE_URL + '/bathroom-remodeling.html',
    },
    'flooring-installation.html': {
        'title': 'Flooring Installation in Houston | Harvest Renovation',
        'description': 'Flooring installation in Houston, South Houston, and surrounding communities for luxury vinyl plank, laminate, tile, and whole-home flooring upgrades.',
        'canonical': BASE_URL + '/flooring-installation.html',
    },
    'interior-painting.html': {
        'title': 'Interior Painting in Houston | Harvest Renovation',
        'description': 'Interior painting in Houston, South Houston, and surrounding communities with clean prep, crisp finishes, trim painting, and whole-home repainting.',
        'canonical': BASE_URL + '/interior-painting.html',
    },
    'full-home-renovation.html': {
        'title': 'Full Home Renovation in Houston | Harvest Renovation',
        'description': 'Full home renovation in Houston, South Houston, and surrounding communities for coordinated multi-room remodeling, finish updates, and contractor-led planning.',
        'canonical': BASE_URL + '/full-home-renovation.html',
    },
    'proof-kit.html': {
        'title': 'Proof Kit | Harvest Renovation',
        'description': 'Internal proof framework for Harvest Renovation reviews, project stories, and before-and-after content.',
        'canonical': BASE_URL + '/proof-kit.html',
        'robots': 'noindex, nofollow'
    },
    'review-tracking-playbook.html': {
        'title': 'Review and Tracking Playbook | Harvest Renovation',
        'description': 'Internal operational playbook for Harvest Renovation reviews, follow-up, and lead tracking.',
        'canonical': BASE_URL + '/review-tracking-playbook.html',
        'robots': 'noindex, nofollow'
    },
}

SERVICE_CONFIG = {
    'kitchen-remodeling.html': {
        'hero': 'assets/kitchen-hero.jpg',
        'alt': 'Kitchen remodeling finishes and cabinetry detail by Harvest Renovation',
        'service_name': 'Kitchen Remodeling',
        'float_title': 'Plan a kitchen that works harder every day',
        'float_text': 'Cabinets, countertops, lighting, storage, and layout updates built around how you cook and gather.',
        'faq': [
            ('What kind of kitchen projects are a good fit?', 'This page is a good fit for homeowners planning anything from a cosmetic kitchen update to a more complete remodel.'),
            ('What should I include in my estimate request?', 'Share what feels outdated, what you want to improve, and whether the biggest priorities are storage, layout, finishes, or lighting.'),
            ('How do I get the fastest response?', 'Call now for fastest response, or request your estimate online and expect a reply within 1 business day.'),
        ],
    },
    'bathroom-remodeling.html': {
        'hero': 'assets/bathroom-hero.jpg',
        'alt': 'Bathroom planning materials and finish selections for a remodel',
        'service_name': 'Bathroom Remodeling',
        'float_title': 'Create a cleaner, brighter bathroom',
        'float_text': 'Tile, vanity, lighting, storage, and finish updates designed around comfort, function, and easy upkeep.',
        'faq': [
            ('Can this page work for guest baths and primary baths?', 'Yes. It is designed for homeowners updating smaller bathrooms as well as more involved primary-bath projects.'),
            ('What details help with the estimate request?', 'Share whether you want a simple visual update, a more functional layout, or a more complete bathroom transformation.'),
            ('How do I get the fastest response?', 'Call now for fastest response, or request your estimate online and expect a reply within 1 business day.'),
        ],
    },
    'flooring-installation.html': {
        'hero': 'assets/flooring-hero.jpg',
        'alt': 'Open room flooring and finish detail for a home renovation project',
        'service_name': 'Flooring Installation',
        'float_title': 'Upgrade worn floors with cleaner transitions',
        'float_text': 'Luxury vinyl plank, laminate, tile, and detail work that help the whole home feel more finished.',
        'faq': [
            ('Should I include square footage in my estimate request?', 'If you know it, that is helpful. If not, sharing the number of rooms or main areas involved is enough to start the conversation.'),
            ('Can you help with partial-home and whole-home flooring updates?', 'Yes. This page works for both smaller flooring projects and larger home-wide refreshes.'),
            ('How do I get the fastest response?', 'Call now for fastest response, or request your estimate online and expect a reply within 1 business day.'),
        ],
    },
    'interior-painting.html': {
        'hero': 'assets/interior-painting-hero.jpg',
        'alt': 'Interior project planning materials and paint-ready renovation details',
        'service_name': 'Interior Painting',
        'float_title': 'Refresh interiors with clean, crisp finishes',
        'float_text': 'Walls, ceilings, trim, prep work, and repainting support for single-room updates or larger interior refreshes.',
        'faq': [
            ('What kind of painting projects fit this page?', 'This page works for everything from a single-room refresh to broader interior painting throughout the home.'),
            ('What helps with the estimate request?', 'Share the rooms involved, whether the home is occupied, and anything that needs repair or extra prep before painting.'),
            ('How do I get the fastest response?', 'Call now for fastest response, or request your estimate online and expect a reply within 1 business day.'),
        ],
    },
    'full-home-renovation.html': {
        'hero': 'assets/full-home-renovation-hero.jpg',
        'alt': 'Open-concept renovation finishes and layout improvements for a larger remodel',
        'service_name': 'Full Home Renovation',
        'float_title': 'Coordinate bigger change with one plan',
        'float_text': 'Multi-room updates, finish work, and contractor-led coordination that keep a larger renovation organized.',
        'faq': [
            ('What projects are a good fit for this page?', 'This page is best for homeowners planning multiple-room upgrades, larger interior updates, or a staged renovation with one contractor coordinating the work.'),
            ('What should I include in the estimate request?', 'List the rooms involved, the main issues you want solved, and whether you want everything handled at once or in phases.'),
            ('How do I get the fastest response?', 'Call now for fastest response, or request your estimate online and expect a reply within 1 business day.'),
        ],
    },
}

GALLERY_ITEMS = [
    ('assets/gallery-kitchen-1.jpg', 'Kitchen remodeling visual from Harvest Renovation’s current public project library', 'Kitchen remodeling visual from Harvest Renovation’s current public project library.'),
    ('assets/gallery-planning-1.jpg', 'Planning and material-selection visual from Harvest Renovation’s current public project library', 'Planning and material selections before installation and finish work.'),
    ('assets/gallery-kitchen-2.jpg', 'Open-concept renovation finishes from Harvest Renovation’s current public project library', 'Updated finishes, brighter surfaces, and a cleaner flow through the room.'),
    ('assets/gallery-planning-2.jpg', 'Renovation planning image showing tools, layout, and finish coordination', 'Project planning and prep work that support a smoother remodeling process.'),
    ('assets/gallery-kitchen-3.jpg', 'Interior finish detail from Harvest Renovation’s current public project library', 'Craftsmanship details and finish decisions that help a remodel feel complete.'),
    ('assets/gallery-planning-3.jpg', 'Home remodeling preparation image from Harvest Renovation’s current public project library', 'Current project visuals from Harvest Renovation’s existing public brand library while more before-and-after photography is being organized.'),
]


def ensure_meta(soup, head, attrs, content=None):
    tag = None
    if 'name' in attrs:
        tag = head.find('meta', attrs={'name': attrs['name']})
    elif 'property' in attrs:
        tag = head.find('meta', attrs={'property': attrs['property']})
    if not tag:
        tag = soup.new_tag('meta')
        for key, value in attrs.items():
            tag[key] = value
        head.append(tag)
    if content is not None:
        tag['content'] = content
    return tag


def ensure_link(soup, head, rel, href):
    tag = head.find('link', attrs={'rel': rel})
    if not tag:
        tag = soup.new_tag('link', rel=rel)
        head.append(tag)
    tag['href'] = href
    return tag


def append_json_ld(soup, payload):
    tag = soup.new_tag('script', type='application/ld+json')
    tag.string = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))
    soup.head.append(tag)


def add_common_head(soup, file_name):
    meta = PAGE_META[file_name]
    soup.title.string = meta['title']
    ensure_meta(soup, soup.head, {'name': 'description'}, meta['description'])
    ensure_meta(soup, soup.head, {'name': 'theme-color'}, '#0d0d0d')
    ensure_meta(soup, soup.head, {'name': 'color-scheme'}, 'dark')
    ensure_link(soup, soup.head, 'canonical', meta['canonical'])
    if meta.get('robots'):
        ensure_meta(soup, soup.head, {'name': 'robots'}, meta['robots'])
    ensure_meta(soup, soup.head, {'property': 'og:type'}, 'website')
    ensure_meta(soup, soup.head, {'property': 'og:site_name'}, 'Harvest Renovation')
    share_title = meta.get('share_title', meta['title'])
    ensure_meta(soup, soup.head, {'property': 'og:title'}, share_title)
    ensure_meta(soup, soup.head, {'property': 'og:description'}, meta['description'])
    ensure_meta(soup, soup.head, {'property': 'og:url'}, meta['canonical'])
    ensure_meta(soup, soup.head, {'property': 'og:image'}, OG_IMAGE)
    ensure_meta(soup, soup.head, {'property': 'og:image:alt'}, 'Harvest Renovation Houston remodeling contractor promotional graphic')
    ensure_meta(soup, soup.head, {'name': 'twitter:card'}, 'summary_large_image')
    ensure_meta(soup, soup.head, {'name': 'twitter:title'}, share_title)
    ensure_meta(soup, soup.head, {'name': 'twitter:description'}, meta['description'])
    ensure_meta(soup, soup.head, {'name': 'twitter:image'}, OG_IMAGE)


def add_skip_link_and_main_id(soup):
    body = soup.body
    if not body.find('a', class_='skip-link'):
        skip = soup.new_tag('a', href='#main-content', **{'class': 'skip-link'})
        skip.string = 'Skip to main content'
        body.insert(0, skip)
    main = soup.find('main')
    if main:
        main['id'] = 'main-content'


def normalize_common_links(soup):
    for link in soup.find_all('a', href=True):
        href = link['href']
        classes = set(link.get('class', []))
        text = ' '.join(link.stripped_strings)
        if href.startswith('tel:'):
            classes.add('track-phone-click')
            link['aria-label'] = f'Call Harvest Renovation at {DISPLAY_PHONE}'
        if 'estimate.html#project-request-form' in href or href == '#project-request-form':
            classes.add('track-service-cta')
        if 'google.com/search' in href or 'place_id:' in href:
            link['href'] = REVIEWS_URL
            if 'View Google Reviews' in text or 'Reviews' in text:
                classes.add('track-maps-click')
        link['class'] = sorted(classes)


def add_home_schema(soup):
    payload = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'WebSite',
                '@id': BASE_URL + '/#website',
                'url': BASE_URL + '/',
                'name': 'Harvest Renovation',
                'publisher': {'@id': BASE_URL + '/#business'},
            },
            {
                '@type': 'GeneralContractor',
                '@id': BASE_URL + '/#business',
                'name': 'Harvest Renovation',
                'url': BASE_URL + '/',
                'telephone': DISPLAY_PHONE,
                'image': [OG_IMAGE, BASE_URL + '/assets/gallery-kitchen-1.jpg'],
                'logo': LOGO_URL,
                'areaServed': ['Houston', 'South Houston'],
                'sameAs': [FACEBOOK_URL, INSTAGRAM_URL, MAPS_URL],
                'address': {
                    '@type': 'PostalAddress',
                    'addressLocality': 'Houston',
                    'addressRegion': 'TX',
                    'addressCountry': 'US'
                },
                'openingHoursSpecification': [{
                    '@type': 'OpeningHoursSpecification',
                    'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
                    'opens': '08:00',
                    'closes': '18:00'
                }]
            }
        ]
    }
    append_json_ld(soup, payload)


def add_estimate_schema(soup):
    payload = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'ContactPage',
                'name': 'Request a Free Remodeling Estimate',
                'url': BASE_URL + '/estimate.html',
                'about': {'@id': BASE_URL + '/#business'},
                'mainEntity': {'@id': BASE_URL + '/#business'},
            },
            {
                '@type': 'GeneralContractor',
                '@id': BASE_URL + '/#business',
                'name': 'Harvest Renovation',
                'url': BASE_URL + '/',
                'telephone': DISPLAY_PHONE,
                'sameAs': [FACEBOOK_URL, INSTAGRAM_URL, MAPS_URL],
                'areaServed': ['Houston', 'South Houston']
            }
        ]
    }
    append_json_ld(soup, payload)


def add_service_schema(soup, file_name):
    config = SERVICE_CONFIG[file_name]
    service_url = PAGE_META[file_name]['canonical']
    faq_entities = []
    for question, answer in config['faq']:
        faq_entities.append({
            '@type': 'Question',
            'name': question,
            'acceptedAnswer': {'@type': 'Answer', 'text': answer}
        })
    payload = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'Service',
                'serviceType': config['service_name'],
                'name': f"{config['service_name']} in Houston",
                'url': service_url,
                'areaServed': ['Houston', 'South Houston'],
                'provider': {
                    '@type': 'GeneralContractor',
                    'name': 'Harvest Renovation',
                    'url': BASE_URL + '/',
                    'telephone': DISPLAY_PHONE,
                }
            },
            {
                '@type': 'FAQPage',
                'mainEntity': faq_entities
            }
        ]
    }
    append_json_ld(soup, payload)


def update_homepage(soup):
    proof_section = soup.find('section', id='reviews')
    if proof_section:
        proof_section['id'] = 'proof'
        container = proof_section.find('div', class_='container')
        if container:
            reviews_anchor = soup.new_tag('div', id='reviews')
            container.insert(0, reviews_anchor)
    video = soup.find('video', id='welcome-video')
    if video:
        video['poster'] = 'assets/welcome-video-poster.jpg'
        video['preload'] = 'none'
        video['aria-label'] = 'Welcome video from Harvest Renovation'
        video['controlslist'] = 'nodownload'
    hero_img = soup.select_one('.hero-media > img')
    if hero_img:
        hero_img['src'] = 'assets/kitchen-hero.jpg'
        hero_img['alt'] = 'Kitchen renovation finish detail by Harvest Renovation'
        hero_img['fetchpriority'] = 'high'
        hero_img['decoding'] = 'async'
    secondary_img = soup.select_one('section .grid-2 .panel.card img')
    if secondary_img:
        secondary_img['src'] = 'assets/gallery-planning-1.jpg'
        secondary_img['alt'] = 'Remodel planning materials and job-prep detail'
        secondary_img['loading'] = 'lazy'
        secondary_img['decoding'] = 'async'
    gallery = soup.select_one('#images .gallery-grid')
    if gallery:
        gallery.clear()
        for src, alt, caption in GALLERY_ITEMS:
            fig = soup.new_tag('figure', **{'class': 'gallery-card'})
            img = soup.new_tag('img', src=src, alt=alt, loading='lazy', decoding='async')
            cap = soup.new_tag('figcaption')
            cap.string = caption
            fig.append(img)
            fig.append(cap)
            gallery.append(fig)
        paragraph = soup.select_one('#images .section-head p')
        if paragraph:
            paragraph.string = 'Current visuals from Harvest Renovation’s public brand library. Additional before-and-after project photography can be shared during your estimate conversation.'
    review_link = soup.find('a', string=lambda text: text and 'View Google Reviews' in text)
    if review_link:
        review_link['href'] = REVIEWS_URL
        review_link['class'] = sorted(set(review_link.get('class', []) + ['track-maps-click']))
    callout_p = soup.select_one('.callout .section-head p')
    if callout_p:
        callout_p.string = 'Call now for the fastest response, request your estimate online, or review our Google Maps listing before you reach out.'
    callout_actions = soup.select_one('.callout .hero-actions')
    if callout_actions and not callout_actions.find('a', href=MAPS_URL):
        maps_link = soup.new_tag('a', href=MAPS_URL, **{'class': 'btn btn-secondary track-maps-click'})
        maps_link.string = 'View Google Maps Listing'
        callout_actions.append(maps_link)
    add_home_schema(soup)


def update_estimate_page(soup):
    form = soup.find('form', id='estimate-request-form')
    if form:
        form['novalidate'] = 'novalidate'
        hidden_fields = {
            '_template': 'table',
            'source_page': 'estimate.html',
            'page_title': 'Request a Free Remodeling Estimate',
            'submitted_at_utc': ''
        }
        existing_names = {tag.get('name') for tag in form.find_all('input') if tag.get('name')}
        for name, value in hidden_fields.items():
            if name not in existing_names:
                input_tag = soup.new_tag('input', attrs={'type': 'hidden', 'name': name, 'value': value})
                form.insert(2, input_tag)
        phone_label = None
        for label in form.find_all('label'):
            if label.get_text(strip=True).startswith('Phone'):
                phone_label = label
                break
        if phone_label and not form.find('select', attrs={'name': 'preferred_contact_method'}):
            preferred_label = soup.new_tag('label')
            preferred_label.string = 'Preferred Contact Method'
            select = soup.new_tag('select', attrs={'name': 'preferred_contact_method'})
            for option_text in ['Phone Call', 'Text Message', 'Email', 'Any of the above']:
                option = soup.new_tag('option')
                option.string = option_text
                select.append(option)
            preferred_label.append(select)
            phone_label.insert_after(preferred_label)
        details_label = form.find('textarea', attrs={'name': 'project_details'})
        if details_label:
            details_label['placeholder'] = 'Tell us about the room, work needed, timing, concerns, and whether photos are available.'
        help_block = form.find('div', id='estimate-form-status')
        if help_block:
            help_block['role'] = 'status'
            help_block['aria-live'] = 'polite'
    add_estimate_schema(soup)


def replace_service_hero(soup, file_name):
    config = SERVICE_CONFIG[file_name]
    hero_img = soup.select_one('.hero-media > img')
    if hero_img:
        hero_img['src'] = config['hero']
        hero_img['alt'] = config['alt']
        hero_img['fetchpriority'] = 'high'
        hero_img['decoding'] = 'async'
    float_card = soup.select_one('.hero-media .float-card')
    if float_card:
        h3 = float_card.find('h3')
        p = float_card.find('p')
        if h3:
            h3.string = config['float_title']
        if p:
            p.string = config['float_text']
    add_service_schema(soup, file_name)


def mark_internal_page(soup, title):
    hero_copy = soup.select_one('.subhero .hero-copy')
    if hero_copy and not hero_copy.find(class_='internal-page-note'):
        note = soup.new_tag('p', **{'class': 'internal-page-note'})
        note.string = 'Internal reference page. Keep this URL out of public navigation and search indexing.'
        list_block = hero_copy.find('div', class_='list')
        if list_block:
            list_block.insert_after(note)
        else:
            hero_copy.append(note)


def rewrite_estimate_script(html):
    pattern = re.compile(r'<script>\s*\(function \(\) \{.*?\}\)\(\);\s*</script>', re.S)
    replacement = '''<script>
    (function () {
      function getStickyOffset() {
        var offset = 16;
        var header = document.querySelector('header');
        var quickNav = document.querySelector('.mobile-quick-nav');

        if (header) {
          offset += header.getBoundingClientRect().height;
        }

        if (quickNav) {
          var quickNavStyles = window.getComputedStyle(quickNav);
          if (quickNavStyles.display !== 'none') {
            offset += quickNav.getBoundingClientRect().height + 8;
          }
        }

        return offset;
      }

      function pushTrackingEvent(eventName, payload) {
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push(Object.assign({ event: eventName }, payload || {}));
      }

      function scrollToHash(hash, updateHistory) {
        if (!hash || hash.charAt(0) !== '#') return;

        var id = decodeURIComponent(hash.slice(1));
        var target = document.getElementById(id);
        if (!target) return;

        var top = target.getBoundingClientRect().top + window.scrollY - getStickyOffset();

        window.scrollTo({ top: Math.max(top, 0), behavior: 'smooth' });

        if (updateHistory) {
          history.replaceState(null, '', '#' + id);
        }
      }

      document.addEventListener('click', function (event) {
        var link = event.target.closest('a');
        if (!link) return;

        var href = link.getAttribute('href') || '';
        var linkText = (link.textContent || '').trim();

        if (href.indexOf('#') > -1) {
          var hashIndex = href.indexOf('#');
          var path = href.slice(0, hashIndex);
          var hash = href.slice(hashIndex);

          if (!path || path === 'estimate.html') {
            event.preventDefault();
            scrollToHash(hash, true);
          }
        }

        if (href.indexOf('tel:') === 0) {
          pushTrackingEvent('click_to_call', { link_text: linkText, page_path: window.location.pathname });
        }

        if (href.indexOf('place_id:') > -1 || href.indexOf('google.com/maps') > -1) {
          pushTrackingEvent('maps_click', { link_text: linkText, page_path: window.location.pathname });
        }
      });

      function scrollFromCurrentHash() {
        if (!window.location.hash) return;
        scrollToHash(window.location.hash, false);
      }

      window.addEventListener('load', function () {
        scrollFromCurrentHash();
        setTimeout(scrollFromCurrentHash, 120);
      });

      window.addEventListener('hashchange', function () {
        scrollFromCurrentHash();
      });

      var projectTypeSource = document.getElementById('project-type-source');
      var projectTypeOtherRow = document.getElementById('project-type-other-row');
      var projectTypeOther = document.getElementById('project-type-other');
      var heardAboutSource = document.getElementById('heard-about-source');
      var heardAboutOtherRow = document.getElementById('heard-about-other-row');
      var heardAboutOther = document.getElementById('heard-about-other');
      var estimateForm = document.getElementById('estimate-request-form');
      var estimateSubmitBtn = document.getElementById('estimate-submit-btn');
      var estimateStatus = document.getElementById('estimate-form-status');

      function toggleConditionalField(sourceField, rowField, textField) {
        if (!sourceField || !rowField || !textField) return;

        var showOther = sourceField.value === 'Other';
        rowField.style.display = showOther ? 'grid' : 'none';
        textField.disabled = !showOther;

        if (!showOther) {
          textField.value = '';
        }
      }

      function toggleProjectTypeOther() {
        toggleConditionalField(projectTypeSource, projectTypeOtherRow, projectTypeOther);
      }

      function toggleHeardAboutOther() {
        toggleConditionalField(heardAboutSource, heardAboutOtherRow, heardAboutOther);
      }

      if (projectTypeSource) {
        projectTypeSource.addEventListener('change', toggleProjectTypeOther);
        toggleProjectTypeOther();
      }

      if (heardAboutSource) {
        heardAboutSource.addEventListener('change', toggleHeardAboutOther);
        toggleHeardAboutOther();
      }

      function setHiddenFieldValue(name, value) {
        if (!estimateForm) return;
        var field = estimateForm.querySelector('[name="' + name + '"]');
        if (field) {
          field.value = value;
        }
      }

      if (estimateForm && estimateSubmitBtn && estimateStatus) {
        estimateForm.addEventListener('submit', function (event) {
          event.preventDefault();

          if (!estimateForm.reportValidity()) {
            estimateStatus.textContent = 'Please complete the required fields before sending your request.';
            return;
          }

          setHiddenFieldValue('submitted_at_utc', new Date().toISOString());
          setHiddenFieldValue('source_page', window.location.pathname || '/estimate.html');
          setHiddenFieldValue('page_title', document.title);

          estimateStatus.textContent = 'Sending your request...';
          estimateSubmitBtn.disabled = true;
          pushTrackingEvent('generate_lead_attempt', { page_path: window.location.pathname, project_type: projectTypeSource ? projectTypeSource.value : '' });

          fetch(estimateForm.action, {
            method: 'POST',
            body: new FormData(estimateForm),
            headers: { Accept: 'application/json' }
          })
            .then(function (response) {
              if (!response.ok) throw new Error('Request failed');
              return response.json().catch(function () { return {}; });
            })
            .then(function () {
              estimateStatus.textContent = 'Thanks. Your estimate request was sent successfully. Harvest Renovation will follow up soon.';
              pushTrackingEvent('generate_lead', { page_path: window.location.pathname, project_type: projectTypeSource ? projectTypeSource.value : '' });
              estimateForm.reset();
              toggleProjectTypeOther();
              toggleHeardAboutOther();
            })
            .catch(function () {
              estimateStatus.textContent = 'Something went wrong while sending the form. Please call Harvest Renovation at (832) 944-0267 for the fastest response.';
              pushTrackingEvent('generate_lead_error', { page_path: window.location.pathname });
            })
            .finally(function () {
              estimateSubmitBtn.disabled = false;
            });
        });
      }
    })();
  </script>'''
    return pattern.sub(replacement, html, count=1)


def add_global_tracking_script(html):
    script = '''<script>
    (function () {
      function pushTrackingEvent(eventName, payload) {
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push(Object.assign({ event: eventName }, payload || {}));
      }

      document.addEventListener('click', function (event) {
        var link = event.target.closest('a');
        if (!link) return;

        var href = link.getAttribute('href') || '';
        var linkText = (link.textContent || '').trim();

        if (href.indexOf('tel:') === 0) {
          pushTrackingEvent('click_to_call', { link_text: linkText, page_path: window.location.pathname });
        }

        if (href.indexOf('estimate.html#project-request-form') > -1) {
          pushTrackingEvent('service_page_cta', { link_text: linkText, page_path: window.location.pathname });
        }

        if (href.indexOf('place_id:') > -1 || href.indexOf('google.com/maps') > -1) {
          pushTrackingEvent('maps_click', { link_text: linkText, page_path: window.location.pathname });
        }
      });
    })();
  </script>'''
    return html.replace('</body>', script + '\n</body>')


def update_css():
    css_path = ASSETS / 'style.css'
    css = css_path.read_text()
    replacements = {
        '--anchor-offset: 102px;': '--anchor-offset: 102px;\n  --focus-ring: rgba(241, 194, 125, 0.95);\n  --focus-shadow: 0 0 0 3px rgba(241, 194, 125, 0.22);',
        'a { color: inherit; text-decoration: none; }': 'a { color: inherit; text-decoration: none; }\nbutton { font: inherit; }\nbutton, select, input, textarea { -webkit-appearance: none; appearance: none; }',
        'img { max-width: 100%; display: block; }': 'img { max-width: 100%; display: block; height: auto; }\nvideo { max-width: 100%; display: block; }',
        '  .brand > div > div {\n    font-size: 13px;': '  .brand > div > div {\n    font-size: 14px;',
        '    font-size: 9px;': '    font-size: 10px;',
        '    min-height: 30px;\n    padding: 5px 8px;\n    font-size: 8.8px;': '    min-height: 36px;\n    padding: 7px 10px;\n    font-size: 10.4px;',
        '    font-size: 8.5px;\n    line-height: 1.2;': '    font-size: 12px;\n    line-height: 1.35;',
        '    font-size: 8.5px;\n    line-height: 1.2;\n    flex: 0 0 auto;': '    font-size: 11.5px;\n    line-height: 1.3;\n    flex: 0 0 auto;',
        '  :root { --anchor-offset: 190px; }': '  :root { --anchor-offset: 176px; }',
        '    grid-template-columns: minmax(0, 1fr) 140px;': '    grid-template-columns: minmax(0, 1fr) 164px;',
        '    font-size: 11.3px;': '    font-size: 12.8px;',
        '    font-size: 8px;': '    font-size: 10.2px;',
        '    max-width: 118px;': '    max-width: 132px;',
        '    width: 140px;': '    width: 164px;',
        '    min-width: 140px;': '    min-width: 164px;',
        '    min-height: 30px;\n    padding: 5px 8px;\n    font-size: 8.8px;': '    min-height: 38px;\n    padding: 8px 10px;\n    font-size: 10.6px;',
        '    min-height: 32px;': '    min-height: 40px;',
        '    font-size: 8.5px;': '    font-size: 10.5px;',
        '  .hero-copy p.lead { font-size: 14px; }': '  .hero-copy p.lead { font-size: 15.5px; }',
        '    font-size: 8.5px;\n    line-height: 1.3;': '    font-size: 11.5px;\n    line-height: 1.45;',
        '    font-size: 8.5px;\n    line-height: 1.25;': '    font-size: 11.5px;\n    line-height: 1.35;',
    }
    for old, new in replacements.items():
        css = css.replace(old, new)

    additions = '''\n.skip-link {\n  position: absolute;\n  left: 16px;\n  top: -60px;\n  z-index: 999;\n  padding: 12px 16px;\n  border-radius: 14px;\n  background: #fff;\n  color: #111;\n  font-weight: 700;\n  box-shadow: 0 8px 30px rgba(0,0,0,0.25);\n}\n.skip-link:focus {\n  top: 16px;\n}\na:focus-visible,\nbutton:focus-visible,\ninput:focus-visible,\ntextarea:focus-visible,\nselect:focus-visible,\nvideo:focus-visible {\n  outline: 2px solid var(--focus-ring);\n  outline-offset: 3px;\n  box-shadow: var(--focus-shadow);\n}\ninput:focus-visible,\ntextarea:focus-visible,\nselect:focus-visible {\n  border-color: rgba(241,194,125,0.75);\n  background: rgba(255,255,255,0.05);\n}\n.internal-page-note {\n  margin-top: 18px;\n  padding: 14px 16px;\n  border-radius: 16px;\n  border: 1px dashed rgba(240, 207, 134, 0.6);\n  background: rgba(240, 207, 134, 0.08);\n  color: var(--warn);\n}\n.gallery-card img {\n  background: rgba(255,255,255,0.02);\n}\n.video-frame {\n  background: #000;\n}\n@media (prefers-reduced-motion: reduce) {\n  html {\n    scroll-behavior: auto;\n  }\n  *, *::before, *::after {\n    animation: none !important;\n    transition: none !important;\n  }\n}\n'''
    if '@media (prefers-reduced-motion: reduce)' not in css:
        css += additions
    css_path.write_text(css)


def save_soup(soup, path):
    html = str(soup)
    html = re.sub(r'\n{3,}', '\n\n', html)
    if path.name == 'estimate.html':
        html = rewrite_estimate_script(html)
    elif path.name in {'index.html', 'kitchen-remodeling.html', 'bathroom-remodeling.html', 'flooring-installation.html', 'interior-painting.html', 'full-home-renovation.html'}:
        html = add_global_tracking_script(html)
    path.write_text(html)


def process_page(path: Path):
    soup = BeautifulSoup(path.read_text(), 'lxml')
    add_common_head(soup, path.name)
    add_skip_link_and_main_id(soup)
    normalize_common_links(soup)

    if path.name == 'index.html':
        update_homepage(soup)
    elif path.name == 'estimate.html':
        update_estimate_page(soup)
    elif path.name in SERVICE_CONFIG:
        replace_service_hero(soup, path.name)
    elif path.name in {'proof-kit.html', 'review-tracking-playbook.html'}:
        mark_internal_page(soup, PAGE_META[path.name]['title'])

    # update outdated internal nav anchor
    for link in soup.find_all('a', href='index.html#proof'):
        link['href'] = 'index.html#reviews'
        if not link.string or link.get_text(strip=True) == 'Proof':
            link.string = 'Testimonials'

    # lazy-load non-critical images
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if 'logo' in (img.get('alt', '').lower()) or src.endswith('image000000_edited.png'):
            continue
        if img.parent and 'hero-media' in img.parent.get('class', []):
            continue
        if not img.get('loading'):
            img['loading'] = 'lazy'
        if not img.get('decoding'):
            img['decoding'] = 'async'

    save_soup(soup, path)


def main():
    update_css()
    for file_name in PAGE_META:
        process_page(ROOT / file_name)
    print('Updated HTML and CSS files.')


if __name__ == '__main__':
    main()
