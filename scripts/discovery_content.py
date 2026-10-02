"""A beginner exercise and a crawlable catalog drawn from the actual pose data."""
import json
from html import escape
from pathlib import Path
from seo_common import HOME

EXTRA_SLUGS = ('beginner', 'poses')
CATEGORY_NAMES = {
 'ST': ['서기·체중 이동', '立つ・体重移動', 'Standing & weight shift', '站姿與重心轉移'],
 'WK': ['걷기·달리기', '歩く・走る', 'Walking & running', '行走與跑步'],
 'DY': ['점프·스포츠·춤', 'ジャンプ・スポーツ・ダンス', 'Jumping, sport & dance', '跳躍、運動與舞蹈'],
 'TR': ['뻗기·굽히기·비틀기', '伸ばす・曲げる・ひねる', 'Reaching, bending & twisting', '伸展、彎曲與扭轉'],
 'CH': ['의자·좌석', '椅子・座席', 'Chair & seat poses', '椅子與座位'],
 'FL': ['바닥·무릎·쪼그림', '床・膝・しゃがむ', 'Floor, kneeling & crouching', '地板、跪姿與蹲姿'],
 'LY': ['눕기·기대기', '寝る・もたれる', 'Lying & reclining', '躺臥與倚靠'],
 'FP': ['밀기·당기기·들기', '押す・引く・持ち上げる', 'Pushing, pulling & lifting', '推、拉與提舉'],
 'DA': ['일상·도구 사용', '日常・道具を使う', 'Daily life & tools', '日常與工具使用'],
 'EM': ['감정·의사 표현', '感情・意思の表現', 'Emotion & communication', '情緒與意思表達'],
}
COLUMNS = {'ko': 0, 'ja': 1, 'en': 2, 'zh-TW': 3}
COPY = {
 'ko': {
  'beginner': {'title': '크로키 초보자를 위한 10분 인체 연습법', 'description': '연필 한 자루로 시작하는 초보자 크로키. 1분 포즈 5장씩 두 묶음을 그리며 동작선, 어깨·골반, 지지 발을 관찰하는 실습 가이드.', 'lead': '처음 크로키를 할 때는 모든 윤곽을 끝내려고 하지 마세요. 이 연습은 1분 포즈 5장씩 두 묶음, 총 10분의 그리는 시간으로 구성됩니다. 첫 묶음에서는 몸의 큰 흐름을, 두 번째 묶음에서는 몸이 서 있는 이유를 살핍니다.'},
  'poses': {'title': '무료 크로키 포즈 자료: 10가지 유형, 120개 인체 자세', 'description': '서기·걷기·앉기·스포츠·일상 동작 등 120개 AI 생성 착의 인물 포즈. 자세별 관찰 목표와 권장 시간을 읽고 타이머로 바로 연습하세요.', 'lead': '각 포즈에는 이름, 난이도, 관찰 목표와 권장 시간이 있습니다. 작은 디테일을 베끼기보다 몸의 흐름과 지지점을 읽어보세요. 아래 이미지는 모두 AI 생성 착의 인물 예시이며 실제 인물 사진이 아닙니다.'},
  'nav': ['초보자 연습법', '포즈 자료실'], 'jump': '자세 유형으로 이동', 'level': ['초급','중급','고급'], 'start': '이 포즈로 연습', 'seconds': '초',
  'catalog_title': '자료를 연습에 활용하는 방법', 'catalog_intro': '초보자라면 서기·체중 이동에서 1분·5장을 고릅니다. 첫 30초에 머리·가슴통·골반을 놓고, 남은 시간에 무게가 실린 발과 어깨·골반의 각도를 비교하세요. 권장 시간은 관찰 과제의 출발점이며 정답이나 필수 제한 시간이 아닙니다.',
  'limit_title': 'AI 예시 자료의 한계', 'limit': '손가락, 발, 관절과 비례에 생성 오류가 남아 있을 수 있습니다. 해부학의 정답으로 사용하지 말고 실제 인물 관찰과 함께 연습하세요. 이미지의 문제를 발견하면 포즈 번호를 적어 운영 안내의 공개 제보 창구로 알려주세요.',
  'steps': [
   ('준비: 사진보다 먼저 연습 목표 정하기', '종이와 연필을 준비하고 지우개는 잠시 내려놓습니다. 연습실에서 서기·체중 이동, 1분, 5장을 선택하세요. 완성 그림을 만드는 시간이 아니라 큰 덩어리와 지지점을 알아보는 시간이라고 정합니다.'),
   ('첫 5분: 머리·가슴통·골반 세 덩어리', '각 포즈의 첫 10초는 사진만 봅니다. 머리와 발의 위치를 종이에 작은 점으로 잡고, 가슴통과 골반이 향하는 방향을 단순한 덩어리로 놓습니다. 팔과 다리는 긴 축으로 연결합니다. 얼굴, 손가락, 옷 주름은 생략합니다.'),
   ('다음 5분: 같은 자세 유형에서 무게중심 찾기', '같은 설정으로 새 묶음을 시작합니다. 발과 바닥이 닿는 곳을 먼저 찍고 어느 다리가 몸통을 받치는지 살핍니다. 어깨와 골반의 기울기를 짧은 선 두 개로 기록하세요. 새 포즈가 나오면 앞 그림을 고치지 말고 새 칸에서 시작합니다.'),
   ('그린 뒤: 두 장만 골라 비교하기', '처음과 마지막 묶음에서 한 장씩 고릅니다. 손과 얼굴을 가려도 자세가 읽히는지, 몸통과 지지 발이 연결되는지, 어깨와 골반이 무심코 평행해지지 않았는지 봅니다. 복습 시간은 위 10분의 그리는 시간에 추가합니다. 다음 목표는 한 가지로 좁히세요.'),
   ('시간이 부족하거나 자세가 어색할 때', '1분이 짧으면 3분으로 바꾸되 처음 1분의 큰 구조부터 시작하세요. 그림이 뻣뻣하면 윤곽선 대신 머리에서 골반을 지나 지지 발로 내려가는 선 하나를 먼저 그립니다. 사진을 고개를 돌려 본 것처럼 기울여 해석하지 말고 접지점과 어깨 각도를 다시 비교합니다.'),
  ],
  'table_title': '30초·1분·3분에는 무엇을 남길까요?', 'table_headers': ['시간','관찰 목표','마무리 기준'], 'table_rows': [('30초','동작선과 머리·발의 위치','몸이 어느 쪽으로 향하는지 한 선으로 읽힌다.'),('1분','가슴통·골반·지지 발','어깨와 골반의 기울기, 무게를 받는 다리가 구별된다.'),('3분','비례·회전·앞뒤 겹침','큰 구조를 유지한 채 관절과 겹침을 점검한다.')],
  'cta': '1분·5장으로 첫 묶음 시작', 'next': '사진으로 더 깊게 연습하기',
 },
 'en': {
  'beginner': {'title': 'Gesture drawing for beginners: a 10-minute figure exercise', 'description': 'Two sets of five 1-minute poses for beginners. Use a pencil to observe the line of action, shoulder and hip angles, and the supporting foot.', 'lead': 'You do not need to finish every contour when you start gesture drawing. This exercise uses two sets of five 1-minute poses: ten minutes of drawing. In the first set, observe the big shapes; in the second, look for what supports the body.'},
  'poses': {'title': 'Free gesture drawing references: 120 figure poses in 10 types', 'description': 'Browse 120 AI-generated clothed figure poses: standing, walking, seated, sport and daily actions. Read observation goals and suggested times, then practise with a timer.', 'lead': 'Each pose has a name, level, observation goal and suggested duration. Read the body’s gesture and support instead of copying small details. Every image below is an AI-generated clothed figure example, not a photograph of a real person.'},
  'nav': ['Beginner exercise', 'Pose reference library'], 'jump': 'Jump to a pose type', 'level': ['Beginner','Intermediate','Advanced'], 'start': 'Practise this pose', 'seconds': ' sec',
  'catalog_title': 'How to use the references', 'catalog_intro': 'For a first session, choose Standing & weight shift, 1 minute and 5 poses. Spend the first 30 seconds placing the head, rib cage and pelvis, then compare the supporting foot and shoulder–hip angles. Suggested times are starting points for observation, not mandatory limits or measures of success.',
  'limit_title': 'Limits of the AI examples', 'limit': 'Fingers, feet, joints and proportions may contain generation errors. Use these references alongside observation of real people, rather than as an anatomy answer key. Report an image issue with its pose ID through the public contact channel on the operation page.',
  'steps': [
   ('Prepare: choose an observation goal', 'Take paper and a pencil; leave the eraser aside for now. In the studio choose Standing & weight shift, 1 minute and 5 poses. Your task is to notice the big shapes and supports, rather than produce a finished illustration.'),
   ('First five minutes: three big shapes', 'Spend the first ten seconds of each pose just looking. Mark the head and feet with small points. Place the rib cage and pelvis as simple shapes pointing in the directions you see. Connect arms and legs with long axes. Leave out faces, fingers and clothing folds.'),
   ('Next five minutes: find what carries the weight', 'Start another set with the same settings. Mark where the feet touch the ground before drawing the body. Which leg supports the torso? Record shoulder and hip angles with two short lines. Move to a fresh space when the next pose appears, rather than correcting the previous drawing.'),
   ('After drawing: compare only two studies', 'Choose one study from each set. Cover the face and hands: is the pose still readable? Does the torso connect to its supporting foot? Did you accidentally make the shoulders and hips parallel? Review time is additional to the ten minutes of drawing. Pick just one goal for your next session.'),
   ('When time is short or the pose looks stiff', 'Switch to three minutes if one minute is too short, but still begin with the same big structure. If your drawing looks stiff, draw one line from the head through the pelvis to the supporting foot before outlining it. Recheck the contact points and shoulder angles rather than guessing from a tilted view of the photo.'),
  ],
  'table_title': 'What belongs in 30 seconds, one minute or three minutes?', 'table_headers': ['Time','Observation goal','What to keep'], 'table_rows': [('30 sec','Gesture, head and foot positions','One line makes the overall direction readable.'),('1 min','Rib cage, pelvis and supporting foot','Shoulder–hip angles and the weight-bearing leg are distinct.'),('3 min','Proportion, rotation and overlap','Check joints and overlap while keeping the big structure.')],
  'cta': 'Start the first set: 1 minute × 5', 'next': 'Study an example more closely',
 },
 'ja': {
  'beginner': {'title': 'クロッキー初心者向け：10分の人物練習', 'description': '1分ポーズ5枚を2セット。鉛筆一本で、動きの線、肩と骨盤の傾き、身体を支える足を観察する初心者向け実践ガイド。', 'lead': 'クロッキーを始めたばかりなら、輪郭をすべて描き終えようとしなくて大丈夫です。1分ポーズ5枚を2セット、描く時間は合計10分。最初は大きな形、次は身体を支える構造に注目します。'},
  'poses': {'title': '無料クロッキー資料：10種類・120の人物ポーズ', 'description': '立つ・歩く・座る・スポーツ・日常動作など、AI生成の着衣人物120ポーズ。観察ポイントと推奨時間を読み、タイマーで練習できます。', 'lead': '各ポーズには名前、難易度、観察ポイントと推奨時間があります。細部を写す前に、動きと身体の支えを読みましょう。掲載画像はすべてAI生成の着衣人物サンプルで、実在人物の写真ではありません。'},
  'nav': ['初心者の練習法', 'ポーズ資料室'], 'jump': 'ポーズの種類へ移動', 'level': ['初級','中級','上級'], 'start': 'このポーズで練習', 'seconds': '秒',
  'catalog_title': '資料を練習に使う方法', 'catalog_intro': '最初は「立つ・体重移動」で1分・5枚を選びます。前半30秒で頭・胸郭・骨盤を置き、残りで支える足と肩・骨盤の角度を比べます。推奨時間は観察課題の出発点であり、必須の制限や成功の基準ではありません。',
  'limit_title': 'AIサンプルの限界', 'limit': '指、足、関節、比率に生成の誤りが残る可能性があります。解剖学の正解として使わず、実際の人物の観察と併用してください。画像の問題はポーズ番号を添えて、運営案内の公開窓口から報告できます。',
  'steps': [
   ('準備：観察する目的を一つ決める', '紙と鉛筆を用意し、消しゴムは一旦置きます。練習室で「立つ・体重移動」、1分、5枚を選びましょう。完成イラストを作るのではなく、大きな形と支えを見つける時間にします。'),
   ('最初の5分：頭・胸郭・骨盤の三つの形', '各ポーズの最初の10秒は見るだけにします。頭と足の位置を小さな点で置き、胸郭と骨盤を向きのある単純な形で描きます。腕と脚は長い軸でつなぎます。顔、指、服のしわは省きます。'),
   ('次の5分：体重を支える位置を探す', '同じ設定で次のセットを始めます。足と床の接点を先に記し、どちらの脚が胴体を支えているかを見ます。肩と骨盤の傾きを短い二本の線で示しましょう。ポーズが変わったら前の絵を直さず、新しい欄で始めます。'),
   ('描いた後：二枚だけ比べる', '各セットから一枚選びます。顔と手を隠しても姿勢が読めるか、胴体が支える足につながるか、肩と骨盤を無意識に平行にしていないか確認します。振り返り時間は10分の描画に追加します。次の目標は一つに絞りましょう。'),
   ('時間が足りない・姿勢が硬くなる場合', '1分が短ければ3分に変えても、最初は同じ大きな構造から始めます。硬く見えるなら輪郭の前に、頭から骨盤を通り支える足へ一本の線を引きます。写真を傾けて推測するより、接点と肩の角度を再確認しましょう。'),
  ],
  'table_title': '30秒・1分・3分で何を残す？', 'table_headers': ['時間','観察の目的','残したい構造'], 'table_rows': [('30秒','動きの線と頭・足の位置','一本の線で身体の向きが読める。'),('1分','胸郭・骨盤・支える足','肩と骨盤の傾き、体重を受ける脚が区別できる。'),('3分','比率・回転・重なり','大きな構造を保ちながら関節と重なりを確認する。')],
  'cta': '最初のセット：1分×5枚', 'next': '写真をもっと深く観察する',
 },
 'zh-TW': {
  'beginner': {'title': '人物速寫初學者：10分鐘人體練習法', 'description': '每張1分鐘、5張為一組，練習兩組。用鉛筆觀察動勢線、肩膀與骨盆的傾斜，以及支撐身體的腳。', 'lead': '剛開始人物速寫時，不必急著完成所有輪廓。本練習分兩組，每組五張、每張一分鐘，繪畫時間共十分鐘。第一組看大形，第二組看身體如何獲得支撐。'},
  'poses': {'title': '免費人物速寫素材：10種類型、120個人體姿勢', 'description': '瀏覽站姿、行走、坐姿、運動與日常動作等120張AI生成著衣人物。閱讀觀察重點與建議時間，直接用計時器練習。', 'lead': '每個姿勢都有名稱、難度、觀察重點與建議時間。先讀出身體動勢與支撐，再處理細節。下方圖片全為AI生成的著衣人物範例，並非真實人物照片。'},
  'nav': ['初學者練習法', '姿勢素材庫'], 'jump': '跳至姿勢類型', 'level': ['初級','中級','進階'], 'start': '練習這個姿勢', 'seconds': ' 秒',
  'catalog_title': '如何使用參考素材', 'catalog_intro': '第一次練習可選「站姿與重心轉移」、1分鐘、5張。前30秒放下頭、胸廓與骨盆，剩餘時間比較支撐腳和肩膀、骨盆角度。建議時間只是觀察課題的起點，不是必須遵守的限制或成功標準。',
  'limit_title': 'AI範例的限制', 'limit': '手指、腳、關節與比例可能仍有生成錯誤。請搭配真實人物觀察使用，勿當成解剖學標準答案。若發現圖片問題，可附上姿勢編號，透過營運說明的公開管道回報。',
  'steps': [
   ('準備：先選一個觀察目標', '準備紙和鉛筆，先把橡皮擦放一旁。在練習室選「站姿與重心轉移」、1分鐘、5張。目標是看出大形與支撐點，不是完成一張插畫。'),
   ('前五分鐘：頭、胸廓與骨盆三個大形', '每個姿勢的前10秒只觀察。用小點標出頭和腳，把胸廓、骨盆放成有方向的簡單形體。手臂與腿用長軸連接。先省略臉、手指和衣服皺褶。'),
   ('接著五分鐘：找到承重的位置', '用相同設定開始新一組。先標出腳與地面的接點，再看哪條腿支撐軀幹。用兩條短線記錄肩膀與骨盆的傾斜。姿勢切換後，在新空間開始，不要一直修前一張。'),
   ('畫完後：只比較兩張', '每組各選一張。遮住臉和手後，姿勢還讀得出來嗎？軀幹是否接到支撐腳？是否不自覺把肩膀與骨盆畫成平行？回顧時間另計，不含在十分鐘繪畫時間內。下次只選一個目標。'),
   ('時間不足或姿勢僵硬時', '若1分鐘太短，可改成3分鐘，但仍先畫相同的大結構。姿勢僵硬時，先用一條線從頭穿過骨盆連到支撐腳，再處理輪廓。與其傾斜照片猜測，不如重新比較接地點和肩膀角度。'),
  ],
  'table_title': '30秒、1分鐘、3分鐘要留下什麼？', 'table_headers': ['時間','觀察目標','保留的結構'], 'table_rows': [('30秒','動勢線與頭、腳位置','一條線能讀出全身方向。'),('1分鐘','胸廓、骨盆與支撐腳','能區分肩盆傾斜和承重腿。'),('3分鐘','比例、旋轉與前後交疊','維持大結構，檢查關節與重疊。')],
  'cta': '第一組：1分鐘×5張', 'next': '更深入觀察範例',
 },
}


def load_poses():
    source = (Path(__file__).resolve().parents[1] / 'dist/pose-library.js').read_text()
    return json.loads(source.split('=', 1)[1].strip().removesuffix(';'))


def render_beginner(lang):
    copy = COPY[lang]
    body = ''.join(f'<section><h2>{escape(title)}</h2><p>{escape(text)}</p></section>' for title, text in copy['steps'])
    headers = ''.join(f'<th scope="col">{escape(t)}</th>' for t in copy['table_headers'])
    rows = ''.join('<tr>' + ''.join(f'<{tag}>{escape(v)}</{tag}>' for tag, v in zip(('th','td','td'), row)) + '</tr>' for row in copy['table_rows'])
    body += f'<section><h2>{escape(copy["table_title"])}</h2><div class="table-scroll"><table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></div></section>'
    body += f'<section class="practice-callout"><h2>{escape(copy["cta"])}</h2><p>{escape(copy["limit"])}</p><a class="primary" href="{HOME[lang]}?seconds=60&amp;count=5&amp;category=ST#practice">{escape(copy["cta"])} →</a></section>'
    return body


def render_catalog(lang):
    copy = COPY[lang]; column = COLUMNS[lang]; poses = load_poses()
    nav = ''.join(f'<a href="#type-{key.lower()}">{escape(names[column])}</a>' for key, names in CATEGORY_NAMES.items())
    body = f'<section><h2>{escape(copy["catalog_title"])}</h2><p>{escape(copy["catalog_intro"])}</p></section><nav class="catalog-jump" aria-label="{escape(copy["jump"])}">{nav}</nav>'
    for code, names in CATEGORY_NAMES.items():
        cards = ''
        for pose in [p for p in poses if p['category'] == code]:
            level = copy['level'][('beginner','intermediate','advanced').index(pose['level'])]
            href = f'{HOME[lang]}?poseId={pose["id"]}&amp;category={code}&amp;seconds={pose["seconds"]}&amp;count=5#practice'
            cards += f'<article class="reference-card" id="{pose["id"]}"><img src="{pose["thumb"]}" width="256" height="384" loading="lazy" decoding="async" alt="{escape(pose["name"][lang], quote=True)}"><div><small>{pose["id"]} · {escape(level)} · {pose["seconds"]}{copy["seconds"]}</small><h3>{escape(pose["name"][lang])}</h3><p>{escape(pose["focus"][lang])}</p><a href="{href}">{escape(copy["start"])} →</a></div></article>'
        body += f'<section id="type-{code.lower()}"><h2>{escape(names[column])}</h2><div class="reference-grid">{cards}</div></section>'
    body += f'<section><h2>{escape(copy["limit_title"])}</h2><p>{escape(copy["limit"])}</p><a href="/{"zh-tw" if lang=="zh-TW" else lang}/about.html#feedback">{escape({'ko':'자료 문제 제보','ja':'資料の問題を報告','en':'Report a reference issue','zh-TW':'回報素材問題'}[lang])}</a></section>'
    return body
