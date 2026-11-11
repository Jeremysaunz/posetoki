"""Construction diagrams drawn over PoseToki's AI reference photos.

Each diagram is an <img> with an SVG overlay in the photo's own pixel space,
so the marks stay on the body at any size. Colours come from the site's
non-photo blue construction tokens in sketch-content.css.
"""
from html import escape

COLUMN = {'ko': 0, 'ja': 1, 'en': 2, 'zh-TW': 3}
WORDS = {
    'action': ('동작선', '動勢線', 'Line of action', '動勢線'),
    'head': ('머리', '頭', 'Head', '頭部'),
    'top': ('머리 꼭대기', '頭頂', 'Top of head', '頭頂'),
    'ground': ('바닥', '床', 'Floor', '地面'),
    'half': ('절반', '半分', 'Halfway', '一半'),
    'shoulder': ('어깨선', '肩の線', 'Shoulder line', '肩線'),
    'hip': ('골반선', '骨盤の線', 'Hip line', '骨盆線'),
    'centre': ('몸통 가운데', '胴体の中ほど', 'Torso centre', '軀幹中段'),
    'support': ('지지 발', '支える足', 'Supporting foot', '承重腳'),
    'ribcage': ('가슴통', '胸郭', 'Rib cage', '胸廓'),
    'pelvis': ('골반', '骨盤', 'Pelvis', '骨盆'),
    'thigh': ('앞에 있는 허벅지', '手前の太もも', 'Front thigh', '前方大腿'),
    'short': ('짧게 덧그은 선', '短く重ねた線', 'Short, layered strokes', '短線反覆疊畫'),
    'long': ('한 번에 그은 긴 선', '一度に引いた長い線', 'One long stroke', '一筆拉長的線'),
}


def word(lang, key):
    return WORDS[key][COLUMN[lang]]


def text(lang, key, x, y, anchor='start'):
    return f'<text class="d-tag" x="{x}" y="{y}" text-anchor="{anchor}">{escape(word(lang, key))}</text>'


def dot(x, y, r=9):
    return f'<circle class="d-joint" cx="{x}" cy="{y}" r="{r}"/>'


def line(x1, y1, x2, y2, cls='d-line'):
    return f'<path class="{cls}" d="M{x1} {y1}L{x2} {y2}"/>'


def ruler(top, unit, end, x=34):
    count = int((end - top) // unit)
    marks = f'<path class="d-thin" d="M{x} {top}V{end}"/>'
    for k in range(count + 1):
        y = top + unit * k
        marks += f'<path class="d-thin" d="M{x - 14} {y}h28"/>'
    marks += f'<path class="d-thin" d="M{x - 14} {end}h28"/>'
    marks += ''.join(f'<text class="d-num" x="{x}" y="{top + unit * k + unit / 2}">{k + 1}</text>' for k in range(count))
    return marks


def plumb(x, top, bottom):
    return (f'<path class="d-plumb" d="M{x} {top}V{bottom}"/>{dot(x, top, 10)}'
            f'<path class="d-bob" d="M{x - 11} {bottom}h22l-11 18z"/>')


# id: (image path, width, height, builder(lang) -> svg body)
DIAGRAMS = {
    'two-points': ('/assets/pose-01', 512, 1024, lambda l: (
        dot(232, 36, 10) + dot(240, 912, 10)
        + '<path class="d-line d-action" d="M232 46C228 250 300 470 240 902"/>'
        + text(l, 'top', 254, 42) + text(l, 'ground', 262, 930) + text(l, 'action', 316, 470))),
    'action-walk': ('/assets/pose-03', 512, 1024, lambda l: (
        '<ellipse class="d-line" cx="234" cy="96" rx="44" ry="58" transform="rotate(-6 234 96)"/>'
        + '<path class="d-line d-action" d="M238 40C214 260 222 560 256 900"/>'
        + text(l, 'head', 288, 70) + text(l, 'action', 150, 560, 'end'))),
    'halfway': ('/assets/library/PT005', 768, 1152, lambda l: (
        dot(384, 30, 11) + dot(384, 1055, 11)
        + '<path class="d-thin" d="M384 42V1043"/>'
        + '<path class="d-line" d="M330 542h108"/>'
        + text(l, 'top', 410, 40) + text(l, 'ground', 410, 1068) + text(l, 'half', 452, 552))),
    'head-ruler': ('/assets/pose-01', 512, 1024, lambda l: (
        ruler(35, 115, 915)
        + '<ellipse class="d-line" cx="232" cy="92" rx="46" ry="58" transform="rotate(-4 232 92)"/>'
        + text(l, 'head', 288, 70))),
    'tilts': ('/assets/pose-01', 512, 1024, lambda l: (
        line(118, 216, 344, 199) + dot(118, 216) + dot(344, 199)
        + line(146, 386, 324, 371) + dot(146, 386) + dot(324, 371)
        + text(l, 'shoulder', 356, 196) + text(l, 'hip', 336, 368))),
    'plumb-one-foot': ('/assets/pose-17', 512, 1024, lambda l: (
        line(80, 222, 300, 212, 'd-thin') + line(126, 430, 290, 412, 'd-thin')
        + plumb(201, 350, 880)
        + text(l, 'centre', 222, 342) + text(l, 'support', 252, 900))),
    'boxes-seated': ('/assets/pose-02', 512, 1024, lambda l: (
        '<path class="d-line" d="M168 262L354 262L336 432L188 432Z"/>'
        + '<path class="d-line" d="M188 436L330 436L338 560L176 560Z"/>'
        + '<rect class="d-line d-front" x="276" y="452" width="176" height="70" rx="35" transform="rotate(2 364 487)"/>'
        + text(l, 'ribcage', 160, 340, 'end') + text(l, 'pelvis', 168, 520, 'end') + text(l, 'thigh', 300, 444))),
}


def figure(lang, key, caption):
    path, w, h, build = DIAGRAMS[key]
    return (f'<figure class="diagram"><div class="diagram-sheet" style="aspect-ratio:{w}/{h}">'
            f'<picture><source type="image/webp" srcset="{path}.webp"><img src="{path}.jpg" width="{w}" height="{h}" loading="lazy" decoding="async" alt=""></picture>'
            f'<svg viewBox="0 0 {w} {h}" aria-hidden="true">{build(lang)}</svg></div>'
            f'<figcaption>{escape(caption)}</figcaption></figure>')


def _curve(t, y0):
    """Point on the shared demo curve, shifted to baseline y0."""
    p = ((30, y0), (160, y0 - 60), (300, y0 - 70), (420, y0 - 40))
    u = 1 - t
    return tuple(u ** 3 * p[0][i] + 3 * u * u * t * p[1][i] + 3 * u * t * t * p[2][i] + t ** 3 * p[3][i] for i in (0, 1))


def strokes(lang, caption):
    """Line-only diagram: one curve drawn as layered short strokes, then as one stroke."""
    jitter = (-5, 3, -2, 5, -4, 2, -3, 4, -1, 3, -5, 2, 0, -3)
    short = ''
    for i, dy in enumerate(jitter):
        a = _curve(i / 15, 140 + dy)
        b = _curve(min(1, i / 15 + 0.11), 140 + dy * .6)
        short += f'<path class="d-hair" d="M{a[0]:.0f} {a[1]:.0f}L{b[0]:.0f} {b[1]:.0f}"/>'
    longest = ' '.join(f'{x:.0f} {y:.0f}' for x, y in (_curve(t / 20, 290) for t in range(21)))
    return (f'<figure class="diagram diagram-wide"><div class="diagram-sheet diagram-plain" style="aspect-ratio:2/1">'
            f'<svg viewBox="0 0 640 320" aria-hidden="true">'
            f'<text class="d-tag" x="460" y="110">{escape(word(lang, "short"))}</text>{short}'
            f'<polyline class="d-line d-action" points="{longest}"/>'
            f'<text class="d-tag" x="460" y="262">{escape(word(lang, "long"))}</text>'
            f'</svg></div><figcaption>{escape(caption)}</figcaption></figure>')
