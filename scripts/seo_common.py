"""Shared, factual metadata for static pages; no claims of ranking or endorsement."""
import json
from html import escape

ORIGIN = 'https://posetoki.com'
LANGS = {'ko': 'ko', 'ja': 'ja', 'en': 'en', 'zh-TW': 'zh-tw'}
AUTHOR = {'ko': '제레미', 'ja': 'ジェレミー', 'en': 'Jeremy', 'zh-TW': '傑瑞米'}
HOME = {'ko': '/', 'ja': '/ja/', 'en': '/en/', 'zh-TW': '/zh-tw/'}
LOCALES = {'ko': 'ko_KR', 'ja': 'ja_JP', 'en': 'en_US', 'zh-TW': 'zh_TW'}
HOME_LABEL = {'ko': '크로키 연습실', 'ja': 'クロッキー練習室', 'en': 'Gesture drawing studio', 'zh-TW': '人物速寫練習室'}
DATE = '2026-10-02'


def jsonld(data):
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c') + '</script>'


def metadata(lang, title, description, url, image='/assets/pose-01.jpg', kind='website'):
    image = image if image.startswith('https://') else ORIGIN + image
    tags = {
        'og:type': kind, 'og:site_name': 'PoseToki', 'og:title': title,
        'og:description': description, 'og:url': url, 'og:locale': LOCALES[lang],
        'og:image': image, 'og:image:alt': title,
    }
    return ('<meta name="robots" content="index,follow,max-image-preview:large">\n'
        + '\n'.join(f'<meta property="{key}" content="{escape(value, quote=True)}">' for key, value in tags.items())
        + '\n<meta name="twitter:card" content="summary_large_image">\n')


def page_schema(lang, slug, title, description, image=None, kind='Article', items=None):
    url = f'{ORIGIN}/{LANGS[lang]}/{slug}.html'
    author = {'@type': 'Person', '@id': ORIGIN + '/#jeremy', 'name': AUTHOR[lang], 'url': f'{ORIGIN}/{LANGS[lang]}/about.html#operator'}
    node = {'@type': kind, '@id': url + '#content', 'url': url, 'name': title,
        'description': description, 'inLanguage': lang, 'isAccessibleForFree': True,
        'isPartOf': {'@id': ORIGIN + '/#website'}}
    if kind == 'Article':
        node.update(headline=title, author=author, publisher=author,
                    datePublished=DATE, dateModified=DATE, mainEntityOfPage=url)
    if image:
        node['image'] = ORIGIN + image
    if items:
        node['mainEntity'] = {'@type': 'ItemList', 'numberOfItems': len(items), 'itemListElement': items}
    breadcrumb = {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': HOME_LABEL[lang], 'item': ORIGIN + HOME[lang]},
        {'@type': 'ListItem', 'position': 2, 'name': title, 'item': url},
    ]}
    return jsonld({'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', '@id': ORIGIN + '/#website', 'name': 'PoseToki', 'alternateName': '포즈토키', 'url': ORIGIN + '/', 'inLanguage': list(LANGS), 'publisher': author},
        node, breadcrumb]})


def byline(lang):
    label = {'ko': '작성·운영', 'ja': '執筆・運営', 'en': 'Written and maintained by', 'zh-TW': '撰寫與營運'}[lang]
    return f'<p class="byline">{label}: <a href="/{LANGS[lang]}/about.html#operator">{AUTHOR[lang]}</a></p>'
