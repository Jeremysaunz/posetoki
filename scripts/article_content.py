"""Navigation, the practice-guide hub, and two long-form practice articles.

Every reader-facing string is a 4-tuple in (ko, ja, en, zh-TW) order so the
four language versions of a sentence sit side by side. Practice settings are
numbers; their labels and studio links are generated per language.
Claims in the two articles were checked against published drawing references
on 2026-11-10 (see Posetoki/drafts/00_검증기록_20261110.md).
"""
from html import escape

from diagrams import figure, strokes
from discovery_content import CATEGORY_NAMES
from seo_common import HOME, LANGS

COL = {'ko': 0, 'ja': 1, 'en': 2, 'zh-TW': 3}
ARTICLE_DATE = '2026-11-10'
ARTICLE_SLUGS = ('30-day-routine', 'common-mistakes')
HUB_SLUG = 'learn'


def pick(lang, value):
    return value[COL[lang]] if isinstance(value, tuple) else value


def T(ko, ja, en, zh):
    return (ko, ja, en, zh)


NAV = {
    'studio': T('연습실', '練習室', 'Studio', '練習室'),
    'learn': T('연습 가이드', '練習ガイド', 'Practice guides', '練習指南'),
    'poses': T('포즈 자료실', 'ポーズ資料室', 'Pose library', '姿勢素材庫'),
    'about': T('소개', '紹介', 'About', '關於'),
    'about_long': T('소개·운영 안내', '紹介・運営案内', 'About & operation', '介紹與營運說明'),
    'privacy': T('개인정보 안내', 'プライバシー', 'Privacy', '隱私說明'),
    'feedback': T('의견 보내기', '意見を送る', 'Send feedback', '提供意見'),
}

UPDATED = {
    'ko': lambda y, m, d: f'{y}년 {m}월 {d}일 업데이트',
    'ja': lambda y, m, d: f'{y}年{m}月{d}日更新',
    'en': lambda y, m, d: f'Updated {["January","February","March","April","May","June","July","August","September","October","November","December"][m-1]} {d}, {y}',
    'zh-TW': lambda y, m, d: f'{y}年{m}月{d}日更新',
}


def updated_label(lang, iso):
    y, m, d = (int(part) for part in iso.split('-'))
    return UPDATED[lang](y, m, d)


# ---------------------------------------------------------------- settings
def seconds_label(lang, s):
    if s % 60 == 0:
        n = s // 60
        return {'ko': f'{n}분', 'ja': f'{n}分', 'en': f'{n} min', 'zh-TW': f'{n}分鐘'}[lang]
    return {'ko': f'{s}초', 'ja': f'{s}秒', 'en': f'{s} sec', 'zh-TW': f'{s}秒'}[lang]


def count_label(lang, n):
    return {'ko': f'{n}장', 'ja': f'{n}枚', 'en': f'{n} poses', 'zh-TW': f'{n}張'}[lang]


ALL_POSES = T('전체', '全ポーズ', 'All poses', '全部姿勢')
OWN_PHOTOS = T('내 사진 탭', '「自分の写真」タブ', 'My photos tab', '「我的照片」分頁')
THEN = T(', 이어서 ', '、続けて', ', then ', '，接著')


def session_label(lang, s, n, cat):
    where = pick(lang, OWN_PHOTOS) if cat == 'own' else pick(lang, ALL_POSES) if cat is None else CATEGORY_NAMES[cat][COL[lang]]
    return f'{seconds_label(lang, s)} × {count_label(lang, n)} · {where}'


def studio_href(lang, s=None, n=None, cat=None):
    params = []
    if s:
        params.append(f'seconds={s}')
    if n:
        params.append(f'count={n}')
    if cat and cat != 'own':
        params.append(f'category={cat}')
    return HOME[lang] + ('?' + '&amp;'.join(params) if params else '') + '#practice'


def page_href(lang, slug):
    return f'/{LANGS[lang]}/{slug}.html'


def paragraph(lang, value):
    return f'<p>{escape(pick(lang, value))}</p>'


def rich(lang, value, links):
    """Paragraph with {slug} placeholders turned into links to other guides."""
    text = escape(pick(lang, value))
    for slug, label in links.items():
        text = text.replace('{' + slug + '}', f'<a href="{page_href(lang, slug)}">{escape(pick(lang, label))}</a>')
    return f'<p>{text}</p>'


LESSON_TITLES = {
    'gesture': T('30초 동작선: 걷는 몸의 흐름을 한 줄로', '30秒の動勢線：歩く身体の流れを一本の線で捉える', '30-second line of action: one line for a walking figure', '30 秒動勢線：用一條線抓住走路的身體流向'),
    'balance': T('1분 무게중심: 골반과 지지 발을 함께 보기', '1分の重心：骨盤と支える足を一緒に見る', '1-minute balance: read the pelvis and supporting foot together', '1 分鐘重心：同時觀察骨盆與承重腳'),
    'seated': T('3분 앉은 자세: 골반의 자리와 겹침 읽기', '3分の座りポーズ：骨盤の位置と重なりを読む', '3-minute seated pose: find the pelvis and read overlaps', '3 分鐘坐姿：讀出骨盆位置與重疊'),
    'beginner': T('크로키 초보자를 위한 10분 인체 연습법', 'クロッキー初心者のための10分人体練習', 'A 10-minute figure drawing routine for beginners', '速寫初學者的 10 分鐘人體練習法'),
    '30-day-routine': T('30일 크로키 루틴', '30日クロッキールーティン', 'the 30-day gesture drawing routine', '30 天速寫練習計畫'),
}

REFS_TITLE = T('참고 자료', '参考資料', 'References', '參考資料')
REFS_NOTE = T('이 글의 관찰 방법은 아래 자료에서 널리 가르치는 내용을 연습 순서로 묶은 것입니다. 내용 확인: 2026년 11월 10일.',
              'この記事の観察方法は、以下の資料で広く教えられている内容を練習の順番にまとめたものです。確認日：2026年11月10日。',
              'The observation methods here gather widely taught material from the sources below into a practice sequence. Checked on November 10, 2026.',
              '本文的觀察方法，是把下列資料中廣泛教授的內容整理成練習順序。確認日期：2026 年 11 月 10 日。')
AI_NOTE = T('예시 포즈 사진은 포즈토키를 위해 만든 AI 생성 이미지입니다. 인체 구조의 정답이 아니라 관찰 연습용 자료로 사용하세요. 사진 위의 파란 선은 포즈토키가 그린 관찰 도해입니다.',
            '例のポーズ写真はPoseTokiのために作成したAI生成画像です。人体構造の正解ではなく、観察練習用の資料として使ってください。写真上の青い線はPoseTokiが描いた観察図解です。',
            'Example pose photos are AI-generated images made for PoseToki. Use them as observation material, not as anatomical answers. The blue lines on the photos are observation diagrams drawn by PoseToki.',
            '示範姿勢照片是為 PoseToki 製作的 AI 生成圖像。請把它當作觀察練習素材，而不是人體結構的標準答案。照片上的藍線是 PoseToki 繪製的觀察圖解。')


def references(lang, items):
    rows = ''.join(f'<li>{escape(pick(lang, topic))}: ' + ', '.join(f'<a href="{url}" rel="noopener">{escape(title)}</a>' for title, url in links) + '</li>' for topic, links in items)
    return f'<section class="references"><h2>{escape(pick(lang, REFS_TITLE))}</h2><p>{escape(pick(lang, REFS_NOTE))}</p><ul>{rows}</ul></section>'


R_WIKI_GESTURE = ('Gesture drawing (Wikipedia)', 'https://en.wikipedia.org/wiki/Gesture_drawing')
R_DRAWINGSOURCE = ('The Line of Action (The Drawing Source)', 'https://www.thedrawingsource.com/line-of-action.html')
R_LOA = ('Gesture basics #1: Line of action (Line of Action)', 'https://line-of-action.com/article/gesture-basics-1-line-of-action/')
R_CONTRAPPOSTO = ('Contrapposto (Wikipedia)', 'https://en.wikipedia.org/wiki/Contrapposto')
R_BALANCE = ('How to Draw Balanced Poses (Proko)', 'https://www.proko.com/course-lesson/how-to-draw-balanced-poses')
R_ROBOBEAN = ('How to Draw Structure in the Body – Robo Bean (Proko)', 'https://www.proko.com/robo-bean/')
R_PROPORTIONS = ('Body proportions (Wikipedia)', 'https://en.wikipedia.org/wiki/Body_proportions')
R_MEASURE = ('Measuring Techniques (Proko)', 'https://proko.com/62')
R_PENCIL = ('How to Measure with a Pencil from Life (Life Drawing Academy)', 'https://lifedrawing.academy/life-drawing-academy-news/how-to-measure-with-a-pencil-from-life')
R_FORESHORTEN = ('Foreshortening (Wikipedia)', 'https://en.wikipedia.org/wiki/Foreshortening')
R_SHOULDER = ('Drawing From the Shoulder vs. Drawing From the Wrist (Envato Tuts+)', 'https://design.tutsplus.com/articles/drawing-from-the-shoulder-vs-drawing-from-the-wrist-pros-and-cons--cms-24173')
R_CERF = ('Cerf, Frady & Koch (2009), Faces and text attract gaze independent of the task, Journal of Vision', 'https://resolver.caltech.edu/CaltechAUTHORS:20130816-103355264')


# ---------------------------------------------------------------- 30-day routine
ROUTINE = {
    'title': T('30일 크로키 루틴: 하루 10분, 한 번에 한 가지만',
               '30日クロッキールーティン：1日10分、一度に一つだけ',
               '30-day gesture drawing routine: 10 minutes a day, one thing at a time',
               '30 天速寫練習計畫：每天 10 分鐘，一次只看一件事'),
    'description': T('하루 10분씩 30일 동안 동작선, 무게중심, 덩어리와 겹침을 차례로 익히는 무료 크로키 연습 계획. 날마다 시간·장수·포즈 유형과 관찰할 한 가지를 정리했습니다.',
                     '1日10分、30日間で動勢線・重心・量感と重なりを順に身につける無料のクロッキー練習計画。毎日の時間、枚数、ポーズの種類と観察する一点をまとめました。',
                     'A free 30-day gesture drawing plan, about 10 minutes a day, that builds the line of action, balance, then masses and overlaps. Each day lists time, pose count, pose type, and one thing to observe.',
                     '每天約 10 分鐘、為期 30 天的免費速寫練習計畫，依序練習動勢線、重心、體塊與重疊。每天都列出時間、張數、姿勢類型與一個觀察重點。'),
    'lead': T('크로키가 늘지 않는 흔한 이유는 실력이 아니라 매번 모든 것을 한꺼번에 보려 하기 때문입니다. 이 루틴은 하루에 관찰할 것 하나만 정합니다. 시간과 장수, 포즈 유형까지 정해 두었으니 표의 "시작" 링크를 눌러 바로 그리세요.',
              'クロッキーが伸びない理由としてよくあるのは、実力ではなく、毎回すべてを一度に見ようとすることです。このルーティンでは1日に観察することを一つだけ決めます。時間、枚数、ポーズの種類まで決めてあるので、表の「開始」リンクからすぐ描き始めてください。',
              'A common reason gesture drawing stalls is not skill but trying to see everything at once. This routine gives you one thing to observe each day. Time, pose count and pose type are already chosen, so tap "Start" in the table and draw.',
              '速寫遲遲沒有進步，常見原因不是能力，而是每次都想一口氣看完所有東西。這份計畫每天只定一個觀察重點。時間、張數和姿勢類型都已設定好，點表格裡的「開始」就能直接畫。'),
}
TABLE_HEAD = T(('일차', '설정', '오늘 볼 것', '확인 질문', '바로 시작'), ('日目', '設定', '今日見ること', '確認の質問', 'すぐ始める'),
               ('Day', 'Setting', 'Observe today', 'Check yourself', 'Start'), ('天數', '設定', '今天觀察', '自我檢查', '直接開始'))
START = T('시작', '開始', 'Start', '開始')
BEFORE = {
    'title': T('시작하기 전에', '始める前に', 'Before you start', '開始之前'),
    'paras': [
        T('준비물은 연필 한 자루와 아껴 쓰지 않아도 되는 종이면 됩니다. A4 복사지나 크로키북이 좋습니다. 태블릿으로 그린다면 지우개 도구를 쓰지 않기로 미리 정하세요. 지우지 않아야 다음 선이 빨라집니다.',
          '用意するのは鉛筆1本と、気兼ねなく使える紙だけです。コピー用紙やクロッキー帳が向いています。タブレットで描くなら、消しゴムツールを使わないと先に決めておきましょう。消さないほうが次の線が速くなります。',
          'All you need is a pencil and paper you will not mind using up, such as copy paper or a sketchbook. If you draw on a tablet, decide in advance not to use the eraser. Not erasing makes the next line come faster.',
          '準備一支鉛筆和不必省著用的紙就夠了，影印紙或速寫本都很適合。若用平板繪圖，先決定不使用橡皮擦工具。不擦掉，下一條線才會更快。'),
    ],
    'steps': [
        T('표에서 오늘 줄을 찾아 "시작"을 누릅니다. 연습실이 그 설정으로 열립니다.', '表で今日の行を探して「開始」を押します。練習室がその設定で開きます。', 'Find today\'s row and tap "Start". The studio opens with those settings.', '在表格中找到今天那一列，點「開始」。練習室會以該設定開啟。'),
        T('"오늘 볼 것" 한 가지만 생각하며 그립니다. 나머지는 틀려도 괜찮습니다.', '「今日見ること」だけを意識して描きます。それ以外は間違っていても構いません。', 'Draw with only "Observe today" in mind. Everything else is allowed to be wrong.', '只想著「今天觀察」那一件事來畫，其他地方畫錯也沒關係。'),
        T('끝나면 그린 종이를 모아 사진을 찍고, "확인 질문"에 한 줄로 답합니다.', '終わったら描いた紙をまとめて写真を撮り、「確認の質問」に一行で答えます。', 'When you finish, photograph the pages together and answer "Check yourself" in one line.', '結束後把畫好的紙集中拍照，用一句話回答「自我檢查」。'),
    ],
    'skip': T('빠진 날은 그냥 넘어가세요. 30일은 순서일 뿐 마감이 아닙니다. 사흘을 쉬었다면 그다음 날부터 이어 하면 됩니다.',
              '休んだ日はそのまま飛ばしてください。30日は順番であって締め切りではありません。3日休んだら、その次の日から続ければ大丈夫です。',
              'If you miss a day, just move on. Thirty days is an order, not a deadline. After three days off, pick up from the next day.',
              '漏掉的日子直接跳過就好。30 天只是順序，不是截止日期。休息了三天，就從下一天接著做。'),
}
WEEKS = [
    {
        'title': T('1주차: 큰 흐름 한 줄 (30초)', '1週目：大きな流れを一本で（30秒）', 'Week 1: one line for the big flow (30 seconds)', '第 1 週：用一條線抓大流向（30 秒）'),
        'intro': T('첫 주는 동작선만 봅니다. 동작선은 포즈 전체가 향하는 방향과 힘의 흐름을 한 줄로 요약한 선입니다. 척추와 겹칠 때도 많지만 척추를 그대로 따라 그리는 선은 아니고, 흔히 머리에서 무게를 가장 많이 받는 발 쪽으로 이어집니다. 곡선의 모양은 대개 C자, S자, 곧은 선 가운데 하나로 단순하게 잡습니다.',
                   '1週目は動勢線だけを見ます。動勢線はポーズ全体が向かう方向と力の流れを一本にまとめた線です。背骨と重なることも多いものの、背骨をそのままなぞる線ではなく、たいてい頭から最も体重を受ける足のほうへ続きます。形はC字、S字、まっすぐな線のどれかで単純に捉えます。',
                   'Week 1 is only about the line of action: one line that sums up where the whole pose is heading and how its force flows. It often runs close to the spine but is not a tracing of it, and it usually travels from the head toward the foot carrying the most weight. Keep its shape simple: a C curve, an S curve, or a straight line.',
                   '第一週只看動勢線。動勢線是用一條線概括整個姿勢的方向與力量流動。它常與脊椎很接近，但不是照著脊椎描線，通常從頭部延伸到承受最多體重的那隻腳。形狀簡化成 C 形、S 形或直線其中之一即可。'),
        'rows': [
            (1, [(30, 10, None)], T('머리 꼭대기와 발끝에 점 두 개를 먼저 찍고, 그 사이를 한 선으로 잇기', '頭頂とつま先に点を二つ打ち、その間を一本の線でつなぐ', 'Mark two dots, top of the head and the feet, then join them with one line', '先在頭頂和腳尖點兩個點，再用一條線連起來'),
             T('손과 얼굴이 없어도 어떤 자세인지 읽히나요?', '手と顔がなくても、どんな姿勢か読み取れますか。', 'Can you read the pose without hands or a face?', '沒有手和臉，也看得出是什麼姿勢嗎？')),
            (2, [(30, 10, 'ST')], T('머리 → 골반 → 바닥을 딛는 발로 내려오는 한 줄', '頭 → 骨盤 → 床を踏む足へ下りる一本の線', 'One line from the head, through the pelvis, down to the foot on the floor', '從頭部經過骨盆，往下到踩地的腳的一條線'),
             T('선이 두 발 사이가 아니라 무게를 받는 발 쪽으로 내려왔나요?', '線が両足の間ではなく、体重を受ける足のほうへ下りていますか。', 'Did the line come down toward the weight-bearing foot rather than between the feet?', '線條是往承重腳延伸，而不是落在兩腳中間嗎？')),
            (3, [(30, 10, 'WK')], T('몸통이 앞으로 기운 각도', '胴体が前に傾く角度', 'How far the torso leans forward', '軀幹往前傾的角度'),
             T('몸통을 세워 그려서 멈춰 선 사람처럼 보이지 않나요?', '胴体をまっすぐ描いて、立ち止まった人のように見えていませんか。', 'Did an upright torso make the figure look like it stopped walking?', '軀幹畫得太直，看起來像停下來的人嗎？')),
            (4, [(30, 10, 'TR')], T('몸이 C자로 휘었는지 S자로 휘었는지 구분하기', '身体がC字に曲がっているかS字かを見分ける', 'Tell a C curve from an S curve', '分辨身體是 C 形還是 S 形彎曲'),
             T('휜 방향을 사진과 반대로 그리지 않았나요?', '曲がる向きを写真と逆に描いていませんか。', 'Did you bend it the opposite way from the photo?', '有沒有把彎曲方向畫反了？')),
            (5, [(30, 15, 'DY')], T('실제보다 조금 더 휘게 과장하기', '実際より少しだけ大きく曲げて誇張する', 'Exaggerate the curve slightly beyond the photo', '比實際稍微再彎一點，誇張處理'),
             T('과장했더니 움직임이 더 잘 보이나요?', '誇張したら動きがよく見えるようになりましたか。', 'Does the movement read better with the exaggeration?', '誇張之後，動作更清楚了嗎？')),
            (6, [(60, 5, None)], T('동작선 위에 머리, 가슴통, 골반 세 덩어리 얹기', '動勢線の上に頭・胸郭・骨盤の三つの塊をのせる', 'Place three masses on the line: head, rib cage, pelvis', '在動勢線上放頭部、胸廓、骨盆三個體塊'),
             T('덩어리를 얹은 뒤에도 처음의 흐름이 살아 있나요?', '塊をのせた後も、最初の流れが残っていますか。', 'Is the first flow still alive after adding the masses?', '放上體塊後，最初的流向還在嗎？')),
            (7, [(30, 10, None)], T('복습: 한 주 동안 그린 그림 중 가장 잘 읽히는 장과 가장 안 읽히는 장 고르기', '復習：1週間の絵からいちばん読み取りやすい1枚と、いちばん読み取りにくい1枚を選ぶ', 'Review: pick the clearest and the least clear drawing from the week', '複習：從這週的畫裡挑出最容易看懂與最難看懂的各一張'),
             T('두 장의 차이는 선의 개수인가요, 방향인가요?', '2枚の違いは線の数ですか、向きですか。', 'Is the difference the number of lines, or their direction?', '兩張的差別在線條數量，還是方向？')),
        ],
        'after': T('더 자세한 설명은 {gesture}에 있습니다.', '詳しくは{gesture}をご覧ください。', 'For more detail, read {gesture}.', '更詳細的說明請看{gesture}。'),
        'diagram': ('two-points', T('1일차 방법. 머리 꼭대기와 바닥에 점 두 개를 찍고, 무게를 받는 발 쪽으로 이어지는 한 줄을 긋습니다. (PT001)',
                                     '1日目の方法。頭頂と床に点を二つ打ち、体重を受ける足へ続く一本の線を引きます。（PT001）',
                                     'Day 1: two dots for the top of the head and the floor, then one line running toward the weight-bearing foot. (PT001)',
                                     '第 1 天的方法：在頭頂與地面點兩個點，再畫一條通往承重腳的線。（PT001）')),
    },
    {
        'title': T('2주차: 무게는 어디에 실렸나 (1분)', '2週目：体重はどこにかかっているか（1分）', 'Week 2: where is the weight? (1 minute)', '第 2 週：重量落在哪裡？（1 分鐘）'),
        'intro': T('둘째 주에는 1분으로 늘리고 기울기와 무게중심을 봅니다. 서 있는 사람이 어색해 보일 때는 머리 크기보다 무게가 실린 위치가 틀린 경우가 많습니다.',
                   '2週目は1分に延ばし、傾きと重心を見ます。立っている人が不自然に見えるときは、頭の大きさより体重のかかる位置がずれていることがよくあります。',
                   'In week 2 the poses get one minute, and you look at tilts and balance. When a standing figure looks wrong, the cause is often where the weight sits, not the size of the head.',
                   '第二週延長到 1 分鐘，觀察傾斜與重心。站立的人看起來不自然時，問題常常不在頭的大小，而在重量放錯了位置。'),
        'rows': [
            (8, [(60, 10, 'ST')], T('어깨를 잇는 선과 골반을 잇는 선, 두 선의 각도 비교', '両肩を結ぶ線と骨盤を結ぶ線、二本の角度を比べる', 'Compare the angle of the shoulder line and the hip line', '比較肩線與骨盆線兩條線的角度'),
             T('두 선을 무심코 평행하게 그리지 않았나요?', '二本の線をつい平行に描いていませんか。', 'Did you draw the two lines parallel out of habit?', '有沒有不自覺把兩條線畫成平行？')),
            (9, [(60, 10, 'ST')], T('몸통 가운데에서 바닥까지 가상의 수직선 내리기', '胴体の中ほどから床まで仮の垂線を下ろす', 'Drop an imaginary vertical line from the middle of the torso to the floor', '從軀幹中段往地面放一條假想垂線'),
             T('한 다리에 무게를 실었다면 그 발 쪽으로, 두 발에 고르게 실었다면 두 발 사이로 떨어지나요?', '片脚に体重をかけていればその足の側へ、両足に均等なら両足の間へ落ちますか。', 'Does it land toward the supporting foot, or between the feet if the weight is shared?', '單腳承重時是否落向那隻腳，兩腳平均承重時是否落在兩腳之間？')),
            (10, [(60, 10, 'FP')], T('힘을 주는 방향과 몸이 기우는 방향', '力を入れる向きと身体が傾く向き', 'The direction of effort and the direction the body leans', '施力方向與身體傾斜方向'),
             T('무거운 것을 당기는데 몸이 곧게 서 있지 않나요?', '重いものを引いているのに、身体がまっすぐ立っていませんか。', 'Is the body standing straight while pulling something heavy?', '拉重物時，身體卻站得筆直嗎？')),
            (11, [(60, 10, 'WK')], T('바닥에 닿은 다리는 진하게, 뜬 다리는 가볍게', '床についた脚は濃く、浮いた脚は軽く', 'Draw the planted leg darker and the lifted leg lighter', '著地的腳畫深，懸空的腳畫淡'),
             T('선의 진하기만으로 어느 발이 땅에 있는지 보이나요?', '線の濃さだけで、どちらの足が地面にあるか分かりますか。', 'Can you tell which foot is down from line weight alone?', '只看線條深淺，就看得出哪隻腳著地嗎？')),
            (12, [(60, 10, 'DA')], T('가방·우산·컵 같은 물건의 무게가 몸을 당기는 쪽', 'かばん・傘・カップなどの重さが身体を引く向き', 'Which way the weight of a bag, umbrella or cup pulls the body', '包包、雨傘、杯子等物品的重量把身體拉向哪邊'),
             T('물건을 빼고 봐도 무언가를 들고 있는 것처럼 보이나요?', '物を隠しても、何かを持っているように見えますか。', 'Without the object, does the figure still look like it is holding something?', '把物品遮住，看起來仍像拿著東西嗎？')),
            (13, [(60, 10, 'EM')], T('감정을 얼굴이 아니라 어깨와 가슴의 방향으로 읽기', '感情を顔ではなく肩と胸の向きで読む', 'Read emotion from the shoulders and chest, not the face', '從肩膀與胸口的方向讀情緒，而不是從臉'),
             T('얼굴을 가려도 감정이 전해지나요?', '顔を隠しても感情が伝わりますか。', 'Does the emotion come through with the face covered?', '遮住臉，情緒還傳達得出來嗎？')),
            (14, [(30, 5, None), (60, 5, None)], T('복습: 같은 시간 안에 1주차의 흐름과 2주차의 기울기를 함께', '復習：同じ時間内に1週目の流れと2週目の傾きを一緒に', 'Review: put week 1\'s flow and week 2\'s tilts into the same drawing', '複習：在同樣時間內同時畫出第一週的流向與第二週的傾斜'),
             T('30초 그림에도 어깨·골반 기울기가 들어갔나요?', '30秒の絵にも肩と骨盤の傾きが入りましたか。', 'Do the 30-second drawings include the shoulder and hip tilts too?', '30 秒的畫裡也有肩膀與骨盆的傾斜嗎？')),
        ],
        'after': T('{balance}에서 같은 관찰을 사진 한 장으로 자세히 설명합니다.', '{balance}で同じ観察を写真1枚で詳しく説明しています。', '{balance} walks through the same observation on one photo.', '{balance}以一張照片詳細說明同樣的觀察。'),
    },
    {
        'title': T('3주차: 덩어리와 겹침 (3분)', '3週目：塊と重なり（3分）', 'Week 3: masses and overlaps (3 minutes)', '第 3 週：體塊與重疊（3 分鐘）'),
        'intro': T('셋째 주는 3분입니다. 시간이 길어지면 윤곽선을 따라 그리고 싶어지는데, 이번 주에는 반대로 몸을 상자와 원통 같은 덩어리로 보고 무엇이 앞에 있는지를 봅니다.',
                   '3週目は3分です。時間が長くなると輪郭線をなぞりたくなりますが、今週は逆に身体を箱や円柱のような塊として見て、何が手前にあるかを見ます。',
                   'Week 3 uses three-minute poses. Longer time tempts you to trace outlines; this week, do the opposite and see the body as boxes and cylinders, and notice what sits in front.',
                   '第三週是 3 分鐘。時間一長就容易想沿著輪廓描，這週反過來，把身體看成箱子和圓柱般的體塊，觀察哪個部分在前面。'),
        'rows': [
            (15, [(180, 5, 'CH')], T('골반이 의자에 닿는 면, 앞으로 나온 허벅지가 짧아 보이는 정도', '骨盤が椅子に触れる面と、手前に出た太ももが短く見える度合い', 'Where the pelvis meets the seat, and how short a thigh looks when it points toward you', '骨盆接觸椅面的位置，以及朝前的大腿看起來縮短多少'),
             T('허벅지를 선 자세의 길이로 그리지 않았나요?', '太ももを立ちポーズの長さで描いていませんか。', 'Did you draw the thigh at its standing length?', '有沒有把大腿畫成站姿時的長度？')),
            (16, [(180, 5, 'FL')], T('겹친 두 다리 중 앞에 있는 다리의 외곽선을 끊기지 않게', '重なった2本の脚のうち、手前の脚の輪郭を途切れさせない', 'Keep the outline of the front leg unbroken where the legs overlap', '兩腿重疊時，讓前面那條腿的輪廓不要中斷'),
             T('뒤쪽 다리 선이 앞 다리를 가로질러 지나가지 않나요?', '奥の脚の線が手前の脚を横切っていませんか。', 'Does the back leg\'s line cut across the front leg?', '後面那條腿的線有沒有穿過前腿？')),
            (17, [(180, 5, 'LY')], T('머리 대신 바닥에 닿은 골반과 어깨부터 시작하기', '頭ではなく、床に触れている骨盤と肩から描き始める', 'Start with the pelvis and shoulders touching the floor, not the head', '不從頭開始，先畫貼地的骨盆與肩膀'),
             T('몸이 바닥 위에 떠 있지 않고 눌려 있나요?', '身体が床から浮かずに、押しつけられて見えますか。', 'Does the body rest its weight on the floor instead of floating?', '身體是壓在地面上，而不是浮在上面嗎？')),
            (18, [(180, 5, 'TR')], T('가슴통과 골반을 서로 다른 방향의 상자로 그리기', '胸郭と骨盤を、向きの違う箱として描く', 'Draw the rib cage and pelvis as boxes facing different ways', '把胸廓和骨盆畫成朝向不同的兩個箱子'),
             T('두 상자가 같은 쪽을 보고 있지 않나요?', '二つの箱が同じ方向を向いていませんか。', 'Are both boxes facing the same way?', '兩個箱子是不是朝同一邊？')),
            (19, [(180, 5, 'DY')], T('머리 길이를 자로 삼아 팔과 다리 길이 재기', '頭の長さを物差しにして腕と脚の長さを測る', 'Use the head length as a ruler for the arms and legs', '以頭長當尺，量手臂與腿的長度'),
             T('뻗은 팔이 머리 몇 개 길이인지 사진과 비교했나요?', '伸ばした腕が頭いくつ分か、写真と比べましたか。', 'Did you compare how many heads long the reaching arm is?', '有沒有對照照片，看伸出的手臂有幾個頭長？')),
            (20, [(180, 5, None)], T('손을 벙어리장갑 모양, 발을 쐐기 모양으로 단순하게', '手はミトン、足はくさび形に単純化する', 'Simplify hands to mittens and feet to wedges', '把手簡化成連指手套、腳簡化成楔形'),
             T('손가락을 그리다 시간이 끝나지 않았나요?', '指を描いているうちに時間切れになっていませんか。', 'Did time run out while you were drawing fingers?', '有沒有畫手指畫到時間結束？')),
            (21, [(60, 10, None)], T('복습: 3분 동안 배운 덩어리를 1분 안에 넣기', '復習：3分で学んだ塊を1分の中に入れる', 'Review: fit the three-minute masses into one minute', '複習：把 3 分鐘學到的體塊放進 1 分鐘裡'),
             T('1분 그림에도 가슴통과 골반의 방향이 보이나요?', '1分の絵にも胸郭と骨盤の向きが見えますか。', 'Can you see the rib cage and pelvis directions in one-minute drawings?', '1 分鐘的畫裡也看得出胸廓與骨盆的方向嗎？')),
        ],
        'after': T('앉은 자세는 {seated}를 함께 보면 좋습니다.', '座りポーズは{seated}も合わせて読むと役立ちます。', 'For seated poses, read {seated} alongside this week.', '坐姿可以搭配{seated}一起看。'),
        'diagram': ('boxes-seated', T('3주차 방법. 가슴통과 골반을 상자로, 앞에 있는 허벅지를 원통으로 놓습니다. 앞 허벅지의 윤곽은 끊기지 않게 그립니다. (PT049)',
                                       '3週目の方法。胸郭と骨盤を箱、手前の太ももを円柱として置きます。手前の太ももの輪郭は途切れさせません。（PT049）',
                                       'Week 3: boxes for the rib cage and pelvis, a cylinder for the front thigh, whose outline stays unbroken. (PT049)',
                                       '第 3 週的方法：把胸廓與骨盆當作箱子，前方大腿當作圓柱，前方大腿的輪廓不中斷。（PT049）')),
    },
    {
        'title': T('4주차: 섞고, 뒤집고, 내 사진으로', '4週目：混ぜる、反転する、自分の写真で', 'Week 4: mix, flip, and use your own photos', '第 4 週：混合、翻轉、用自己的照片'),
        'intro': T('마지막 주에는 지금까지 익힌 것을 다른 조건에서 써 봅니다. 같은 구조라도 시간이나 방향이 바뀌면 새로 보입니다.',
                   '最後の週は、これまで身につけたことを別の条件で使ってみます。同じ構造でも、時間や向きが変わると新しく見えてきます。',
                   'The last week applies everything under new conditions. The same structure looks new when the time or direction changes.',
                   '最後一週，在不同條件下運用目前學到的東西。同樣的結構，換了時間或方向就會看到新的東西。'),
        'rows': [
            (22, [(30, 10, 'ST'), (180, 3, 'ST')], T('같은 유형을 짧게 많이, 길게 적게 그려 비교하기', '同じ種類を短く多く、長く少なく描いて比べる', 'Draw the same type short and many, then long and few, and compare', '同一類型先短時間畫多張，再長時間畫少張，互相比較'),
             T('3분 그림이 30초 그림보다 흐름을 잃지 않았나요?', '3分の絵が30秒の絵より流れを失っていませんか。', 'Did the three-minute drawings lose the flow the 30-second ones had?', '3 分鐘的畫有沒有比 30 秒的畫失去流向？')),
            (23, [(60, 10, None)], T('난이도를 고급으로 바꾸고, 첫 10초는 동작선 하나만', '難易度を上級に変え、最初の10秒は動勢線だけ', 'Switch the level to advanced; spend the first 10 seconds on the line of action only', '把難度改成進階，前 10 秒只畫動勢線'),
             T('복잡한 포즈일수록 큰 흐름이 먼저 나왔나요?', '複雑なポーズほど、大きな流れが先に出ましたか。', 'The harder the pose, did the big flow still come first?', '姿勢越複雜，大流向是否仍先畫出來？')),
            (24, [(45, 15, None)], T('익숙하지 않은 시간으로 리듬 바꾸기', '慣れない時間でリズムを変える', 'Change your rhythm with an unfamiliar time', '用不熟悉的時間改變節奏'),
             T('시간이 애매할 때 무엇을 먼저 포기했나요?', '時間が中途半端なとき、何を先にあきらめましたか。', 'With an awkward time limit, what did you drop first?', '時間不上不下時，你先放棄了什麼？')),
            (25, [(180, 5, 'own')], T('가족, 친구, 거울 속 내 모습 사진으로 그리기', '家族、友人、鏡に映った自分の写真で描く', 'Draw from photos of family, friends, or yourself in a mirror', '用家人、朋友或鏡中自己的照片來畫'),
             T('준비된 포즈와 비교해 무엇이 더 어려웠나요?', '用意されたポーズと比べて、何が難しかったですか。', 'Compared with the prepared poses, what was harder?', '和準備好的姿勢相比，什麼比較難？')),
            (26, [(60, 10, None)], T('한 장 끝날 때마다 좌우 반전으로 같은 포즈를 한 번 더', '1枚終わるごとに左右反転して同じポーズをもう一度', 'After each pose, flip it and draw it again', '每畫完一張就左右翻轉，再畫一次同一姿勢'),
             T('반전했을 때 내 그림의 기울기 실수가 드러나나요?', '反転したとき、自分の絵の傾きのずれが見えましたか。', 'Did flipping reveal tilt mistakes in your drawing?', '翻轉後，有沒有看出自己畫的傾斜錯誤？')),
            (27, [(180, 5, 'EM')], T('포즈마다 한 줄 대사를 붙이고 그 대사가 보이게 그리기', 'ポーズごとに一行のセリフを付け、それが伝わるように描く', 'Give each pose one line of dialogue and draw so it shows', '替每個姿勢配一句台詞，並畫得讓人看出那句台詞'),
             T('대사를 가려도 장면이 상상되나요?', 'セリフを隠しても場面が想像できますか。', 'Can you imagine the scene with the dialogue hidden?', '遮住台詞，還能想像出場景嗎？')),
            (28, [(60, 10, None)], T('복습: 4주 동안 그린 그림을 날짜순으로 늘어놓기', '復習：4週間の絵を日付順に並べる', 'Review: lay out four weeks of drawings in date order', '複習：把四週的畫依日期排開'),
             T('가장 많이 달라진 것은 선, 비례, 기울기 중 무엇인가요?', 'いちばん変わったのは線、比率、傾きのどれですか。', 'What changed most: lines, proportions, or tilts?', '變化最大的是線條、比例還是傾斜？')),
        ],
        'after': T('25일차의 사진은 연습실의 "내 사진" 탭에서 고릅니다. 사진은 서버로 보내지지 않고 지금 쓰는 기기 안에서만 사용됩니다. 26일차의 좌우 반전은 연습 화면의 "좌우 반전" 버튼이나 M 키를 쓰면 됩니다.',
                   '25日目の写真は練習室の「自分の写真」タブで選びます。写真はサーバーに送られず、使っている端末の中だけで使われます。26日目の左右反転は、練習画面の「左右反転」ボタンかMキーで行えます。',
                   'For day 25, choose photos in the studio\'s "My photos" tab. They are never uploaded and stay on your device. For day 26, use the "Mirror" button or the M key in the practice screen.',
                   '第 25 天的照片請在練習室的「我的照片」分頁選擇。照片不會傳到伺服器，只在目前使用的裝置中使用。第 26 天的左右翻轉，可用練習畫面的「左右翻轉」按鈕或 M 鍵。'),
    },
]
FINAL = {
    'title': T('29~30일차: 첫날과 나란히 놓기', '29〜30日目：初日と並べる', 'Days 29–30: put day 1 beside today', '第 29～30 天：和第一天並排比較'),
    'day29': T('1일차와 똑같은 설정으로 다시 그립니다. 끝난 뒤 나오는 복습 화면의 "다음 연습에서 볼 한 가지"에서 동작선·무게중심·겹침과 비례 가운데 가장 약했던 것을 골라 두세요.',
               '1日目とまったく同じ設定でもう一度描きます。終わった後の復習画面にある「次の練習で見ること」で、動勢線・重心・重なりと比率のうち最も弱かったものを選んでおきましょう。',
               'Draw again with exactly the day 1 settings. On the review screen that follows, use "One thing to watch next time" to choose your weakest area: line of action, balance, or overlap and proportion.',
               '用和第 1 天完全相同的設定再畫一次。結束後的複習畫面中，在「下次練習要看的一件事」裡，從動勢線、重心、重疊與比例中選出最弱的一項。'),
    'day30': T('그리지 않는 날입니다. 1일차와 29일차 그림을 나란히 놓고 아래 표를 종이에 옮겨 채워 보세요. 고른 목표는 연습실의 "내 연습 기록"에서 다시 볼 수 있습니다.',
               '描かない日です。1日目と29日目の絵を並べ、下の表を紙に写して埋めてみましょう。選んだ目標は練習室の「練習記録」で見返せます。',
               'A day without drawing. Put the day 1 and day 29 drawings side by side, copy the table below onto paper, and fill it in. The goal you chose appears again in the studio\'s practice log.',
               '這天不畫畫。把第 1 天和第 29 天的畫並排，把下表抄到紙上填寫。選好的目標可以在練習室的「練習紀錄」再次查看。'),
    'compare_head': T(('확인할 것', '1일차', '29일차'), ('確認すること', '1日目', '29日目'), ('Check', 'Day 1', 'Day 29'), ('檢查項目', '第 1 天', '第 29 天')),
    'compare_rows': [
        T('가장 먼저 그은 것은?', '最初に描いたものは？', 'What did you draw first?', '最先畫的是什麼？'),
        T('머리부터 발까지 종이 안에 들어왔나?', '頭から足まで紙に収まったか？', 'Did head to feet fit on the page?', '從頭到腳都在紙內嗎？'),
        T('무게를 받는 발이 어느 쪽인지 보이나?', '体重を受ける足がどちらか見えるか？', 'Can you see which foot carries the weight?', '看得出哪隻腳承重嗎？'),
        T('한 장을 끝낼 때 시간이 모자랐나?', '1枚を終えるとき時間が足りなかったか？', 'Did you run out of time on each pose?', '每張畫完時時間不夠嗎？'),
    ],
    'close': T('비교할 때는 잘 그렸는지가 아니라 무엇을 먼저 보게 됐는지를 봅니다. 1일차에는 얼굴부터 그렸는데 29일차에는 동작선부터 그었다면 이 루틴은 제 몫을 한 것입니다.',
               '比べるときは、上手に描けたかではなく、何を先に見るようになったかを見ます。1日目は顔から描いていたのに29日目は動勢線から引いていたなら、このルーティンは役目を果たしています。',
               'When you compare, look at what you now notice first, not at how good the drawing is. If day 1 started with the face and day 29 started with the line of action, the routine has done its job.',
               '比較時看的不是畫得好不好，而是你先看到了什麼。若第 1 天從臉開始畫，第 29 天卻先拉出動勢線，這份計畫就達到目的了。'),
}
AFTER30 = {
    'title': T('30일 뒤에는', '30日の後は', 'After 30 days', '30 天之後'),
    'items': [
        T('같은 루틴을 한 번 더 돌리되, 1주차를 1분으로, 3주차를 5분으로 늘려 보세요.', '同じルーティンをもう一度回し、1週目を1分、3週目を5分に延ばしてみましょう。', 'Run the routine again with week 1 at one minute and week 3 at five minutes.', '再跑一次同樣的計畫，把第一週改成 1 分鐘、第三週改成 5 分鐘。'),
        T('가장 약했던 주의 표만 일주일 더 반복해도 됩니다.', 'いちばん弱かった週の表だけを、もう1週間繰り返しても構いません。', 'Or repeat only your weakest week for another seven days.', '也可以只把最弱那一週的表格再重複一週。'),
        T('어디서부터 볼지 막막하다면 {beginner}부터 읽어 보세요.', 'どこから見ればよいか分からなければ、{beginner}から読んでみてください。', 'If you are not sure where to begin, start with {beginner}.', '不知道從哪裡開始看，可以先讀{beginner}。'),
        T('그리다가 같은 문제가 반복되면 {common-mistakes}에서 원인과 고치는 순서를 찾아보세요.', '描いていて同じ問題が繰り返すなら、{common-mistakes}で原因と直す順番を探してみましょう。', 'If the same problem keeps coming back, look it up in {common-mistakes}.', '畫的時候同樣問題一再出現，可以到{common-mistakes}找原因與修正順序。'),
    ],
}
ROUTINE_REFS = [
    (T('짧은 포즈로 시작해 긴 포즈로 넘어가는 구성', '短いポーズから長いポーズへ移る構成', 'Moving from short to longer poses', '從短姿勢進到長姿勢的安排'), [R_WIKI_GESTURE]),
    (T('동작선의 정의와 C·S 곡선', '動勢線の定義とC・S曲線', 'Line of action and C/S curves', '動勢線的定義與 C、S 曲線'), [R_DRAWINGSOURCE, R_LOA]),
    (T('어깨선과 골반선의 반대 기울기', '肩と骨盤の逆の傾き', 'Opposite tilt of shoulders and hips', '肩與骨盆的反向傾斜'), [R_CONTRAPPOSTO]),
    (T('무게중심선과 지지 발', '重心線と支える足', 'Balance line and supporting foot', '重心線與承重腳'), [R_BALANCE]),
    (T('가슴통·골반을 상자로 단순화', '胸郭・骨盤を箱で単純化', 'Simplifying rib cage and pelvis as boxes', '把胸廓與骨盆簡化成箱子'), [R_ROBOBEAN]),
    (T('머리 길이로 비례 재기', '頭の長さで比率を測る', 'Measuring proportion in head lengths', '以頭長測量比例'), [R_PROPORTIONS, R_MEASURE]),
    (T('단축법', '短縮法', 'Foreshortening', '透視縮短'), [R_FORESHORTEN]),
]

COMMON_LINKS = {
    'gesture': LESSON_TITLES['gesture'], 'balance': LESSON_TITLES['balance'], 'seated': LESSON_TITLES['seated'],
    'beginner': LESSON_TITLES['beginner'], '30-day-routine': LESSON_TITLES['30-day-routine'],
    'common-mistakes': T('크로키가 어색해지는 7가지 이유', 'クロッキーが不自然になる7つの理由', 'seven reasons gesture drawings look off', '速寫看起來不自然的 7 個原因'),
}


def table(lang, head, rows_html):
    cells = ''.join(f'<th scope="col">{escape(h)}</th>' for h in pick(lang, head))
    return f'<div class="table-scroll"><table class="routine-table"><thead><tr>{cells}</tr></thead><tbody>{rows_html}</tbody></table></div>'


def routine_row(lang, day, sessions, focus, question):
    setting = escape(pick(lang, THEN).join(session_label(lang, *s) for s in sessions))
    s, n, cat = sessions[0]
    link = f'<a class="start-link" href="{studio_href(lang, s, n, cat)}">{escape(pick(lang, START))}</a>'
    return (f'<tr><th scope="row">{day}</th><td>{setting}</td><td>{escape(pick(lang, focus))}</td>'
            f'<td>{escape(pick(lang, question))}</td><td>{link}</td></tr>')


def render_routine(lang):
    out = [f'<section><h2>{escape(pick(lang, BEFORE["title"]))}</h2>']
    out += [paragraph(lang, p) for p in BEFORE['paras']]
    out.append('<ol>' + ''.join(f'<li>{escape(pick(lang, s))}</li>' for s in BEFORE['steps']) + '</ol>')
    out.append(paragraph(lang, BEFORE['skip']) + '</section>')
    for week in WEEKS:
        rows = ''.join(routine_row(lang, *row) for row in week['rows'])
        block = f'<section><h2>{escape(pick(lang, week["title"]))}</h2>{paragraph(lang, week["intro"])}'
        if 'diagram' in week:
            key, caption = week['diagram']
            block += figure(lang, key, pick(lang, caption))
        block += table(lang, TABLE_HEAD, rows) + rich(lang, week['after'], COMMON_LINKS) + '</section>'
        out.append(block)
    head29 = pick(lang, TABLE_HEAD)
    final_rows = (f'<tr><th scope="row">29</th><td>{escape(session_label(lang, 30, 10, None))}</td><td colspan="2">{escape(pick(lang, FINAL["day29"]))}</td>'
                  f'<td><a class="start-link" href="{studio_href(lang, 30, 10)}">{escape(pick(lang, START))}</a></td></tr>'
                  f'<tr><th scope="row">30</th><td>—</td><td colspan="2">{escape(pick(lang, FINAL["day30"]))}</td><td>—</td></tr>')
    compare_cells = ''.join(f'<th scope="col">{escape(h)}</th>' for h in pick(lang, FINAL['compare_head']))
    compare_rows = ''.join(f'<tr><th scope="row">{escape(pick(lang, r))}</th><td></td><td></td></tr>' for r in FINAL['compare_rows'])
    out.append(f'<section><h2>{escape(pick(lang, FINAL["title"]))}</h2>'
               f'<div class="table-scroll"><table class="routine-table"><thead><tr><th scope="col">{escape(head29[0])}</th><th scope="col">{escape(head29[1])}</th><th scope="col" colspan="2">{escape(head29[2])}</th><th scope="col">{escape(head29[4])}</th></tr></thead><tbody>{final_rows}</tbody></table></div>'
               f'<div class="table-scroll"><table class="compare-table"><thead><tr>{compare_cells}</tr></thead><tbody>{compare_rows}</tbody></table></div>'
               f'{paragraph(lang, FINAL["close"])}</section>')
    items = ''.join(rich(lang, item, COMMON_LINKS).replace('<p>', '<li>').replace('</p>', '</li>') for item in AFTER30['items'])
    out.append(f'<section><h2>{escape(pick(lang, AFTER30["title"]))}</h2><ul>{items}</ul></section>')
    out.append(references(lang, ROUTINE_REFS))
    out.append(f'<p class="source-note">{escape(pick(lang, AI_NOTE))}</p>')
    return ''.join(out)


# ---------------------------------------------------------------- common mistakes
MISTAKES = {
    'title': T('크로키가 어색해지는 7가지 이유와 고치는 법', 'クロッキーが不自然になる7つの理由と直し方',
               'Seven reasons gesture drawings look off, and how to fix them', '速寫看起來不自然的 7 個原因與修正方法'),
    'description': T('머리가 커지고, 발이 종이 밖으로 나가고, 서 있는 사람이 넘어질 것 같다면. 크로키에서 자주 생기는 7가지 실수의 원인과 바로 해 볼 수 있는 수정 연습을 정리했습니다.',
                     '頭が大きくなる、足が紙からはみ出す、立っている人が倒れそうに見える。クロッキーでよく起こる7つのミスの原因と、すぐ試せる修正練習をまとめました。',
                     'Heads too big, feet running off the page, standing figures about to tip over: the causes of seven common gesture drawing mistakes, with fixes you can practise right away.',
                     '頭越畫越大、腳跑出紙外、站著的人好像要倒下？整理了速寫常見的 7 種錯誤原因，以及可以立刻練習的修正方法。'),
    'lead': T('크로키를 몇 번 해 보면 그림이 비슷한 방식으로 어색해진다는 것을 알게 됩니다. 다행히 그 실수에는 대부분 이유가 있고, 고치는 순서가 있습니다. 일곱 가지를 한 번에 다 고치려 하지 말고, 내 그림에서 가장 자주 보이는 것 하나를 골라 그 항목의 연습만 일주일 해 보세요.',
              'クロッキーを何度か描くと、絵が似たような形で不自然になることに気づきます。幸い、そのミスのほとんどには理由があり、直す順番があります。7つを一度に直そうとせず、自分の絵でいちばんよく見かけるものを一つ選び、その項目の練習だけを1週間続けてみてください。',
              'After a few sessions you notice your drawings go wrong in familiar ways. Most of those mistakes have a cause and an order of repair. Do not try to fix all seven at once: pick the one you see most often and practise only that for a week.',
              '畫過幾次速寫就會發現，畫面總是以相似的方式變得不自然。好在這些錯誤大多有原因，也有修正的順序。不要一次修正七個，選出自己畫裡最常見的一個，只針對那一項練習一週。'),
}
SYMPTOM = T('이런 그림이 됩니다.', 'こんな絵になります。', 'What it looks like.', '畫面會變成這樣。')
CAUSE = T('왜 생기나요.', 'なぜ起こるのか。', 'Why it happens.', '為什麼會發生。')
FIX = T('이렇게 고칩니다.', 'こう直します。', 'How to fix it.', '這樣修正。')
PRACTICE = T('연습', '練習', 'Practice', '練習')
ITEMS = [
    {
        'title': T('얼굴을 그리다가 시간이 끝난다', '顔を描いているうちに時間が終わる', 'Time runs out while you draw the face', '畫臉畫到時間結束'),
        'symptom': T('머리와 어깨는 그럴듯한데 몸통 아래가 비어 있습니다. 30초처럼 짧은 그림에서 특히 자주 생깁니다.', '頭と肩はそれらしいのに、胴体から下が空っぽです。30秒のような短い絵で特によく起こります。', 'The head and shoulders look fine but everything below the torso is missing. It happens most in short poses such as 30 seconds.', '頭和肩膀畫得有模有樣，軀幹以下卻是空的。在 30 秒這種短時間的畫裡特別常見。'),
        'cause': T('사람이 담긴 장면을 보면 시선이 얼굴로 먼저, 그리고 자주 향합니다. 시선 추적 연구에서도 여러 번 확인된 경향입니다. 게다가 얼굴은 작은 면적에 그릴 것이 많아 시간이 빨리 지나갑니다.', '人が写った場面を見ると、視線はまず顔に、しかも何度も向かいます。視線追跡の研究でも繰り返し確かめられている傾向です。しかも顔は小さな面積に描くものが多く、時間がすぐに過ぎます。', 'When we look at a scene with people, our eyes go to faces first and often. Eye-tracking studies have shown this repeatedly. Faces also pack a lot to draw into a small area, so time disappears.', '看到有人的畫面時，視線會先、而且經常落在臉上。眼動追蹤研究也多次證實這種傾向。加上臉在小面積裡有很多要畫的東西，時間很快就過去了。'),
        'fixes': [T('30초와 1분 그림에서는 얼굴을 그리지 않기로 정합니다. 머리는 달걀 모양 하나면 충분합니다.', '30秒と1分の絵では顔を描かないと決めます。頭は卵形一つで十分です。', 'Decide not to draw faces in 30-second and one-minute poses. An egg shape is enough for the head.', '在 30 秒和 1 分鐘的畫裡，決定不畫臉。頭部畫一個蛋形就夠了。'),
                  T('첫 5초 안에 머리에서 발까지 이어지는 선 하나를 먼저 긋습니다. 이 선이 있으면 시간이 끝나도 자세는 남습니다.', '最初の5秒で頭から足まで続く線を一本引きます。この線があれば、時間が終わっても姿勢は残ります。', 'In the first five seconds, draw one line from head to feet. With that line on the page, the pose survives even if time runs out.', '在最初 5 秒內先畫出一條從頭到腳的線。有了這條線，就算時間結束，姿勢也留得下來。')],
        'practice': (30, 10, None),
        'diagram': ('action-walk', T('머리는 타원 하나, 그다음 바로 발까지 이어지는 동작선 한 줄. 얼굴은 그리지 않습니다. (PT013)', '頭は楕円一つ、すぐに足まで続く動勢線を一本。顔は描きません。（PT013）', 'One oval for the head, then straight away one line of action to the feet. No face. (PT013)', '頭部一個橢圓，接著立刻畫出通到腳的一條動勢線，不畫臉。（PT013）')),
    },
    {
        'title': T('그릴수록 아래로 커져서 발이 종이 밖으로 나간다', '描くほど下に大きくなり、足が紙からはみ出す', 'The figure grows as you go down and the feet fall off the page', '越往下畫越大，腳跑出紙外'),
        'symptom': T('머리는 종이 위쪽에 잘 자리 잡았는데, 다리를 그릴 즈음 종이가 모자랍니다. 결국 발목에서 잘리거나 다리가 짧아집니다.', '頭は紙の上にうまく収まったのに、脚を描くころには紙が足りません。結局、足首で切れるか脚が短くなります。', 'The head sits nicely near the top of the page, but by the legs you run out of paper. The feet get cut off or the legs shrink.', '頭部好好放在紙的上方，畫到腿時紙卻不夠了，結果腳踝被切掉，或腿變短。'),
        'cause': T('위에서부터 차례로 그리면서 각 부분을 조금씩 크게 그리고, 그 오차가 아래로 쌓이기 때문입니다. 미술 강좌에서도 대표적인 초보 실수로 꼽습니다.', '上から順に描きながら各部分を少しずつ大きく描き、その誤差が下に積み重なるからです。美術講座でも代表的な初心者のミスとして挙げられます。', 'Drawing from the top down, each part comes out slightly too big and the errors pile up toward the bottom. Drawing courses list it as a classic beginner mistake.', '從上往下依序畫時，每個部位都畫大了一點，誤差一路往下累積。美術課程也把它列為代表性的初學者錯誤。'),
        'fixes': [T('선을 긋기 전에 종이에 점 두 개를 먼저 찍습니다. 머리 꼭대기 자리 하나, 발이 닿을 바닥 자리 하나입니다.', '線を引く前に、紙に点を二つ打ちます。頭頂の位置と、足が触れる床の位置です。', 'Before any line, mark two dots: one for the top of the head, one for where the feet meet the floor.', '畫線前先在紙上點兩個點：一個是頭頂，一個是腳踩到的地面。'),
                  T('그다음 두 점의 중간에 무엇이 오는지 사진에서 확인합니다. 곧게 선 사람이라면 대개 허리가 아니라 골반 아래쪽, 사타구니 높이입니다.', '次に、二つの点の真ん中に何が来るか写真で確かめます。まっすぐ立った人なら、たいてい腰ではなく骨盤の下側、股の高さです。', 'Then check what falls halfway between the dots. For an upright figure it is usually not the waist but the lower pelvis, around the crotch.', '接著在照片上確認兩點正中間是什麼。站直的人通常不是腰，而是骨盆下方、胯下的高度。')],
        'practice': (30, 10, 'ST'),
        'diagram': ('halfway', T('머리 꼭대기와 바닥에 점을 찍으면 그 중간은 사타구니 근처에 옵니다. (PT005)', '頭頂と床に点を打つと、その真ん中は股のあたりに来ます。（PT005）', 'With dots at the top of the head and the floor, halfway lands near the crotch. (PT005)', '在頭頂和地面點上點，正中間大約落在胯下附近。（PT005）')),
    },
    {
        'title': T('머리가 너무 크다', '頭が大きすぎる', 'The head is too big', '頭太大'),
        'symptom': T('몸이 어린아이나 캐릭터처럼 보입니다. 사진대로 그렸다고 느끼는데 나란히 두면 머리가 확연히 큽니다.', '身体が子どもやキャラクターのように見えます。写真どおりに描いたつもりでも、並べると頭がはっきり大きいのです。', 'The figure looks like a child or a cartoon character. It feels faithful to the photo, but side by side the head is clearly larger.', '身體看起來像小孩或卡通角色。自以為照著照片畫，並排一看頭明顯偏大。'),
        'cause': T('얼굴에 관심이 많아 머리를 실제보다 크게 기억하기 때문입니다. 1번 실수와 뿌리가 같습니다.', '顔に関心が向くため、頭を実際より大きく覚えてしまうからです。1つ目のミスと根は同じです。', 'Attention on the face makes us remember the head as bigger than it is. It shares a root with mistake 1.', '因為注意力集中在臉上，把頭記得比實際大。和第 1 個錯誤同一個根源。'),
        'fixes': [T('머리 길이를 자로 씁니다. 사진에서 머리 꼭대기부터 턱까지를 한 칸으로 보고, 몸 전체가 몇 칸인지 셉니다.', '頭の長さを物差しにします。写真で頭頂からあごまでを1つ分とし、全身がいくつ分かを数えます。', 'Use the head as a ruler. Count the distance from the top of the head to the chin as one unit and see how many units the whole body is.', '把頭長當尺。把照片中頭頂到下巴視為一格，數全身有幾格。'),
                  T('미술 교재에서는 보통 사람을 7.5칸 정도, 이상화한 인물을 8칸으로 설명합니다. 다만 이 수치도 관례일 뿐이어서 숫자를 외우기보다 그 사진에서 직접 세는 것이 정확합니다. 몸을 숙이거나 앉으면 칸 수가 크게 달라집니다.', '美術の教本では、一般的な人を約7.5頭身、理想化した人物を8頭身と説明します。ただしこの数値も慣例にすぎないので、数字を覚えるよりその写真で実際に数えるほうが正確です。かがんだり座ったりすると数は大きく変わります。', 'Drawing books often describe an average person as about 7.5 heads tall and an idealized figure as 8. Those numbers are conventions, so counting on the photo in front of you is more accurate than memorizing them. Bending or sitting changes the count a lot.', '美術教材常把一般人說成約 7.5 個頭身，理想化人物 8 個頭身。不過這些數字只是慣例，與其背數字，不如在眼前的照片上實際數比較準確。彎腰或坐下時格數會大幅改變。'),
                  T('팔을 곧게 편 채 연필을 세워 머리 꼭대기에 연필 끝을 맞추고, 턱 위치를 엄지로 표시합니다. 그 길이로 위에서부터 몸을 잽니다. 잴 때마다 팔을 똑같이 펴야 값이 흔들리지 않습니다.', '腕をまっすぐ伸ばしたまま鉛筆を立て、鉛筆の先を頭頂に合わせ、あごの位置を親指で示します。その長さで上から身体を測ります。毎回同じように腕を伸ばすと、値がぶれません。', 'Hold the pencil upright at arm\'s length, line its tip up with the top of the head, and mark the chin with your thumb. Step that length down the body. Keep the arm equally straight every time or the measurement drifts.', '手臂伸直、鉛筆立起，讓筆尖對準頭頂，用拇指標出下巴位置，再用這段長度從上往下量身體。每次手臂都要同樣伸直，數值才不會跑掉。')],
        'practice': (180, 5, 'DY'),
        'diagram': ('head-ruler', T('머리 길이를 한 칸으로 세면 이 사진의 인물은 약 7.6칸입니다. (PT001)', '頭の長さを1つ分として数えると、この写真の人物は約7.6頭身です。（PT001）', 'Counting in head lengths, this figure is about 7.6 heads tall. (PT001)', '以頭長為一格來數，這張照片的人物約 7.6 格。（PT001）')),
    },
    {
        'title': T('몸이 나무 기둥처럼 뻣뻣하다', '身体が丸太のように硬い', 'The body looks as stiff as a post', '身體像木樁一樣僵硬'),
        'symptom': T('비례는 맞는데 움직임이 없습니다. 같은 사람을 여러 포즈로 그려도 다 비슷해 보입니다.', '比率は合っているのに動きがありません。同じ人を何ポーズ描いても、どれも似て見えます。', 'The proportions are right but nothing moves. Different poses of the same person all look alike.', '比例沒問題，卻沒有動感。同一個人畫了好幾個姿勢，看起來都差不多。'),
        'cause': T('몸통을 위아래로 곧은 직사각형 하나로 그리고 팔다리를 거기에 붙이기 때문입니다. 실제 몸은 가슴통과 골반이 서로 다른 방향으로 기울고 비틀립니다.', '胴体を上下にまっすぐな長方形一つで描き、そこに手足を付けるからです。実際の身体は胸郭と骨盤が別々の向きに傾き、ねじれます。', 'The torso becomes one straight rectangle with limbs attached. In a real body the rib cage and pelvis tilt and twist in different directions.', '因為把軀幹畫成一個上下筆直的長方形，再把手腳接上去。真實身體的胸廓與骨盆會朝不同方向傾斜、扭轉。'),
        'fixes': [T('그리기 전에 어깨를 잇는 선과 골반을 잇는 선을 짧게 긋고 두 선의 각도를 비교합니다. 한쪽 다리에 무게를 싣고 선 사람은 두 선이 서로 반대로 기우는 경우가 많습니다. 고대 그리스 조각부터 쓰인 이 자세를 콘트라포스토라고 부릅니다.', '描く前に、両肩を結ぶ線と骨盤を結ぶ線を短く引き、二本の角度を比べます。片脚に体重をかけて立つ人は、二本が逆向きに傾くことがよくあります。古代ギリシャの彫刻から使われてきたこの姿勢をコントラポストと呼びます。', 'Before drawing, sketch a short shoulder line and hip line and compare their angles. When someone stands with weight on one leg, the two lines often tilt in opposite directions, a stance known as contrapposto since ancient Greek sculpture.', '下筆前先短短畫出肩線與骨盆線，比較兩條線的角度。單腳承重站立的人，兩條線常朝相反方向傾斜。這種自古希臘雕塑就使用的姿勢稱為對立式平衡（contrapposto）。'),
                  T('동작선을 실제보다 조금 더 휘게 그려 봅니다. 크로키에서는 약간의 과장이 움직임을 살립니다.', '動勢線を実際より少し大きく曲げて描いてみます。クロッキーでは少しの誇張が動きを生かします。', 'Bend the line of action a little more than the photo. In gesture drawing a bit of exaggeration brings out the movement.', '把動勢線畫得比實際再彎一點。速寫裡一點誇張能讓動作更鮮活。')],
        'practice': (30, 10, 'TR'),
        'diagram': ('tilts', T('어깨선과 골반선을 따로 긋고 두 선의 각도를 비교합니다. 몸통을 곧은 직사각형 하나로 보지 않기 위한 첫 단계입니다. (PT001)', '肩の線と骨盤の線を別々に引き、二本の角度を比べます。胴体をまっすぐな長方形一つと見ないための第一歩です。（PT001）', 'Draw the shoulder line and the hip line separately and compare them: the first step away from a rectangle torso. (PT001)', '分別畫出肩線與骨盆線並比較角度，這是不把軀幹看成單一長方形的第一步。（PT001）')),
    },
    {
        'title': T('서 있는데 금방이라도 넘어질 것 같다', '立っているのに今にも倒れそう', 'A standing figure looks about to fall over', '站著卻像隨時要跌倒'),
        'symptom': T('사람이 앞이나 옆으로 쏟아질 것처럼 보입니다. 어디가 틀렸는지 짚기 어려워 가장 답답한 실수입니다.', '人が前や横に倒れ込みそうに見えます。どこが違うのか指摘しにくく、いちばんもどかしいミスです。', 'The figure seems to pitch forward or sideways. It is hard to say what is wrong, which makes it the most frustrating mistake.', '人物看起來快往前或往旁邊倒。很難指出哪裡錯，是最讓人懊惱的錯誤。'),
        'cause': T('무게가 실린 발과 몸의 위치 관계가 사진과 달라서입니다. 두 다리를 같은 굵기의 기둥처럼 그리면 어느 다리가 몸을 받치는지 사라집니다.', '体重がかかる足と身体の位置関係が写真と違うからです。両脚を同じ太さの柱のように描くと、どちらの脚が身体を支えているかが消えてしまいます。', 'The relationship between the body and the weight-bearing foot differs from the photo. Drawing both legs as equal posts hides which one holds the body up.', '因為承重腳與身體的位置關係和照片不同。把兩條腿畫成一樣粗的柱子，就看不出哪條腿在支撐身體。'),
        'fixes': [T('몸통 가운데에서 바닥까지 가상의 수직선을 내립니다. 가만히 선 사람이 한 다리에 무게를 실었다면 그 발 쪽으로, 두 발에 고르게 실었다면 두 발 사이로 떨어지는지 확인하세요.', '胴体の中ほどから床まで仮の垂線を下ろします。静かに立つ人が片脚に体重をかけていればその足の側へ、両足に均等なら両足の間へ落ちるか確かめます。', 'Drop an imaginary vertical line from the middle of the torso to the floor. For a still, standing figure it should land toward the supporting foot, or between the feet when the weight is shared evenly.', '從軀幹中段往地面放一條假想垂線。靜止站立的人若單腳承重，它應落向那隻腳；兩腳平均承重時則落在兩腳之間。'),
                  T('많은 교재가 목 아래 오목한 곳에서 선을 내리라고 하는데, 몸통 가운데에서 내리는 쪽이 실제 무게중심에 더 가깝다는 설명도 있습니다. 어느 쪽이든 균형을 빠르게 점검하는 어림 방법이지 정확한 측정은 아닙니다.', '多くの教本は首の付け根のくぼみから線を下ろすよう教えますが、胴体の中ほどから下ろすほうが実際の重心に近いという説明もあります。どちらもバランスを素早く確かめる目安で、正確な測定ではありません。', 'Many books drop the line from the pit of the neck; some instructors prefer the middle of the torso because it is closer to the real centre of mass. Either way it is a quick check, not a precise measurement.', '許多教材教人從頸部下方的凹處放線，也有說法認為從軀幹中段放線更接近真正的重心。不論哪種，都是快速檢查平衡的估算法，不是精確測量。'),
                  T('무게를 받는 다리는 진하게, 균형만 돕는 다리는 가볍게 그립니다. 발이 바닥에 닿는 지점을 먼저 찍고 그 위에 다리를 세웁니다.', '体重を受ける脚は濃く、バランスを助けるだけの脚は軽く描きます。足が床に触れる点を先に打ち、その上に脚を立てます。', 'Draw the weight-bearing leg darker and the balancing leg lighter. Mark where the feet touch the floor first, then build the legs on top.', '承重的腿畫深，只負責平衡的腿畫淡。先點出腳接觸地面的位置，再往上立起腿。')],
        'practice': (60, 10, 'ST'),
        'diagram': ('plumb-one-foot', T('한 발로 선 자세에서 몸통 가운데에서 내린 선은 지지 발 위로 떨어집니다. (PT004)', '片足立ちでは、胴体の中ほどから下ろした線は支える足の上に落ちます。（PT004）', 'Standing on one foot, the line from the middle of the torso falls over the supporting foot. (PT004)', '單腳站立時，從軀幹中段放下的線會落在承重腳上。（PT004）')),
        'more': T('더 자세한 설명은 {balance}에 있습니다.', '詳しくは{balance}をご覧ください。', 'For more detail, read {balance}.', '更詳細的說明請看{balance}。'),
    },
    {
        'title': T('선이 털처럼 여러 겹이다', '線が毛羽立ったように何重にもなる', 'Lines come out fuzzy and layered', '線條像毛一樣疊了好幾層'),
        'symptom': T('한 번에 그은 긴 선 대신 짧은 선을 여러 번 덧그어 윤곽이 보풀처럼 일어납니다. 그림이 지저분해 보이고 형태도 흐려집니다.', '一度に引いた長い線ではなく短い線を何度も重ね、輪郭が毛羽立ちます。絵が雑然として形もぼやけます。', 'Instead of one long line, many short strokes pile up and the outline frays. The drawing looks messy and the form blurs.', '不是一筆拉出的長線，而是短線反覆疊畫，輪廓像起毛球一樣。畫面顯得凌亂，形體也變模糊。'),
        'cause': T('틀릴까 봐 조금씩 확인하며 긋기 때문입니다. 손목만 움직여 짧은 선밖에 나오지 않는 경우도 많습니다.', '間違えないよう少しずつ確かめながら引くからです。手首だけを動かして短い線しか出ない場合も多くあります。', 'Fear of being wrong makes us draw in small checked steps. Often only the wrist moves, so only short strokes come out.', '因為怕畫錯，一點一點確認著畫。很多時候只動手腕，所以只畫得出短線。'),
        'fixes': [T('연필을 조금 길게 잡고, 손목 대신 팔꿈치와 어깨로 선을 긋습니다. 세밀한 묘사에는 손목이 낫지만 크로키의 큰 흐름에는 팔 전체가 맞습니다.', '鉛筆を少し長めに持ち、手首ではなく肘と肩で線を引きます。細かい描写には手首が向いていますが、クロッキーの大きな流れには腕全体が合います。', 'Hold the pencil a little further back and draw from the elbow and shoulder, not the wrist. The wrist suits fine detail; the whole arm suits the big flow of a gesture.', '鉛筆握長一點，用手肘和肩膀而不是手腕來畫線。細部描寫適合用手腕，速寫的大流向則適合整隻手臂。'),
                  T('틀린 선은 지우지 말고 그 옆에 새 선을 한 번 더 긋습니다. 처음 선은 가볍게, 맞는 선은 진하게 남기면 됩니다.', '間違えた線は消さず、その横に新しい線をもう一本引きます。最初の線は軽く、合っている線は濃く残せば十分です。', 'Do not erase a wrong line; draw a new one beside it. Keep searching lines light and the right line darker.', '畫錯的線不要擦，在旁邊再畫一條新的。先畫的線輕一點，對的線留深一點就好。'),
                  T('그리기 전에 종이 한쪽에 긴 곡선을 열 번 그어 손을 풀고 시작합니다.', '描く前に、紙の端に長い曲線を10回引いて手をほぐしてから始めます。', 'Warm up by drawing ten long curves in the margin before you start.', '開始前先在紙邊畫十條長曲線熱手。')],
        'practice': (30, 15, None),
        'strokes': T('같은 곡선이라도 짧게 덧그으면 윤곽이 흐려지고, 한 번에 그으면 방향이 분명해집니다.', '同じ曲線でも、短く重ねると輪郭がぼやけ、一度に引くと向きがはっきりします。', 'The same curve: layered short strokes blur the edge, one long stroke makes the direction clear.', '同樣的曲線，短線疊畫會讓輪廓模糊，一筆畫完方向就很清楚。'),
    },
    {
        'title': T('바깥 윤곽만 따라 그린다', '外側の輪郭だけをなぞる', 'You trace only the outer outline', '只沿著外輪廓描'),
        'symptom': T('옷의 외곽선은 정확한데 몸이 납작합니다. 다리가 겹치는 부분이나 팔이 몸 앞을 지나가는 부분에서 선이 엉킵니다.', '服の外形線は正確なのに身体が平たく見えます。脚が重なる部分や、腕が身体の前を通る部分で線が絡まります。', 'The outline of the clothes is accurate but the body looks flat. Lines tangle where the legs overlap or an arm crosses the body.', '衣服外輪廓很準，身體卻扁平。腿重疊或手臂經過身體前方的地方，線條就打結。'),
        'cause': T('사진을 평면 위의 모양으로 보기 때문입니다. 윤곽선은 앞에 있는 것과 뒤에 있는 것을 구분해 주지 않습니다.', '写真を平面上の形として見ているからです。輪郭線は、手前にあるものと奥にあるものを区別してくれません。', 'We read the photo as a flat shape, and an outline does not tell you what is in front and what is behind.', '因為把照片當成平面上的形狀來看。輪廓線無法區分什麼在前、什麼在後。'),
        'fixes': [T('윤곽을 따기 전에 가슴통과 골반을 상자로, 팔다리를 원통으로 가볍게 놓습니다.', '輪郭をとる前に、胸郭と骨盤を箱、手足を円柱として軽く置きます。', 'Before outlining, lightly place the rib cage and pelvis as boxes and the limbs as cylinders.', '描輪廓之前，先輕輕把胸廓與骨盆放成箱子、四肢放成圓柱。'),
                  T('두 부분이 겹치면 앞에 있는 쪽의 선을 끊기지 않게 그리고, 뒤에 있는 쪽의 선은 그 앞에서 멈춥니다. 이렇게 한 선이 다른 선 앞에서 끝나는 T자 모양이 앞뒤를 알려 주는 단서가 됩니다.', '二つの部分が重なったら、手前の線を途切れさせずに描き、奥の線はその手前で止めます。一本の線が別の線の前で終わるこのT字形が、前後を伝える手がかりになります。', 'Where two parts overlap, keep the front one\'s line unbroken and stop the back one\'s line where it meets it. That T-shaped junction is what tells the eye which part is in front.', '兩個部分重疊時，前面那條線不中斷，後面那條線在它前面停住。一條線在另一條線前結束的 T 形交會，就是判斷前後的線索。'),
                  T('앉은 자세나 바닥 자세처럼 겹침이 많은 포즈로 연습하면 효과가 빠릅니다.', '座りポーズや床のポーズのように重なりの多いポーズで練習すると効果が早く出ます。', 'Poses with many overlaps, such as seated or floor poses, give the fastest results.', '用坐姿或地板姿勢這類重疊多的姿勢練習，效果最快。')],
        'practice': (180, 5, 'FL'),
        'diagram': ('boxes-seated', T('가슴통과 골반을 상자로, 앞에 있는 허벅지를 원통으로 놓은 모습입니다. 앞 허벅지의 윤곽은 끊기지 않고, 뒤쪽 다리 선은 그 앞에서 멈춥니다. (PT049)', '胸郭と骨盤を箱、手前の太ももを円柱として置いた様子です。手前の太ももの輪郭は途切れず、奥の脚の線はその手前で止まります。（PT049）', 'Boxes for the rib cage and pelvis, a cylinder for the front thigh. Its outline stays unbroken; the back leg\'s line stops where it meets it. (PT049)', '胸廓與骨盆放成箱子，前方大腿放成圓柱。前方大腿的輪廓不中斷，後腿的線在它前面停住。（PT049）')),
        'more': T('앉은 자세의 겹침은 {seated}에서 사진과 함께 설명합니다.', '座りポーズの重なりは{seated}で写真とともに説明しています。', '{seated} explains seated overlaps with a photo.', '坐姿的重疊在{seated}中搭配照片說明。'),
    },
]
CHECK = {
    'title': T('그린 뒤 30초 점검표', '描いた後の30秒チェック表', 'A 30-second checklist after drawing', '畫完後的 30 秒檢查表'),
    'intro': T('연습이 끝나면 그린 종이를 한꺼번에 놓고 아래 질문에 예·아니오로만 답해 보세요. "아니오"가 가장 많이 나온 항목이 다음 주에 연습할 항목입니다.', '練習が終わったら描いた紙をまとめて並べ、下の質問に「はい・いいえ」だけで答えてみましょう。「いいえ」がいちばん多かった項目が、来週練習する項目です。', 'After a session, lay the pages out together and answer each question with yes or no. The item with the most "no" answers is next week\'s practice.', '練習結束後，把畫好的紙一起攤開，只用「是／否」回答下面的問題。「否」最多的那一項，就是下週要練習的項目。'),
    'items': [
        T('얼굴이 없어도 자세가 읽히나요? (1번)', '顔がなくても姿勢が読み取れますか。（1）', 'Can you read the pose without a face? (1)', '沒有臉也看得出姿勢嗎？（1）'),
        T('머리부터 발까지 종이 안에 들어왔나요? (2번)', '頭から足まで紙に収まりましたか。（2）', 'Did head to feet fit on the page? (2)', '從頭到腳都在紙內嗎？（2）'),
        T('머리 길이로 몸을 재 봤나요? (3번)', '頭の長さで身体を測ってみましたか。（3）', 'Did you measure the body in head lengths? (3)', '有用頭長量過身體嗎？（3）'),
        T('어깨선과 골반선의 각도가 서로 다른가요? (4번)', '肩の線と骨盤の線の角度は違っていますか。（4）', 'Do the shoulder and hip lines have different angles? (4)', '肩線與骨盆線的角度不同嗎？（4）'),
        T('무게를 받는 발이 어느 쪽인지 보이나요? (5번)', '体重を受ける足がどちらか見えますか。（5）', 'Can you see which foot carries the weight? (5)', '看得出哪隻腳承重嗎？（5）'),
        T('한 번에 그은 긴 선이 더 많은가요? (6번)', '一度に引いた長い線のほうが多いですか。（6）', 'Are most lines long, single strokes? (6)', '一筆畫完的長線比較多嗎？（6）'),
        T('겹치는 곳에서 앞에 있는 선이 끊기지 않았나요? (7번)', '重なる所で手前の線が途切れていませんか。（7）', 'Where forms overlap, is the front line unbroken? (7)', '重疊處前面的線沒有中斷嗎？（7）'),
    ],
    'close': T('어디서부터 시작할지 모르겠다면 {30-day-routine}을 따라가 보세요. 이 글에서 다룬 동작선, 기울기, 무게중심, 덩어리와 겹침을 한 주에 한 주제씩 나눠 연습하도록 짜여 있습니다.', 'どこから始めればよいか分からなければ、{30-day-routine}に沿って進めてみてください。この記事で扱った動勢線・傾き・重心・塊と重なりを、1週に1テーマずつ練習できるように組んであります。', 'If you are not sure where to start, follow {30-day-routine}. It practises the line of action, tilts, balance, and masses and overlaps, one theme per week.', '不知道從哪裡開始，可以跟著{30-day-routine}練習。它把本文談到的動勢線、傾斜、重心、體塊與重疊，安排成一週一個主題。'),
}
MISTAKE_REFS = [
    (T('시선이 얼굴로 먼저 향하는 경향', '視線がまず顔に向かう傾向', 'Gaze goes to faces first', '視線先落在臉上的傾向'), [R_CERF]),
    (T('아래로 갈수록 커지는 실수와 위아래 먼저 정하기', '下に行くほど大きくなるミスと上下を先に決めること', 'Drawing progressively larger, and setting top and bottom first', '越往下越大的錯誤與先定上下'), [R_MEASURE]),
    (T('머리 길이 비례와 그 한계', '頭身の比率とその限界', 'Head-length proportions and their limits', '頭身比例與其限制'), [R_PROPORTIONS]),
    (T('연필로 재는 방법', '鉛筆で測る方法', 'Measuring with a pencil', '用鉛筆測量的方法'), [R_PENCIL]),
    (T('어깨선과 골반선의 반대 기울기', '肩と骨盤の逆の傾き', 'Opposite tilt of shoulders and hips', '肩與骨盆的反向傾斜'), [R_CONTRAPPOSTO]),
    (T('무게중심선과 지지 발', '重心線と支える足', 'Balance line and supporting foot', '重心線與承重腳'), [R_BALANCE]),
    (T('팔 전체로 긴 선 긋기', '腕全体で長い線を引く', 'Drawing long lines with the whole arm', '用整隻手臂畫長線'), [R_SHOULDER]),
    (T('가슴통·골반을 상자로 단순화', '胸郭・骨盤を箱で単純化', 'Simplifying rib cage and pelvis as boxes', '把胸廓與骨盆簡化成箱子'), [R_ROBOBEAN]),
    (T('동작선의 곡선과 과장', '動勢線の曲線と誇張', 'Curves and exaggeration in the line of action', '動勢線的曲線與誇張'), [R_LOA]),
]


def render_mistakes(lang):
    out = []
    for n, item in enumerate(ITEMS, 1):
        fixes = ''.join(f'<li>{escape(pick(lang, f))}</li>' for f in item['fixes'])
        s, c, cat = item['practice']
        block = (f'<section class="mistake" id="mistake-{n}"><h2>{n}. {escape(pick(lang, item["title"]))}</h2>'
                 f'<p><strong>{escape(pick(lang, SYMPTOM))}</strong> {escape(pick(lang, item["symptom"]))}</p>'
                 f'<p><strong>{escape(pick(lang, CAUSE))}</strong> {escape(pick(lang, item["cause"]))}</p>'
                 f'<p><strong>{escape(pick(lang, FIX))}</strong></p><ul>{fixes}</ul>')
        if 'diagram' in item:
            key, caption = item['diagram']
            block += figure(lang, key, pick(lang, caption))
        if 'strokes' in item:
            block += strokes(lang, pick(lang, item['strokes']))
        block += (f'<p class="practice-line"><strong>{escape(pick(lang, PRACTICE))}</strong> '
                  f'<a href="{studio_href(lang, s, c, cat)}">{escape(session_label(lang, s, c, cat))}</a></p>')
        if 'more' in item:
            block += rich(lang, item['more'], COMMON_LINKS)
        out.append(block + '</section>')
    checks = ''.join(f'<li>{escape(pick(lang, q))}</li>' for q in CHECK['items'])
    out.append(f'<section><h2>{escape(pick(lang, CHECK["title"]))}</h2>{paragraph(lang, CHECK["intro"])}<ol>{checks}</ol>{rich(lang, CHECK["close"], COMMON_LINKS)}</section>')
    out.append(references(lang, MISTAKE_REFS))
    out.append(f'<p class="source-note">{escape(pick(lang, AI_NOTE))}</p>')
    return ''.join(out)


ARTICLES = {'30-day-routine': (ROUTINE, render_routine), 'common-mistakes': (MISTAKES, render_mistakes)}


def article_meta(lang, slug):
    meta, _ = ARTICLES[slug]
    return {key: pick(lang, meta[key]) for key in ('title', 'description', 'lead')}


def render_article(lang, slug):
    return ARTICLES[slug][1](lang)


# ---------------------------------------------------------------- hub
HUB = {
    'title': T('크로키 연습 가이드 모음', 'クロッキー練習ガイド一覧', 'Gesture drawing practice guides', '速寫練習指南總覽'),
    'description': T('포즈토키의 크로키 연습 글을 한곳에 모았습니다. 처음 시작하는 법, 30일 루틴, 동작선·무게중심·앉은 자세 관찰, 흔한 실수 고치는 법까지.',
                     'PoseTokiのクロッキー練習記事をまとめました。始め方、30日ルーティン、動勢線・重心・座りポーズの観察、よくあるミスの直し方まで。',
                     'All of PoseToki\'s gesture drawing guides in one place: getting started, a 30-day routine, line of action, balance and seated poses, and fixing common mistakes.',
                     '集合 PoseToki 所有速寫練習文章：入門方法、30 天練習計畫、動勢線、重心與坐姿觀察，以及常見錯誤的修正。'),
    'lead': T('무엇부터 읽을지 고민된다면 위에서부터 차례로 보세요. 각 글에는 바로 그 설정으로 연습실을 여는 링크가 있습니다.',
              '何から読むか迷ったら、上から順に読んでください。各記事には、その設定のまま練習室を開くリンクがあります。',
              'Not sure where to begin? Read from the top down. Every guide has a link that opens the studio with matching settings.',
              '不知道先讀哪篇，就從上往下依序看。每篇文章都有以相同設定開啟練習室的連結。'),
    'groups': [
        (T('처음 시작한다면', '初めての方へ', 'If you are just starting', '剛開始的話'), ('beginner', 'guide', '30-day-routine')),
        (T('한 가지씩 깊게 보기', '一つずつ深く見る', 'One observation at a time', '一次深入看一件事'), ('gesture', 'balance', 'seated')),
        (T('그림이 막힐 때', '絵が行き詰まったとき', 'When your drawings get stuck', '畫不下去的時候'), ('common-mistakes',)),
    ],
    'poses_note': T('120개 포즈를 유형별로 보고 싶다면 포즈 자료실로 가세요.', '120のポーズを種類別に見たいときはポーズ資料室へどうぞ。', 'To browse all 120 poses by type, visit the pose library.', '想依類型瀏覽 120 個姿勢，請前往姿勢素材庫。'),
}
