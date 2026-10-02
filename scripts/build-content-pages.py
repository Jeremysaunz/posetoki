#!/usr/bin/env python3
"""Build crawlable, localized PoseToki information pages."""

from html import escape
from pathlib import Path

from lesson_content import LESSONS, LESSON_SLUGS
from operations_content import OPERATIONS, operation_sections
from discovery_content import COPY as DISCOVERY, EXTRA_SLUGS, render_beginner, render_catalog, load_poses
from seo_common import HOME, metadata, page_schema, byline


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ORIGIN = "https://posetoki.com"
LANGS = {"ko": "ko", "ja": "ja", "en": "en", "zh-TW": "zh-tw"}
NAMES = {"ko": "한국어", "ja": "日本語", "en": "English", "zh-TW": "繁體中文"}
SLUGS = ("guide", "about", "privacy")

COPY = {
    "ko": {
        "a11y": {"skip": "본문으로 건너뛰기", "main_nav": "주요 메뉴", "languages": "언어 선택", "info": "서비스 정보"},
        "nav": {"studio": "연습실", "guide": "크로키 연습법", "about": "서비스 소개", "privacy": "개인정보 안내"},
        "contact": "의견과 오류 제보",
        "contact_note": "GitHub 이슈는 공개됩니다. 개인 사진이나 연락처를 올리지 마세요.",
        "back": "포즈 연습 시작하기",
        "updated": "2026년 10월 2일 업데이트",
        "guide": {
            "title": "짧게 보고, 정확히 관찰하는 크로키 연습법",
            "description": "미술 전공생과 웹툰·일러스트 학습자를 위한 30초·1분·3분 크로키 루틴과 복습 방법.",
            "lead": "크로키는 사진의 윤곽을 빨리 베끼는 경주가 아닙니다. 제한된 시간에 몸의 방향, 무게, 움직임을 골라 보는 연습입니다. 포즈토키의 120개 착의 인물 예시와 타이머로 한 번에 한 가지 관찰 목표를 세워 보세요.",
            "body": """
<section><h2>첫 선은 동작선에서 시작하세요</h2><p>얼굴이나 옷 주름보다 머리에서 몸통을 지나 체중이 실린 발까지 이어지는 큰 흐름을 찾습니다. 척추를 실제 해부학 선처럼 정확히 따라 그리기보다, 몸이 어느 쪽으로 뻗거나 굽는지 한 선으로 요약해 보세요. 움직임이 약한 포즈라면 어깨와 골반의 기울기, 몸의 중심이 어느 발 위에 있는지부터 확인합니다.</p><p>동작선이 보이면 가슴통과 골반을 단순한 덩어리로 놓고, 팔과 다리를 연결합니다. 손가락이나 옷 무늬는 마지막까지 미룹니다. 포즈가 끝났을 때도 전체가 읽히면 이번 연습의 목적을 이룬 셈입니다.</p></section>
<section><h2>30초와 1분을 묶은 10분 루틴</h2><ol><li><strong>30초 × 10포즈, 5분:</strong> 동작선 한 줄과 큰 덩어리 두세 개만 그립니다. 멈춰서 고치기보다 다음 포즈로 넘어갑니다.</li><li><strong>1분 × 5포즈, 5분:</strong> 어깨와 골반의 방향, 체중이 실린 발, 팔·다리의 겹침을 더합니다. 짧은 선 여러 개보다 읽히는 큰 형태를 우선합니다.</li><li><strong>복습:</strong> 연습 종료 화면에서 두 포즈를 골라 ‘무게가 어디에 있는가’와 ‘어느 부위가 앞에 오는가’를 원본과 비교합니다.</li></ol><p>포즈토키에서 먼저 5분 몸풀기 코스를 실행한 뒤, 준비된 포즈 탭에서 1분과 5장을 선택하면 됩니다. 준비 시간과 포즈 전환 때문에 실제 경과 시간은 10분보다 조금 깁니다.</p></section>
<section><h2>3분에는 비례보다 방향을 먼저</h2><p>3분 × 5포즈 코스는 한 자세를 더 천천히 볼 때 유용합니다. 먼저 머리, 가슴통, 골반의 위치를 찍고 어깨선과 골반선이 평행한지 살펴봅니다. 다음으로 팔과 다리의 긴 축을 그립니다. 카메라 쪽으로 다가오는 팔처럼 짧게 보이는 부위는 ‘실제 길이’를 추측해 늘리지 말고 사진에서 보이는 겹침을 기록하세요.</p><p>마지막 30초에 손이나 얼굴로 들어가기 전에 발이 바닥에 닿는 지점과 몸의 중심을 다시 봅니다. 인물이 똑바로 서지 않는다면 어느 부분이 균형을 잡는지 표시해 보세요.</p></section>
<section><h2>웹툰·일러스트 장면으로 연결하기</h2><p>같은 포즈라도 감정과 시점을 바꾸면 다른 장면이 됩니다. 걷는 포즈를 그릴 때는 급히 달려가는 인물인지, 조심스럽게 다가가는 인물인지 정하고 몸통의 기울기와 보폭을 조정해 보세요. 앉은 포즈는 골반의 위치를 먼저 잡고 시점을 높이거나 낮추어 세 컷을 그려보면 원근과 무게 중심을 함께 연습할 수 있습니다.</p><p>따라 그리기가 끝나면 사진을 잠시 가리고 같은 동작을 기억으로 다시 그려 보세요. 관찰한 구조를 자신의 그림 언어로 옮기는 단계입니다.</p></section>
<section><h2>복습할 때 볼 네 가지</h2><ul><li>한 선만 보아도 몸의 진행 방향이 읽히나요?</li><li>어깨와 골반의 기울기가 원본과 비슷한가요?</li><li>체중이 실린 발과 접지점이 분명한가요?</li><li>앞뒤로 겹치는 팔·다리의 순서가 맞나요?</li></ul><p>한 장마다 전부 고치려 하지 말고 다음 세션의 목표 하나를 고르세요. 날짜와 연습 시간을 저장하는 기록 기능은 브라우저 안에서만 작동하며, 그림 자체는 저장하지 않습니다.</p></section>
<section><h2>예시 이미지와 내 사진 사용하기</h2><p>준비된 120개 이미지는 이 서비스를 위해 생성한 AI 착의 인물 예시입니다. 관절이나 손·발 비례가 자연스럽지 않을 수 있으므로 해부학의 정답으로 삼지 말고 관찰 주제로 사용하세요. 실제 사람 사진을 쓰고 싶다면 ‘내 사진’에서 이미지 여러 장을 선택할 수 있습니다. 선택한 파일은 서버로 업로드되지 않고 새로고침하면 목록이 사라집니다. 다른 사람의 사진은 사용 권한을 확인하고, 공개 장소에 무단으로 공유하지 마세요.</p></section>
""",
        },
        "about": {
            "title": "포즈토키 소개",
            "description": "포즈토키는 짧은 인체 크로키 연습을 위한 무료 타이머와 포즈 자료를 제공합니다.",
            "lead": "포즈토키는 사진을 찾고 타이머를 맞추는 준비 시간을 줄여, 그림을 보는 시간에 집중하도록 만든 무료 크로키 연습실입니다.",
            "body": """
<section><h2>누구를 위한 도구인가요?</h2><p>미술 전공생, 웹툰 작가 지망생, 일러스트 학습자, 그리고 짧은 그림 루틴이 필요한 누구나 사용할 수 있습니다. 30초에는 동작을, 1분에는 무게 중심을, 3분에는 비례와 겹침을 관찰하도록 구성했습니다. 회원가입 없이 바로 시작할 수 있습니다.</p></section>
<section><h2>어떤 자료를 쓰나요?</h2><p>연습실에는 이 서비스를 위해 생성한 착의 인물 포즈 예시 120장이 있습니다. 서기, 앉기, 걷기, 몸 비틀기, 균형 잡기처럼 다른 방향과 동작을 담았습니다. 모두 AI 생성 이미지이며 인체 구조가 부정확한 부분이 있을 수 있습니다. 자료는 참고용이고 해부학 교재를 대신하지 않습니다.</p><p>직접 소유하거나 사용 권한이 있는 사진을 골라 연습할 수도 있습니다. 선택한 파일은 브라우저 안에서만 표시되고 서버로 보내지지 않습니다.</p></section>
<section><h2>어떻게 사용하나요?</h2><p>준비된 포즈 또는 내 사진을 선택하고, 포즈당 시간과 연습할 장수를 고른 뒤 시작합니다. 일시정지, 이전·다음, 좌우 반전, 확대와 전체 화면을 사용할 수 있습니다. 종료 후에는 본 포즈를 다시 볼 수 있고, 날짜·시간·포즈 수와 선택한 다음 연습 목표를 이 브라우저에 기록합니다. 그림 파일이나 선택한 사진은 기록에 포함되지 않습니다.</p></section>
""",
        },
        "privacy": {
            "title": "개인정보 및 데이터 이용 안내",
            "description": "포즈토키의 사진 처리, 브라우저 저장 기록, 외부 서비스와 광고 관련 데이터 이용 안내.",
            "lead": "포즈토키는 회원가입 없이 사용할 수 있습니다. 이 안내는 현재 공개된 사이트에서 사진과 연습 기록이 어떻게 처리되는지 설명합니다.",
            "body": """
<section><h2>내 사진</h2><p>사용자가 선택한 이미지 파일은 브라우저의 임시 주소로 표시됩니다. 포즈토키는 이 파일을 자체 서버에 업로드하지 않으며, 연습 기록에도 파일이나 파일명을 저장하지 않습니다. 새로고침하거나 페이지를 닫으면 선택한 사진 목록은 사라집니다. 사용 권한이 없는 타인의 사진이나 민감한 이미지를 선택하지 않는 것이 좋습니다.</p></section>
<section><h2>이 기기에 저장되는 정보</h2><p>언어와 라이트·다크 모드 선택은 브라우저의 <code>localStorage</code>에 저장됩니다. 연습을 마치면 날짜, 실제 연습 시간, 관찰한 포즈 수를 최대 100회까지 같은 브라우저에 저장합니다. 계정이나 기기 간 동기화는 없고, 그림 파일은 저장하지 않습니다. 선택한 다음 연습 목표와 최근 관찰한 예시 포즈 번호(최대 120개)도 이 브라우저에만 저장합니다. 포즈 번호는 반복을 줄이는 데 사용합니다. 기록을 삭제하려면 브라우저의 해당 사이트 데이터를 지우면 됩니다.</p></section>
<section><h2>호스팅과 외부 요청</h2><p>사이트는 Vercel에서 제공됩니다. 페이지 요청 과정에서 IP 주소, 브라우저 정보 등 일반적인 접속 정보가 호스팅·보안 목적으로 처리될 수 있습니다. 홈페이지 글꼴은 Google Fonts에서 불러오므로 글꼴 요청 시 접속 정보가 해당 서비스에 전달될 수 있습니다. 공개 GitHub 이슈 링크를 선택하면 GitHub의 별도 정책이 적용됩니다.</p></section>
<section><h2>광고와 쿠키</h2><p>Google AdSense 연결 및 광고용 코드가 설치되어 있습니다. 광고 표시 여부는 Google의 사이트 승인과 광고 설정에 따라 달라집니다. 코드가 로드될 때 IP 주소, 브라우저·기기 정보 등이 Google에 전달될 수 있고, 광고 서비스가 쿠키나 식별자를 사용할 수 있습니다. 자체 방문 분석 도구는 설치되어 있지 않습니다. Google의 데이터 처리와 광고 선택권은 <a href="https://policies.google.com/technologies/ads" rel="noopener noreferrer">Google 광고 안내</a>와 <a href="https://myadcenter.google.com/" rel="noopener noreferrer">내 광고 센터</a>에서 확인할 수 있습니다. 해당 지역에서 요구되는 광고 동의 설정은 광고 운영 시 적용해야 합니다.</p></section>
<section><h2>문의와 변경</h2><p>기록 삭제 또는 데이터 이용에 관한 의견은 <a href="https://github.com/Jeremysaunz/posetoki/issues/new" rel="noopener noreferrer">공개 GitHub 이슈</a>로 남길 수 있습니다. 공개 게시물이므로 사진이나 연락처 등 민감한 정보는 올리지 마세요. 기능이나 외부 서비스가 바뀌면 이 페이지의 날짜와 내용을 업데이트합니다.</p></section>
""",
        },
    },
    "ja": {
        "a11y": {"skip": "本文へスキップ", "main_nav": "メインメニュー", "languages": "言語を選ぶ", "info": "サービス情報"},
        "nav": {"studio": "練習室", "guide": "クロッキーの練習法", "about": "サービスについて", "privacy": "プライバシー"},
        "contact": "ご意見・不具合の報告",
        "contact_note": "GitHub Issue は公開されます。個人の写真や連絡先を投稿しないでください。",
        "back": "ポーズ練習を始める",
        "updated": "2026年10月2日更新",
        "guide": {
            "title": "短時間で観察するクロッキーの練習法",
            "description": "美術学生・漫画・イラスト学習者向けの30秒、1分、3分のクロッキー練習と振り返り。",
            "lead": "クロッキーは輪郭を急いでなぞる競争ではありません。限られた時間で身体の向き、重心、動きを見つける練習です。PoseToki の服を着た人物のサンプル120枚とタイマーを使い、毎回ひとつの観察目標を決めましょう。",
            "body": """
<section><h2>最初の線は動きの流れから</h2><p>顔や服のしわより先に、頭から胴体を通り、体重を支える足へ続く大きな流れを探します。背骨を正確になぞる必要はありません。身体がどちらに伸び、曲がっているかを一本の線に要約してみてください。静かなポーズでは肩と骨盤の傾き、重心がどちらの足にあるかを見ます。</p><p>動きの線が決まったら、胸郭と骨盤を単純な塊にして腕と脚をつなぎます。指や服の模様は最後まで後回しにします。細部がなくても姿勢が伝われば、今回の目的は達成できています。</p></section>
<section><h2>30秒と1分を組み合わせた10分練習</h2><ol><li><strong>30秒 × 10ポーズ、5分：</strong>動きの線一本と大きな形を二、三個だけ描きます。途中で直し続けず、次のポーズへ進みます。</li><li><strong>1分 × 5ポーズ、5分：</strong>肩と骨盤の向き、体重の乗る足、手足の前後関係を加えます。</li><li><strong>振り返り：</strong>終了画面から二つ選び、「重さはどこにあるか」「どの部分が手前か」を元画像と比べます。</li></ol><p>まず「5分のウォームアップ」を実行し、次に練習室で1分・5ポーズを選ぶと試せます。準備時間と切り替えがあるため、実際の経過時間は10分を少し超えます。</p></section>
<section><h2>3分では細部より向きを確認</h2><p>3分 × 5ポーズのコースでは、まず頭、胸郭、骨盤の位置を置き、肩の線と骨盤の線の角度を見ます。その後、腕と脚の長い軸を引きます。カメラに向かって伸びる腕は、実際の長さを想像して伸ばさず、写真に見える短縮と重なりを記録してください。</p><p>最後の30秒は顔や指に入る前に、足が床に触れる場所と身体の中心をもう一度確認します。</p></section>
<section><h2>漫画やイラストの一場面につなげる</h2><p>同じ歩く姿勢でも、急いでいる人物と慎重に近づく人物では胴体の傾きや歩幅が変わります。座る姿勢では骨盤の位置を決め、視点を上・正面・下に変えて三コマ描いてみましょう。遠近感と重心を同時に練習できます。</p><p>模写の後に画像を隠し、記憶だけで同じ動きを描き直すと、観察した構造を自分の絵に移す練習になります。</p></section>
<section><h2>見直す四つのポイント</h2><ul><li>一本の線だけで身体の動く方向が読めるか。</li><li>肩と骨盤の傾きが元画像に近いか。</li><li>体重を支える足と接地点が明確か。</li><li>重なる腕や脚の前後関係が合っているか。</li></ul><p>一枚ごとにすべて直すのではなく、次回の目標をひとつ選びましょう。練習記録は日付・時間・見たポーズ数だけをブラウザに保存し、絵自体は保存しません。</p></section>
<section><h2>サンプル画像と自分の写真</h2><p>120枚のサンプルはこのサービスのために生成した AI の人物画像です。関節や手足の比率が不自然な場合もあるため、解剖学の正解ではなく観察用の題材として使ってください。「自分の写真」では複数の画像を選べます。ファイルはサーバーに送信されず、再読み込みすると一覧が消えます。他人の写真は使用権を確認し、許可なく公開しないでください。</p></section>
""",
        },
        "about": {
            "title": "PoseToki について",
            "description": "PoseToki は短時間の人物クロッキー向けに無料のタイマーとポーズ素材を提供します。",
            "lead": "PoseToki は写真探しとタイマー設定の手間を減らし、観察と描画に集中するための無料練習室です。",
            "body": """
<section><h2>誰のための練習室？</h2><p>美術学生、漫画家を目指す人、イラスト学習者、短い練習を習慣にしたい人のために作りました。30秒では動き、1分では重心、3分では比率と重なりを見る構成です。登録せずにすぐ始められます。</p></section>
<section><h2>素材について</h2><p>服を着た人物のポーズサンプル120枚をこのサービスのために生成しました。立つ・座る・歩く・ひねる・バランスを取るなど、さまざまな動きがあります。すべて AI 生成画像で、身体の構造が正確でない部分もあり得ます。解剖学の教材として扱わず、観察のきっかけとして使ってください。</p><p>使用権のある写真を選んで練習することもできます。ファイルはブラウザ内に留まり、サーバーに送信されません。</p></section>
<section><h2>使い方</h2><p>用意されたポーズか自分の写真を選び、一枚の時間と枚数を設定して始めます。一時停止、前後移動、左右反転、拡大、全画面が使えます。終了後は見たポーズを確認できます。日付・時間・枚数と選んだ次回の目標をブラウザに記録し、絵や写真は保存しません。</p></section>
""",
        },
        "privacy": {
            "title": "プライバシーとデータ利用について",
            "description": "PoseToki の写真、ブラウザ内の練習記録、外部サービス、広告に関する案内。",
            "lead": "PoseToki は登録なしで利用できます。このページでは、現在公開しているサイトが写真と練習記録をどう扱うかを説明します。",
            "body": """
<section><h2>自分の写真</h2><p>選択した画像はブラウザの一時 URL で表示します。ファイルを PoseToki のサーバーにアップロードせず、練習記録にもファイルやファイル名を保存しません。再読み込みやページを閉じると選択一覧は消えます。権利のない他人の写真や機微な画像の使用は避けてください。</p></section>
<section><h2>端末に保存する情報</h2><p>言語とライト・ダークモード設定をブラウザの <code>localStorage</code> に保存します。練習後は日付、実際の練習時間、見たポーズ数を最大100回分保存します。アカウントや端末間の同期はなく、絵は保存されません。選んだ次回の目標と最近見たサンプルの番号（最大120個）も、このブラウザにだけ保存します。番号は繰り返しを減らすために使います。削除するにはブラウザのこのサイトのデータを消去してください。</p></section>
<section><h2>ホスティングと外部通信</h2><p>サイトは Vercel で提供しています。配信やセキュリティのため、IP アドレスやブラウザ情報などの一般的な接続情報が処理される場合があります。ホームページのフォントは Google Fonts から読み込むため、接続情報が同サービスに送られる場合があります。GitHub Issue のリンクを開くと GitHub の別のポリシーが適用されます。</p></section>
<section><h2>広告と Cookie</h2><p>Google AdSense の接続・広告用コードを設置しています。広告表示は Google のサイト承認と広告設定により異なります。コードの読み込み時に IP アドレス、ブラウザ・端末情報などが Google に送信され、広告サービスが Cookie や識別子を利用する場合があります。独自のアクセス解析は設置していません。データの取扱いと選択肢は <a href="https://policies.google.com/technologies/ads" rel="noopener noreferrer">Google の広告案内</a>と<a href="https://myadcenter.google.com/" rel="noopener noreferrer">マイ アド センター</a>を確認してください。広告運営時には対象地域で必要な同意設定を適用する必要があります。</p></section>
<section><h2>お問い合わせと変更</h2><p>データの取扱いに関するご意見は <a href="https://github.com/Jeremysaunz/posetoki/issues/new" rel="noopener noreferrer">公開 GitHub Issue</a> に投稿できます。個人の写真や連絡先は投稿しないでください。機能や外部サービスが変われば、このページの日付と内容を更新します。</p></section>
""",
        },
    },
    "en": {
        "a11y": {"skip": "Skip to content", "main_nav": "Main navigation", "languages": "Choose a language", "info": "Site information"},
        "nav": {"studio": "Studio", "guide": "Drawing guide", "about": "About", "privacy": "Privacy"},
        "contact": "Feedback and bug reports",
        "contact_note": "GitHub issues are public. Please do not post personal photos or contact details.",
        "back": "Start a pose session",
        "updated": "Updated October 2, 2026",
        "guide": {
            "title": "A practical guide to short gesture drawing sessions",
            "description": "A 30-second, 1-minute, and 3-minute croquis routine for art students, comic artists, and illustrators.",
            "lead": "Gesture drawing is not a race to trace every edge of a photograph. It trains you to notice direction, weight, and movement before detail. Use PoseToki's 120 clothed figure samples and timer to give each session one clear observation goal.",
            "body": """
<section><h2>Begin with the line of action</h2><p>Before the face or clothing folds, look for a broad path from the head through the torso toward the foot that carries the weight. This is a summary of motion, not a literal anatomical outline of the spine. In a quiet standing pose, compare the angle of the shoulders and pelvis and ask which foot supports the body.</p><p>Once that flow is clear, place the rib cage and pelvis as simple masses. Connect the arms and legs to those masses. Leave fingers, hair, and costume details until the pose reads as a whole. A drawing that communicates the direction of the body with a few lines has met its first goal.</p></section>
<section><h2>A ten-minute routine that matches the studio</h2><ol><li><strong>30 seconds × 10 poses, five minutes:</strong> Draw one action line and two or three large masses. Move on rather than repeatedly repairing a single sketch.</li><li><strong>One minute × five poses, five minutes:</strong> Add shoulder and pelvis direction, the supporting foot, and the order of overlapping limbs.</li><li><strong>Review:</strong> Choose two poses on the finish screen. Compare where the weight sits and which limb is closest to the viewer.</li></ol><p>Run the 5-minute warm-up plan, then choose one minute and five poses in the prepared-pose studio. The three-second preparation and transitions make the elapsed time slightly longer than ten minutes.</p></section>
<section><h2>Use three minutes to study direction before detail</h2><p>The three-minute plan gives you time to study a pose without losing its overall movement. Place the head, rib cage, and pelvis first. Compare the angle of the shoulder line with the pelvis line. Add the long axes of the arms and legs. If an arm points toward the camera, record the visible overlap and foreshortening rather than lengthening it to the size you know it has in real life.</p><p>Before drawing the face or fingers, check where the feet meet the floor and whether the centre of mass still makes sense.</p></section>
<section><h2>Turn a study into a comic or illustration scene</h2><p>A walking pose can suggest urgency or caution. Decide which story you want to tell, then change the torso tilt and stride to support it. For a seated pose, anchor the pelvis and try three small panels from a high, level, and low camera angle. This makes perspective and balance part of the same exercise.</p><p>After copying from observation, hide the reference and draw the action again from memory. This step helps turn a pose study into a structure you can use in your own characters.</p></section>
<section><h2>Four questions for a useful review</h2><ul><li>Can one line communicate the body's direction?</li><li>Do the shoulder and pelvis tilts resemble the reference?</li><li>Is the supporting foot and its contact with the ground clear?</li><li>Are the overlapping arms and legs in the right order?</li></ul><p>Pick one issue for the next session instead of correcting everything in every drawing. PoseToki stores session date, time, and pose count in this browser; it does not save your drawings.</p></section>
<section><h2>About the sample images and your photos</h2><p>The 120 prepared images are AI-generated clothed figure references created for this service. Hands, joints, or proportions may contain errors. Treat them as prompts for observation rather than anatomical authority. You can choose several of your own photos in the My Photos tab. Those files are not uploaded to a server and disappear from the selection after a reload. Check your right to use someone else's image, and do not publish it without permission.</p></section>
""",
        },
        "about": {
            "title": "About PoseToki",
            "description": "PoseToki is a free gesture drawing studio with a pose timer, 120 clothed figure samples, and local photo practice.",
            "lead": "PoseToki is a free practice room built to reduce setup time so you can spend more time observing and drawing.",
            "body": """
<section><h2>Who is it for?</h2><p>Art students, aspiring comic artists, illustration learners, and anyone building a short drawing habit can use PoseToki. The timer supports 30-second studies of movement, one-minute studies of balance, and longer studies of proportion and overlap. You can begin without creating an account.</p></section>
<section><h2>What references are available?</h2><p>The studio includes 120 clothed figure pose samples generated for this service: standing, sitting, walking, bending, twisting, and balancing. All are AI-generated. Some details of anatomy may be inaccurate, so use them as observation prompts rather than an anatomy textbook. You can also practise with photos you own or have permission to use. Selected files stay in your browser and are not uploaded to our server.</p></section>
<section><h2>How does a session work?</h2><p>Select prepared poses or your own photos, choose a duration and pose count, then start. Pause, move backward or forward, mirror, zoom, or use full screen as needed. After finishing, review the poses you saw. The date, elapsed drawing time, observed pose count and your chosen next-session goal are saved in this browser. Drawings and selected photos are not part of the log.</p></section>
""",
        },
        "privacy": {
            "title": "Privacy and data use",
            "description": "How PoseToki handles selected photos, browser-stored practice records, hosting requests, and advertising.",
            "lead": "PoseToki works without an account. This notice describes how the current site handles selected photos and practice records.",
            "body": """
<section><h2>Your photos</h2><p>Images you select are displayed through temporary browser URLs. PoseToki does not upload the files to its server or store the files or file names in your practice log. The selection disappears when you reload or close the page. Avoid using sensitive images or photographs you do not have permission to use.</p></section>
<section><h2>Data saved on your device</h2><p>Your language and light/dark mode choices are kept in browser <code>localStorage</code>. When you finish a session, the date, actual drawing time, and number of poses observed are stored for up to 100 sessions in the same browser. There is no account or cross-device sync, and drawings are not saved. Your chosen next-session goal and up to 120 recently viewed sample IDs also stay in this browser. These IDs help reduce repeats. Clear this site's browser data to remove these records.</p></section>
<section><h2>Hosting and external requests</h2><p>Vercel serves the site. Ordinary connection data, such as IP address and browser information, may be processed for delivery and security. The homepage loads fonts from Google Fonts, which may receive connection information with font requests. If you follow the public GitHub issues link, GitHub's own policies apply there.</p></section>
<section><h2>Advertising and cookies</h2><p>Google AdSense site-connection and advertising code is installed. Whether ads appear depends on Google’s site approval and ad settings. Loading the code may send an IP address and browser or device information to Google; advertising services may use cookies or identifiers. No first-party visitor analytics is installed. See <a href="https://policies.google.com/technologies/ads" rel="noopener noreferrer">Google’s advertising information</a> and <a href="https://myadcenter.google.com/" rel="noopener noreferrer">My Ad Center</a> for data handling and choices. Required regional ad-consent settings need to be applied when operating ads.</p></section>
<section><h2>Questions and changes</h2><p>You may leave data-use feedback through a <a href="https://github.com/Jeremysaunz/posetoki/issues/new" rel="noopener noreferrer">public GitHub issue</a>. Do not post private photos or contact information there. If the site's features or external services change, we will update this page and its date.</p></section>
""",
        },
    },
    "zh-TW": {
        "a11y": {"skip": "跳至主要內容", "main_nav": "主要選單", "languages": "選擇語言", "info": "網站資訊"},
        "nav": {"studio": "練習室", "guide": "速寫練習指南", "about": "關於本站", "privacy": "隱私說明"},
        "contact": "意見與錯誤回報",
        "contact_note": "GitHub Issue 是公開的，請勿張貼私人照片或聯絡方式。",
        "back": "開始姿勢練習",
        "updated": "2026 年 10 月 2 日更新",
        "guide": {
            "title": "短時間觀察的人物速寫練習指南",
            "description": "給美術學生、漫畫與插畫學習者的 30 秒、1 分鐘與 3 分鐘姿勢速寫練習。",
            "lead": "人物速寫不是搶快描出照片的每條外輪廓，而是在有限時間裡找出身體的方向、重量與動勢。使用 PoseToki 的 120 張著衣人物範例和計時器，每次先訂一個觀察目標。",
            "body": """
<section><h2>第一筆先畫動勢線</h2><p>先別急著畫臉或衣服皺褶，找出從頭部經過軀幹、通往承重腳的大致流向。動勢線是對動作的摘要，不必精確描出脊椎。在靜止的站姿裡，可先比較肩膀與骨盆的傾斜方向，再看重心落在哪一隻腳上。</p><p>看清流向後，把胸廓和骨盆簡化成兩個大形，再接上手腳。手指、髮絲和服裝細節留到最後。即使沒有細節，只要姿勢能被讀懂，這張練習就達成了第一個目的。</p></section>
<section><h2>符合練習室設定的十分鐘安排</h2><ol><li><strong>30 秒 × 10 個姿勢，共 5 分鐘：</strong>每張只畫一條動勢線與兩三個大形，不要一直停下來修同一張。</li><li><strong>1 分鐘 × 5 個姿勢，共 5 分鐘：</strong>加入肩膀、骨盆的方向、承重腳，以及手腳的前後交疊。</li><li><strong>回顧：</strong>結束後挑兩張照片，比較重量落點與哪個肢體更靠近鏡頭。</li></ol><p>先使用「5 分鐘暖身」課程，再到練習室選擇每張 1 分鐘、共 5 張。加上三秒準備與切換，實際經過時間會稍長於十分鐘。</p></section>
<section><h2>三分鐘先看方向，再看細節</h2><p>三分鐘課程可以讓你放慢速度，但仍要保留整體動勢。先定位頭部、胸廓與骨盆，比較肩線和骨盆線的角度，再畫出手腳的長軸。若手臂朝鏡頭伸出，請記錄照片裡看到的縮短與遮擋，不要依照你認為的真實長度把它拉長。</p><p>畫臉和手指之前，再檢查腳與地面接觸的位置，以及身體的重心是否合理。</p></section>
<section><h2>把練習轉成漫畫與插畫場景</h2><p>同一個走路姿勢可以表現匆忙，也可以表現小心接近。先決定情緒，再改變軀幹傾斜與步幅。畫坐姿時先固定骨盆位置，試著從俯視、平視、仰視各畫一小格，便能同時練習透視和重量。</p><p>照著參考圖畫完後，暫時遮住圖片，憑記憶再畫一次同樣的動作。這一步有助於把觀察到的結構轉成自己的角色表現。</p></section>
<section><h2>回顧時問自己四件事</h2><ul><li>只看一條線，能讀出身體的動作方向嗎？</li><li>肩膀與骨盆的傾斜是否接近參考圖？</li><li>承重腳與接地點是否清楚？</li><li>互相遮擋的手腳前後順序是否正確？</li></ul><p>每次只挑一個問題作為下次目標，不必修完所有細節。練習紀錄僅在瀏覽器保存日期、時間與姿勢數，不保存你的畫作。</p></section>
<section><h2>範例圖片與自己的照片</h2><p>120 張內建圖片是為本服務生成的 AI 著衣人物範例。關節、手腳或比例可能有錯誤，請把它們當作觀察題材，而非人體解剖的標準答案。「我的照片」可選取多張自己的圖片；檔案不會上傳伺服器，重新整理後選取清單便會消失。使用他人的照片前請確認權利，勿未經同意公開分享。</p></section>
""",
        },
        "about": {
            "title": "關於 PoseToki",
            "description": "PoseToki 提供免費姿勢計時器、120 張著衣人物範例，以及只在瀏覽器處理的個人照片練習。",
            "lead": "PoseToki 是一間免費的速寫練習室，減少找照片和設定計時器的時間，讓你專注觀察與繪畫。",
            "body": """
<section><h2>適合誰使用？</h2><p>美術學生、漫畫創作者、插畫學習者，以及想培養短時間繪畫習慣的人，都可以使用。30 秒觀察動勢，1 分鐘觀察重心，較長的練習則留意比例與遮擋。不必註冊就能開始。</p></section>
<section><h2>有哪些參考素材？</h2><p>練習室有 120 張為本服務生成的著衣人物姿勢，包含站立、坐下、行走、彎身、扭轉與平衡。它們都是 AI 生成圖片，部分人體結構可能不準確。請用來啟動觀察，而非代替解剖教材。你也可以選擇自己擁有或獲准使用的照片；選取的檔案只留在瀏覽器，不會上傳本站伺服器。</p></section>
<section><h2>如何練習？</h2><p>選擇內建姿勢或自己的照片，設定每張時間與張數後開始。可以暫停、切換前後姿勢、左右反轉、放大或全螢幕觀看。結束後可回看見過的姿勢。本站在此瀏覽器記錄日期、實際練習時間、姿勢數與選定的下次目標，不保存畫作或選取的照片。</p></section>
""",
        },
        "privacy": {
            "title": "隱私與資料使用說明",
            "description": "PoseToki 如何處理選取的照片、瀏覽器中的練習紀錄、外部請求與廣告。",
            "lead": "PoseToki 不需帳號即可使用。本頁說明目前公開網站如何處理你選取的照片與練習紀錄。",
            "body": """
<section><h2>你的照片</h2><p>選取的圖片透過瀏覽器暫時網址顯示。PoseToki 不會將檔案上傳到本站伺服器，也不會把檔案或檔名存進練習紀錄。重新整理或關閉頁面後，選取清單便會消失。請避免使用敏感圖片或未獲授權的他人照片。</p></section>
<section><h2>存在裝置上的資訊</h2><p>語言與淺色／深色模式選擇儲存在瀏覽器的 <code>localStorage</code>。練習結束後，日期、實際繪畫時間和看過的姿勢數最多保存 100 次於同一瀏覽器。沒有帳號或跨裝置同步，也不保存畫作。選定的下次目標與最近看過的範例編號（最多 120 個）也只保存在此瀏覽器，用於減少重複。清除此網站的瀏覽器資料即可刪除紀錄。</p></section>
<section><h2>託管與外部連線</h2><p>網站由 Vercel 提供。為了傳送頁面及維護安全，IP 位址、瀏覽器資訊等一般連線資料可能會被處理。首頁字型由 Google Fonts 載入，字型請求可能向該服務傳送連線資訊。前往公開 GitHub Issue 時，則適用 GitHub 自身的政策。</p></section>
<section><h2>廣告與 Cookie</h2><p>本站已安裝 Google AdSense 的網站連結及廣告程式碼。是否顯示廣告取決於 Google 的網站核准與廣告設定。載入程式碼時，IP 位址、瀏覽器或裝置資訊可能傳送至 Google；廣告服務可能使用 Cookie 或識別資料。本站未安裝自行設置的流量分析工具。資料處理與廣告選擇可參考 <a href="https://policies.google.com/technologies/ads" rel="noopener noreferrer">Google 廣告說明</a>及<a href="https://myadcenter.google.com/" rel="noopener noreferrer">我的廣告中心</a>。營運廣告時需套用適用地區要求的同意設定。</p></section>
<section><h2>問題與更新</h2><p>資料使用方面的意見可透過<a href="https://github.com/Jeremysaunz/posetoki/issues/new" rel="noopener noreferrer">公開 GitHub Issue</a>提出。請勿張貼私人照片或聯絡方式。網站功能或外部服務變更時，本頁日期和內容也會更新。</p></section>
""",
        },
    },
}


def page_url(lang: str, slug: str) -> str:
    return f"{ORIGIN}/{LANGS[lang]}/{slug}.html"


def page_href(lang: str, slug: str) -> str:
    return f"/{LANGS[lang]}/{slug}.html"


def lesson_index(lang: str, current: str | None = None) -> str:
    copy = LESSONS[lang]
    cards = "".join(
        f'<a class="lesson-card" href="{page_href(lang, slug)}">'
        f'<strong>{escape(copy[slug]["title"])}</strong>'
        f'<span>{escape(copy[slug]["description"])}</span></a>'
        for slug in LESSON_SLUGS if slug != current
    )
    return (
        f'<section class="lesson-index" aria-label="{escape(copy["index_title"], quote=True)}">'
        f'<h2>{escape(copy["index_title"] if current is None else copy["related"])}</h2>'
        + (f'<p>{escape(copy["index_intro"])}</p>' if current is None else '')
        + f'<div class="lesson-cards">{cards}</div></section>'
    )


def render_lesson(lang: str, slug: str) -> str:
    copy = LESSONS[lang]
    lesson = copy[slug]
    photo, alt, caption = lesson["primary"]
    second_photo, second_alt, second_caption = lesson["secondary"]
    markers = "".join(
        f'<span class="photo-marker" style="left:{x}%;top:{y}%" aria-hidden="true">{i}</span>'
        for i, (x, y) in enumerate(lesson["markers"], 1)
    )
    focus = "".join(f'<li>{escape(item)}</li>' for item in lesson["focus"])
    timing = "".join(
        f'<li><strong>{escape(label)}</strong><p>{escape(task)}</p></li>'
        for label, task in zip(copy["times"], lesson["timing"])
    )
    review = "".join(f'<li>{escape(item)}</li>' for item in lesson["review"])
    practice_settings = {
        "gesture": ("PT014", 30, "WK"),
        "balance": ("PT001", 60, "ST"),
        "seated": ("PT049", 180, "CH"),
    }
    pose, seconds, category = practice_settings[slug]
    practice_href = f"{HOME[lang]}?poseId={pose}&amp;seconds={seconds}&amp;count=5&amp;category={category}#practice"
    return f"""
<div class="lesson-example">
  <figure class="lesson-photo"><div class="photo-frame"><img src="/assets/{photo}" width="768" height="1536" loading="lazy" decoding="async" alt="{escape(alt, quote=True)}">{markers}</div><figcaption>{escape(caption)}</figcaption></figure>
  <div class="focus-card"><h2>{escape(copy['focus_title'])}</h2><ol>{focus}</ol></div>
</div>
<p class="source-note">{escape(copy['source_note'])}</p>
<section><h2>{escape(copy['timing_title'])}</h2><ol class="timing-list">{timing}</ol></section>
<section><h2>{escape(copy['mistake_title'])}</h2><p>{escape(lesson['mistake'])}</p></section>
<section><h2>{escape(copy['transfer_title'])}</h2><div class="transfer-example"><figure class="lesson-photo secondary-photo"><img src="/assets/{second_photo}" width="768" height="1536" loading="lazy" decoding="async" alt="{escape(second_alt, quote=True)}"><figcaption>{escape(second_caption)}</figcaption></figure><p>{escape(lesson['transfer'])}</p></div></section>
<section><h2>{escape(copy['review_title'])}</h2><ul>{review}</ul></section>
<section class="practice-callout"><h2>{escape(copy['practice_title'])}</h2><p>{escape(lesson['practice'])}</p><a class="primary" href="{practice_href}">{escape(COPY[lang]['back'])} →</a></section>
"""


def render(lang: str, slug: str) -> str:
    copy = COPY[lang]
    article = DISCOVERY[lang][slug] if slug in EXTRA_SLUGS else copy[slug] if slug in SLUGS else LESSONS[lang][slug]
    operation = OPERATIONS[lang]
    title = operation["title"] if slug == "about" else article["title"]
    body = render_beginner(lang) if slug == 'beginner' else render_catalog(lang) if slug == 'poses' else article["body"] if slug in SLUGS else render_lesson(lang, slug)
    if slug == "about":
        before, after = operation_sections(lang)
        body = before + body + after
    elif slug == "privacy":
        body = f'<p>{escape(operation["privacy_operator"])}</p>' + body
    if slug == "guide" or slug in LESSON_SLUGS or slug == 'beginner':
        body += lesson_index(lang, slug if slug in LESSON_SLUGS else None)
    if slug != 'privacy':
        body += f'<section><h2>{escape(DISCOVERY[lang]["nav"][0])}</h2><p><a href="{page_href(lang, "beginner")}">{escape(DISCOVERY[lang]["beginner"]["title"])}</a> · <a href="{page_href(lang, "poses")}">{escape(DISCOVERY[lang]["nav"][1])}</a></p></section>' if slug != 'beginner' else f'<p><a href="{page_href(lang, "poses")}">{escape(DISCOVERY[lang]["nav"][1])} →</a></p>'
    lesson_style = '<link rel="stylesheet" href="/lesson.css?v=1">'
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{code}" href="{page_url(code, slug)}">'
        for code in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{page_url("ko", slug)}">'
    languages = "".join(
        f'<a href="{page_href(code, slug)}" hreflang="{code}" lang="{code}"'
        + (' aria-current="page"' if code == lang else '')
        + f'>{NAMES[code]}</a>'
        for code in LANGS
    )
    nav = "".join(
        f'<a href="{page_href(lang, item)}"'
        + (' aria-current="page"' if item == slug else '')
        + f'>{escape(operation["nav"] if item == "about" else copy["nav"][item])}</a>'
        for item in SLUGS
    )
    nav += f'<a href="{page_href(lang, "poses")}">{escape(DISCOVERY[lang]["nav"][1])}</a>'
    image = '/assets/' + LESSONS[lang][slug]['primary'][0] if slug in LESSON_SLUGS else '/assets/pose-01.jpg'
    kind = 'Article' if slug in ('guide', 'beginner', *LESSON_SLUGS) else 'CollectionPage' if slug == 'poses' else 'AboutPage' if slug == 'about' else 'WebPage'
    items = [{'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'ImageObject', 'name': p['name'][lang], 'description': p['focus'][lang], 'contentUrl': ORIGIN + p['image'], 'url': page_url(lang, slug) + '#' + p['id']}} for i, p in enumerate(load_poses())] if slug == 'poses' else None
    seo = metadata(lang, title + ' | PoseToki', article['description'], page_url(lang, slug), image, 'article' if kind == 'Article' else 'website') + '\n' + page_schema(lang, slug, title, article['description'], image, kind, items)
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | PoseToki</title>
<meta name="description" content="{escape(article['description'], quote=True)}">
<meta name="google-adsense-account" content="ca-pub-5987896746147751">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5987896746147751" crossorigin="anonymous"></script>
<link rel="canonical" href="{page_url(lang, slug)}">
{alternates}
{seo}
<link rel="icon" type="image/svg+xml" href="/assets/rabbit-mark.svg">
<link rel="stylesheet" href="/content.css?v=3">
{lesson_style}
</head><body>
<a class="skip" href="#content">{escape(copy['a11y']['skip'])}</a>
<header class="site-header"><div class="shell top"><a class="brand" href="{HOME[lang]}"><img class="brand-mark" src="/assets/rabbit-mark.svg" alt=""> <strong>PoseToki</strong></a><nav aria-label="{escape(copy['a11y']['main_nav'])}"><a href="{HOME[lang]}">{escape(copy['nav']['studio'])}</a>{nav}</nav></div></header>
<main class="shell" id="content"><div class="language-links" aria-label="{escape(copy['a11y']['languages'])}">{languages}</div>
<article class="{'catalog-article' if slug == 'poses' else 'lesson-article' if slug in LESSON_SLUGS else ''}"><p class="eyebrow">PoseToki · {escape(operation['nav'] if slug == 'about' else copy['nav'].get(slug, copy['nav']['guide']))}</p><h1>{escape(title)}</h1><p class="lead">{escape(article['lead'])}</p>{byline(lang)}<p class="updated"><time datetime="2026-10-02">{escape(copy['updated'])}</time></p>{body}</article>
<div class="next"><a class="primary" href="{HOME[lang]}">{escape(copy['back'])} →</a></div></main>
<footer><div class="shell footer-inner"><div><a class="brand" href="{HOME[lang]}"><img class="brand-mark" src="/assets/rabbit-mark.svg" alt=""> <strong>PoseToki</strong></a><small class="operator-note">{escape(operation['operator'])}</small></div><nav aria-label="{escape(copy['a11y']['info'])}">{nav}</nav><div class="contact"><a href="{page_href(lang, 'about')}#feedback">{escape(copy['contact'])}</a><small>{escape(copy['contact_note'])}</small></div></div></footer>
<script>try{{localStorage.setItem('posetoki-lang',document.documentElement.lang)}}catch{{}}</script>
</body></html>
"""


def main() -> None:
    urls = [ORIGIN + href for href in HOME.values()]
    for lang, path in LANGS.items():
        target = DIST / path
        target.mkdir(parents=True, exist_ok=True)
        for slug in (*SLUGS, *LESSON_SLUGS, *EXTRA_SLUGS):
            (target / f"{slug}.html").write_text(render(lang, slug), encoding="utf-8")
            urls.append(page_url(lang, slug))
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
    for url in urls:
        images = ''.join(f'<image:image><image:loc>{ORIGIN}{p["image"]}</image:loc></image:image>' for p in load_poses()) if url == page_url('ko', 'poses') else ''
        sitemap += f'  <url><loc>{url}</loc><lastmod>2026-10-02</lastmod>{images}</url>\n'
    sitemap += "</urlset>\n"
    (DIST / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (DIST / "robots.txt").write_text(
        '# Public search and AI discovery are permitted.\n'
        'User-agent: OAI-SearchBot\nAllow: /\n\n'
        'User-agent: ChatGPT-User\nAllow: /\n\n'
        '# This token covers Gemini grounding and model training, not Search rankings.\n'
        'User-agent: Google-Extended\nAllow: /\n\n'
        f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n', encoding="utf-8"
    )


if __name__ == "__main__":
    main()
