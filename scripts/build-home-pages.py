#!/usr/bin/env python3
"""Build fully translated landing pages from one Korean source, without browser rendering."""
import json
import re
import subprocess
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from lesson_content import LESSONS
from discovery_content import COPY as DISCOVERY, load_poses
from seo_common import HOME, ORIGIN, LANGS, metadata, jsonld

ROOT = Path(__file__).resolve().parents[1]
COL = {'ko': 0, 'ja': 1, 'en': 2, 'zh-TW': 3}
HERO = {
 'ko': '보고, 그리고.<br>매일의 <em>크로키 연습.</em>',
 'ja': '見て、描く。<br>毎日の<em>クロッキー練習。</em>',
 'en': 'Look. Draw.<br>Your daily <em>gesture practice.</em>',
 'zh-TW': '看一看，畫下來。<br>每天的<em>人物速寫練習。</em>',
}
FACTS = {
 'ko': ['무료 크로키 타이머 · 120개 인체 포즈', '포즈토키는 미술·웹툰·일러스트 학습자를 위한 무료 크로키 연습 도구입니다. 30초·1분·3분 타이머로 준비된 AI 착의 인물 포즈 또는 내 사진을 보며 연습하세요. 회원가입과 연습 횟수 제한이 없습니다.'],
 'ja': ['無料クロッキータイマー・120の人物ポーズ', 'PoseToki は美術・漫画・イラスト学習者向けの無料クロッキー練習ツールです。30秒・1分・3分のタイマーでAI生成の着衣人物や自分の写真を見て練習できます。登録や練習回数の制限はありません。'],
 'en': ['Free gesture drawing timer · 120 figure poses', 'PoseToki is a free gesture drawing tool for art, comic and illustration learners. Practise with 30-second, 1-minute or 3-minute timers using AI-generated clothed figures or your own photos. No sign-up or session limit.'],
 'zh-TW': ['免費速寫計時器・120個人體姿勢', 'PoseToki 是為美術、漫畫與插畫學習者設計的免費人物速寫工具。用30秒、1分鐘或3分鐘計時器，觀察AI生成著衣人物或自己的照片。不需註冊，也不限練習次數。'],
}
LABELS = {
 'ko': ['학습 가이드', '포즈를 보며 한 가지씩 연습하기', '포즈 자료실', '서기·걷기·앉기 등 10개 유형의 120개 포즈와 관찰 목표를 확인하세요.', '언어별 연습실'],
 'ja': ['学習ガイド', 'ポーズを見ながら一つずつ練習する', 'ポーズ資料室', '立つ・歩く・座るなど10種類の120ポーズと観察ポイントを確認できます。', '言語別の練習室'],
 'en': ['Learning guides', 'Learn one observation skill at a time', 'Pose reference library', 'Explore 120 poses across 10 types, including standing, walking and seated figures, with observation goals.', 'Studios by language'],
 'zh-TW': ['學習指南', '看姿勢，一次練習一個觀察重點', '姿勢素材庫', '查看站姿、行走、坐姿等10種類型的120個姿勢與觀察目標。', '各語言練習室'],
}


def translations():
    # Evaluate only our checked-in dictionary declarations in an isolated VM.
    js = """const fs=require('fs'),vm=require('vm');const file=fs.readFileSync(process.argv[1],'utf8');const prefix=file.slice(file.indexOf('const dict='),file.indexOf('const langs='));const box={window:{PoseTokiPoses:[]}};vm.runInNewContext(fs.readFileSync(process.argv[2],'utf8'),box);vm.runInNewContext(prefix+';out=JSON.stringify(dict)',box);process.stdout.write(box.out);"""
    return json.loads(subprocess.check_output(['node','-e',js,str(ROOT/'dist/i18n.js'),str(ROOT/'dist/home-translations.js')],text=True))


class Localize(HTMLParser):
    def __init__(self, lang, dictionary):
        super().__init__(convert_charrefs=True); self.lang=lang; self.dictionary=dictionary; self.parts=[]; self.raw=None; self.select_id=None
    def translate(self, text):
        key=text.strip(); value=self.dictionary.get(key)
        if not value or self.lang=='ko': return text
        translated=value[COL[self.lang]] if len(value)>COL[self.lang] else value[0]
        return text.replace(key,translated or key,1)
    def handle_decl(self,decl): self.parts.append('<!'+decl+'>')
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'): self.raw=tag
        attrs=dict(attrs)
        for attr in ('aria-label','placeholder','title','alt'):
            if attrs.get(attr): attrs[attr]=self.translate(attrs[attr])
        if tag=='html': attrs.update(lang=self.lang,**{'data-site-lang':self.lang})
        if tag=='a' and attrs.get('data-localized-page'):
            attrs['href']=f'/{LANGS[self.lang]}/{attrs["data-localized-page"]}.html'+('#'+attrs['data-localized-anchor'] if attrs.get('data-localized-anchor') else '')
        if tag=='meta' and attrs.get('name')=='description': attrs['content']=self.translate(attrs['content'])
        if tag=='select': self.select_id=attrs.get('id')
        if tag=='option' and self.select_id=='language':
            attrs.pop('selected',None)
            if attrs.get('value')==self.lang: attrs['selected']=None
        for key in ('href','src'):
            value=attrs.get(key,'')
            if value and not value.startswith(('/', '#', 'https:', 'http:', 'mailto:')): attrs[key]='/'+value
        self.parts.append('<'+tag+''.join(' '+k if v is None else f' {k}="{escape(v,quote=True)}"' for k,v in attrs.items())+'>')
    def handle_endtag(self,tag):
        self.parts.append('</'+tag+'>')
        if tag==self.raw: self.raw=None
        if tag=='select': self.select_id=None
    def handle_data(self,data): self.parts.append(data if self.raw else escape(self.translate(data),quote=False))
    def handle_comment(self,data): self.parts.append('<!--'+data+'-->')


def learning(lang):
    labels=LABELS[lang];path=LANGS[lang]
    cards=''
    for slug in ('beginner','gesture','balance','seated'):
        article=DISCOVERY[lang][slug] if slug=='beginner' else LESSONS[lang][slug]
        cards+=f'<a class="learning-card" data-localized-page="{slug}" href="/{path}/{slug}.html"><strong>{escape(article["title"])}</strong><span>{escape(article["description"])}</span></a>'
    return f'<section class="learning" id="learn"><div class="section-title"><div><div class="eyebrow">{labels[0]}</div><h2>{labels[1]}</h2></div></div><div class="learning-grid">{cards}</div><a class="catalog-link" data-localized-page="poses" href="/{path}/poses.html"><strong>{labels[2]} →</strong><span>{labels[3]}</span></a></section>'


def render(lang, template, dictionary):
    parser=Localize(lang,dictionary);parser.feed(template);s=''.join(parser.parts)
    url=ORIGIN+HOME[lang]
    pose=load_poses()[0]
    s=re.sub(r'<span id="imageLabel">.*?</span>',f'<span id="imageLabel">PT001 / 120 · {escape(pose["name"][lang])}</span>',s)
    estimate={'ko':'10장 · 약 10분','ja':'10枚 · 約10分','en':'10 poses · about 10 min','zh-TW':'10 張 · 約10分鐘'}
    s=re.sub(r'<strong id="estimate">.*?</strong>',f'<strong id="estimate">{estimate[lang]}</strong>',s)
    s=re.sub(r'<h1 id="heroTitle">.*?</h1>',f'<h1 id="heroTitle">{HERO[lang]}</h1>',s,flags=re.S)
    s=re.sub(r'<link rel="canonical"[^>]*>',f'<link rel="canonical" href="{url}">',s)
    s=re.sub(r'<div class="eyebrow"><span></span>.*?</div>',f'<div class="eyebrow"><span></span>{FACTS[lang][0]}</div>',s,count=1)
    s=s.replace('<section class="guide"',learning(lang)+'<section class="guide"',1)
    s=s.replace('</section>\n<section class="workspace"',f'<p class="service-summary">{FACTS[lang][1]}</p></section>\n<section class="workspace"',1)
    names={'ko':'한국어','ja':'日本語','en':'English','zh-TW':'繁體中文'}
    links=''.join(f'<a href="{href}" hreflang="{code}" lang="{code}"'+(' aria-current="page"' if code==lang else '')+f'>{names[code]}</a>' for code,href in HOME.items())
    s=s.replace('<footer>',f'<nav class="home-languages" aria-label="{LABELS[lang][4]}">{links}</nav><footer>',1)
    title=parser.translate('무료 크로키 연습 | 120개 인체 포즈와 타이머 | 포즈토키')
    desc=parser.translate('30초·1분·3분 무료 크로키 연습. 120개 AI 생성 인체 포즈와 타이머로 동작선, 무게중심, 앉은 자세를 관찰하세요.')
    schema={'@context':'https://schema.org','@graph':[
      {'@type':'WebSite','@id':ORIGIN+'/#website','name':'PoseToki','alternateName':'포즈토키','url':ORIGIN+'/','inLanguage':list(LANGS)},
      {'@type':'WebApplication','@id':url+'#app','name':'PoseToki','url':url,'description':FACTS[lang][1],'inLanguage':lang,'applicationCategory':'EducationalApplication','operatingSystem':'Web browser','browserRequirements':'JavaScript enabled','isAccessibleForFree':True,'offers':{'@type':'Offer','price':'0','priceCurrency':'USD'},'featureList':['120 AI-generated clothed figure references','30-second, 1-minute, 3-minute and custom timers','Local photo practice without uploads','No sign-up, unlimited sessions'],'publisher':{'@type':'Person','@id':ORIGIN+'/#jeremy','name':'Jeremy','url':f'{ORIGIN}/{LANGS[lang]}/about.html#operator'}},
    ]}
    alternates=''.join(f'<link rel="alternate" hreflang="{code}" href="{ORIGIN+href}">' for code,href in HOME.items())+f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}/">'
    s=s.replace('</head>',metadata(lang,title,desc,url)+'\n'+alternates+'\n'+jsonld(schema).replace('<script type=','<script id="site-schema" type=')+'\n<link rel="preload" as="image" href="/assets/pose-01.jpg" fetchpriority="high">\n</head>',1)
    return s


def main():
    extra={}
    for i in range(2): extra[FACTS['ko'][i]]=[FACTS[lang][i] for lang in ('ko','ja','en','zh-TW')]
    for i in range(5): extra[LABELS['ko'][i]]=[LABELS[lang][i] for lang in ('ko','ja','en','zh-TW')]
    for slug in ('beginner','gesture','balance','seated'):
        source=DISCOVERY if slug=='beginner' else LESSONS
        for field in ('title','description'): extra[source['ko'][slug][field]]=[source[lang][slug][field] for lang in ('ko','ja','en','zh-TW')]
    (ROOT/'dist/home-translations.js').write_text('window.PoseTokiHomeTranslations='+json.dumps(extra,ensure_ascii=False,separators=(',',':'))+';\n')
    dictionary=translations()
    for pose in load_poses():
        for field in ('name','focus'): dictionary[pose[field]['ko']]=[pose[field][lang] for lang in ('ko','ja','en','zh-TW')]
    template=(ROOT/'templates/home.html').read_text()
    for lang,href in HOME.items():
        target=ROOT/'dist'/href.lstrip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(render(lang,template,dictionary))
    print('Built 4 crawlable language homepages')


if __name__=='__main__': main()
