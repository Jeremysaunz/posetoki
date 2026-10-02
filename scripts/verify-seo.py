#!/usr/bin/env python3
"""Verify crawlable HTML, self-canonicals, reciprocal languages and local links."""
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist';ORIGIN='https://posetoki.com'
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.lang=None;self.meta={};self.links=[];self.refs=[];self.title='';self.h1='';self.tag='';self.schema=[];self.script=False;self.buffer='';self.poses=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tag=tag
  if tag=='html':self.lang=a.get('lang')
  if tag=='meta':self.meta[a.get('name',a.get('property'))]=a.get('content')
  if tag=='link':self.links.append(a)
  if tag=='h1':self.h1+='|'
  if tag in ('a','img','script','link'):
   ref=a.get('src',a.get('href'))
   if ref:self.refs.append(ref)
  if tag=='img':assert a.get('alt') is not None,'image alt missing'
  if tag=='article' and a.get('class')=='reference-card':self.poses+=1
  if tag=='script' and a.get('type')=='application/ld+json':self.script=True;self.buffer=''
 def handle_endtag(self,tag):
  if tag=='script' and self.script:self.schema.append(json.loads(self.buffer));self.script=False
  self.tag=''
 def handle_data(self,data):
  if self.script:self.buffer+=data
  if self.tag=='title':self.title+=data


def route(url):
 path=unquote(urlparse(url).path)
 p=DIST/path.lstrip('/')
 if not p.suffix:p=p/'index.html'
 return p

sitemap=ET.parse(DIST/'sitemap.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','i':'http://www.google.com/schemas/sitemap-image/1.1'}
urls=[n.text for n in sitemap.findall('s:url/s:loc',ns)]
assert len(urls)==len(set(urls))
pages={};errors=[]
for url in urls:
 try:
  file=route(url);parser=Page();source=file.read_text();parser.feed(source);pages[url]=parser
  canonical=[l['href'] for l in parser.links if l.get('rel')=='canonical']
  assert canonical==[url],f'canonical {canonical}'
  assert parser.lang in ('ko','ja','en','zh-TW')
  assert parser.h1.count('|')==1,'one H1 required'
  assert parser.title and parser.meta.get('description')
  assert 'noindex' not in parser.meta.get('robots','')
  assert parser.meta.get('og:url')==url
  assert parser.schema,'missing JSON-LD'
  assert 'ca-pub-5987896746147751' in source
  if 'poses.html' in url:assert parser.poses==120,f'expected 120 reference cards, got {parser.poses}'
  for ref in parser.refs:
   parsed=urlparse(ref)
   if parsed.netloc and parsed.netloc!='posetoki.com':continue
   if parsed.path and parsed.path.startswith('/'):
    assert route(ref).is_file(),f'missing resource: {ref}'
 except (AssertionError,FileNotFoundError,ValueError) as e:errors.append(f'{url}: {e}')
for url,page in pages.items():
 for alt in [l for l in page.links if l.get('rel')=='alternate' and l.get('hreflang') not in (None,'x-default')]:
  other=pages.get(alt['href']);
  if not other:errors.append(f'{url}: alternate missing from sitemap {alt["href"]}');continue
  if not any(l.get('rel')=='alternate' and l.get('href')==url for l in other.links):errors.append(f'{url}: nonreciprocal alternate {alt["href"]}')
images=[i.text for i in sitemap.findall('.//i:loc',ns)]
for url in images:
 if not route(url).is_file():errors.append(f'Image sitemap missing file: {url}')
for label,counts in [('title',Counter(p.title for p in pages.values())),('description',Counter(p.meta.get('description') for p in pages.values()))]:
 for value,n in counts.items():
  if n>1:errors.append(f'Duplicate {label} ({n}): {value}')
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; unique titles/descriptions; reciprocal hreflang; JSON-LD; local links and assets; {len(images)} image sitemap entries')
