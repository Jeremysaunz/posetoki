"""Localized, factual operating information for PoseToki."""

from html import escape
from urllib.parse import urlencode


OPERATIONS = {
    "ko": {
        "nav": "소개·운영 안내", "title": "포즈토키 소개·운영 안내",
        "operator": "운영: 제레미", "operator_title": "제레미가 만들고 운영합니다",
        "purpose": "포즈토키는 제레미가 기획·제작하고 운영하는 무료 크로키 연습 서비스입니다. 미술 전공생과 웹툰·일러스트 학습자, 취미로 그림을 그리는 사람들이 사진을 찾고 타이머를 준비하는 부담을 줄이고 꾸준히 연습하도록 만들었습니다.",
        "free_title": "원하는 만큼 무료로 연습하세요",
        "free": "회원가입이나 결제 없이 준비된 자료와 타이머를 사용할 수 있습니다. 연습 횟수에는 제한이 없습니다. ‘내 사진’으로 선택한 파일은 브라우저 안에서만 사용하며 서버에 업로드하지 않습니다.",
        "ads": "현재 광고는 없습니다. 앞으로 운영비를 충당하기 위해 광고를 도입하더라도 연습 도구의 무료 이용을 유지하는 것이 운영 방향입니다. 광고를 도입할 때는 개인정보 안내와 필요한 동의 절차를 먼저 갱신하겠습니다.",
        "quality_title": "자료와 학습 글은 어떻게 관리하나요?",
        "quality": "포즈마다 동작과 관찰 목표를 정하고 AI 생성 예시를 제작했습니다. 현재 120개 자료는 검수용 이미지 목록으로 전신 여백, 다른 인물의 일부가 섞인 장면, 동작과 설명의 일치를 확인했고, 발견한 구성 문제는 재생성해 교체했습니다. 이미지 파일 중복과 네 언어의 자료 연결도 검사했습니다.",
        "limits": "이 점검은 미술·해부학 전문가의 검수를 뜻하지 않습니다. 손·발, 관절, 비례에는 오류가 남을 수 있으므로 실제 인물 관찰과 함께 참고용으로 사용하세요. 학습 글은 각 포즈에서 볼 지점, 시간별 과제와 복습 질문을 제공합니다. 자료나 설명의 오류 제보가 들어오면 확인 후 수정·교체 또는 제외 여부를 판단하고, 주요 변경은 아래에 기록합니다.",
        "feedback_title": "문의와 오류 제보",
        "feedback": "현재 문의 창구는 공개 GitHub 이슈입니다. 제레미가 확인하는 창구이며 작성하려면 GitHub 계정이 필요합니다. 한국어·일본어·영어·번체중문으로 의견을 남길 수 있습니다. 아래 버튼은 내용을 대신 제출하지 않고 작성 화면을 엽니다.",
        "report_items": ["자료 오류: 포즈 번호(예: PT076)와 어색한 부위를 적어주세요.", "기능 문제: 사용 기기·브라우저, 선택한 설정, 문제가 발생한 순서를 적어주세요.", "글·번역 오류: 페이지 주소와 수정이 필요한 문장을 적어주세요."],
        "public_note": "이슈와 첨부 내용은 누구나 볼 수 있습니다. 개인 사진, 이메일 주소나 연락처 등 개인정보는 올리지 마세요. 비공개 상담이나 사진 접수 창구로 사용하지 않습니다.",
        "report_button": "GitHub에서 의견·오류 제보하기",
        "issue_title": "[포즈토키] 의견 또는 오류 제보",
        "issue_body": "종류 (자료 / 기능 / 글·번역 / 제안):\n포즈 번호 또는 페이지 주소:\n문제와 기대한 동작:\n재현 순서:\n기기·브라우저·선택 언어:\n\n공개 게시물입니다. 개인 사진이나 개인정보는 첨부하지 마세요.",
        "updates_title": "주요 변경 내역", "date": "2026년 10월 2일",
        "updates": ["포즈 자료를 120개·10가지 유형으로 확대하고 난이도·이름·번호 검색을 추가했습니다.", "동작선, 무게중심, 앉은 자세의 심화 학습 글을 추가했습니다.", "최근 본 포즈의 반복을 줄이고, 선택한 포즈로 시작하는 기능과 모바일 표시를 개선했습니다.", "토끼 로고를 파비콘과 통일하고 운영자·자료 관리·문의 안내를 보강했습니다."],
        "privacy_operator": "데이터 이용 안내의 책임 운영자는 제레미입니다. 자료 처리 방식에 관한 문의도 아래 공개 제보 창구를 통해 전달할 수 있습니다.",
    },
    "ja": {
        "nav": "紹介・運営案内", "title": "PoseToki の紹介・運営案内",
        "operator": "運営：ジェレミー", "operator_title": "ジェレミーが制作・運営しています",
        "purpose": "PoseToki はジェレミー（Jeremy）が企画・制作・運営する無料のクロッキー練習サービスです。美術学生、漫画・イラストの学習者、趣味で描く人が写真探しやタイマーの準備にかける時間を減らし、練習を続けられるように作りました。",
        "free_title": "好きなだけ無料で練習できます",
        "free": "登録や支払いなしで素材とタイマーを使えます。練習回数に制限はありません。「自分の写真」で選んだファイルはブラウザ内だけで使い、サーバーにはアップロードしません。",
        "ads": "現在、広告はありません。将来、運営費のために広告を導入する場合も、練習ツールを無料で提供し続ける方針です。導入前にプライバシー案内と必要な同意手続きを更新します。",
        "quality_title": "素材と学習記事の管理",
        "quality": "各ポーズの動作と観察目標を決めて AI サンプルを生成しました。現在の120枚は確認用の画像一覧で、全身の余白、別の人物の一部が混じっていないか、動作と説明が一致するかを確認し、見つかった構図の問題は再生成して差し替えました。画像の重複と4言語の素材リンクも検査しました。",
        "limits": "これは美術・解剖学の専門家による監修ではありません。手足、関節、比率には誤りが残る可能性があるため、実際の人物観察と併用してください。記事には観察点、時間別の課題と振り返りの質問を用意しています。素材や説明の問題が報告された場合は確認し、修正・差し替え・除外を判断して、主な変更を下に記録します。",
        "feedback_title": "お問い合わせ・不具合の報告",
        "feedback": "現在の窓口はジェレミーが確認する公開 GitHub Issue です。投稿には GitHub アカウントが必要です。韓国語、日本語、英語、繁体字中国語でご意見を送れます。下のボタンは投稿画面を開くだけで、自動送信はしません。",
        "report_items": ["素材の問題：ポーズ番号（例：PT076）と不自然な部分。", "機能の問題：端末・ブラウザ、設定と問題が起きるまでの手順。", "記事・翻訳の問題：ページのURLと修正が必要な文。"],
        "public_note": "投稿と添付内容は誰でも閲覧できます。個人の写真、メールアドレスや連絡先を投稿しないでください。非公開の相談や写真受付には対応していません。",
        "report_button": "GitHub でご意見・不具合を報告",
        "issue_title": "[PoseToki] ご意見・不具合の報告",
        "issue_body": "種類（素材 / 機能 / 記事・翻訳 / 提案）：\nポーズ番号またはページのURL：\n問題と期待する動作：\n再現手順：\n端末・ブラウザ・選択言語：\n\n公開投稿です。個人の写真や情報を添付しないでください。",
        "updates_title": "主な変更履歴", "date": "2026年10月2日",
        "updates": ["素材を10種類・120ポーズに拡充し、難易度・名前・番号検索を追加しました。", "動きの線、重心、座りポーズの詳しい学習記事を追加しました。", "最近見たポーズの繰り返しを減らし、開始ポーズの指定とモバイル表示を改善しました。", "ウサギのロゴとファビコンを統一し、運営・素材管理・お問い合わせの案内を補足しました。"],
        "privacy_operator": "データ利用案内の責任運営者はジェレミー（Jeremy）です。取扱いに関するご意見も下の公開窓口にお寄せください。",
    },
    "en": {
        "nav": "About & operation", "title": "About PoseToki and its operation",
        "operator": "Run by Jeremy", "operator_title": "Created and run by Jeremy",
        "purpose": "PoseToki is a free gesture drawing practice service planned, built and run by Jeremy. It helps art students, comic and illustration learners, and hobby artists spend less time finding references and setting timers, so they can keep drawing regularly.",
        "free_title": "Practise as often as you like, for free",
        "free": "Use the references and timer without an account or payment. There is no limit on practice sessions. Files selected in My Photos stay in your browser and are not uploaded to a server.",
        "ads": "There are currently no ads. If advertising is introduced to help cover operating costs, the intention is to keep the practice tools free. The privacy notice and any required consent process will be updated before ads are introduced.",
        "quality_title": "How references and lessons are maintained",
        "quality": "Each AI-generated pose was made with a planned action and observation goal. The current 120 references were reviewed in image contact sheets for full-body framing, fragments of other people, and agreement between the pose and its description. Identified composition problems were regenerated and replaced. Duplicate files and reference links in all four languages were also checked.",
        "limits": "This is not an expert review of art or anatomy. Hands, feet, joints and proportions may still contain errors; use these examples alongside observation of real people. Lessons provide observation points, timed tasks and review questions. Reported problems with images or explanations are checked to decide whether to correct, replace or remove them. Major changes are recorded below.",
        "feedback_title": "Contact and report a problem",
        "feedback": "The current contact channel is public GitHub issues, checked by Jeremy. Posting requires a GitHub account. Feedback is welcome in Korean, Japanese, English or Traditional Chinese. The button below opens a draft form; it does not submit anything automatically.",
        "report_items": ["Reference issue: include the pose ID (for example, PT076) and the affected body part.", "Feature issue: include your device, browser, selected settings and steps leading to the problem.", "Lesson or translation issue: include the page URL and the sentence that needs correction."],
        "public_note": "Issues and attachments are visible to everyone. Do not post personal photos, email addresses or other private contact details. This channel is not for confidential support or sending private photos.",
        "report_button": "Send feedback or report an issue on GitHub",
        "issue_title": "[PoseToki] Feedback or problem report",
        "issue_body": "Type (reference / feature / lesson or translation / suggestion):\nPose ID or page URL:\nProblem and expected behaviour:\nSteps to reproduce:\nDevice, browser and selected language:\n\nThis is public. Do not attach personal photos or private information.",
        "updates_title": "Major updates", "date": "October 2, 2026",
        "updates": ["Expanded the reference library to 120 poses across 10 types, with level, name and ID search.", "Added detailed lessons on the line of action, center of gravity and seated poses.", "Reduced repetition of recently viewed poses and improved starting-pose selection and mobile display.", "Matched the rabbit logo to the favicon and expanded operator, reference management and contact information."],
        "privacy_operator": "Jeremy is the operator responsible for this data-use notice. Questions about data handling can also be raised through the public contact channel below.",
    },
    "zh-TW": {
        "nav": "介紹與營運說明", "title": "PoseToki 介紹與營運說明",
        "operator": "營運：傑瑞米", "operator_title": "由傑瑞米製作與營運",
        "purpose": "PoseToki 是由傑瑞米（Jeremy）企劃、製作與營運的免費人物速寫練習服務，希望讓美術學生、漫畫與插畫學習者，以及喜歡畫畫的人，減少尋找參考圖和設定計時器的準備時間，持續練習。",
        "free_title": "免費使用，想練習幾次都可以",
        "free": "不需註冊或付款即可使用參考素材與計時器，練習次數不受限制。「我的照片」所選的檔案只在瀏覽器內使用，不會上傳伺服器。",
        "ads": "目前沒有廣告。未來若為支應營運費用而加入廣告，營運方向仍是維持練習工具免費。導入前會先更新隱私說明與必要的同意程序。",
        "quality_title": "素材與學習文章如何管理？",
        "quality": "每個 AI 姿勢範例都先設定動作與觀察目標。目前的120張素材已透過檢查用圖片總覽，確認全身留白、是否混入其他人物的局部，以及姿勢和說明是否相符；發現的構圖問題已重新生成並替換，也檢查了重複檔案與四種語言的素材連結。",
        "limits": "這項檢查不代表美術或解剖學專家審核。手腳、關節與比例仍可能有錯誤，請搭配真實人物觀察使用。文章提供觀察重點、分時練習與回顧問題。收到素材或說明的問題回報後，會確認並判斷修正、替換或移除的方式，主要變更記錄於下方。",
        "feedback_title": "聯絡與問題回報",
        "feedback": "目前的聯絡管道是由傑瑞米查看的公開 GitHub Issue，發文需要 GitHub 帳號。歡迎以韓文、日文、英文或繁體中文提供意見。下方按鈕只會開啟填寫頁面，不會自動送出內容。",
        "report_items": ["素材問題：請提供姿勢編號（例如 PT076）與不自然的部位。", "功能問題：請提供裝置、瀏覽器、所選設定與問題發生前的操作步驟。", "文章或翻譯問題：請提供頁面網址與需要修改的句子。"],
        "public_note": "文章與附件任何人都能查看。請勿張貼私人照片、電子郵件或其他聯絡資料；此管道不提供非公開諮詢或私人照片收件服務。",
        "report_button": "到 GitHub 提供意見或回報問題",
        "issue_title": "[PoseToki] 意見或問題回報",
        "issue_body": "類型（素材 / 功能 / 文章或翻譯 / 建議）：\n姿勢編號或頁面網址：\n問題與預期操作結果：\n重現步驟：\n裝置、瀏覽器與所選語言：\n\n這是公開文章，請勿附上私人照片或個人資料。",
        "updates_title": "主要更新紀錄", "date": "2026年10月2日",
        "updates": ["素材擴充為10種類型、120個姿勢，新增難度、名稱與編號搜尋。", "新增動勢線、重心與坐姿的深入學習文章。", "減少近期已看姿勢的重複，改善起始姿勢選擇與行動裝置顯示。", "統一兔子標誌與網站圖示，補充營運者、素材管理與聯絡說明。"],
        "privacy_operator": "本資料使用說明的負責營運者為傑瑞米（Jeremy）。資料處理相關問題也可透過下方公開管道提出。",
    },
}


def operation_sections(lang):
    """Return introduction and closing sections around the existing service guide."""
    copy = OPERATIONS[lang]
    report_url = "https://github.com/Jeremysaunz/posetoki/issues/new?" + urlencode({
        "title": copy["issue_title"], "body": copy["issue_body"],
    })
    items = lambda values: "".join(f"<li>{escape(value)}</li>" for value in values)
    before = (
        f'<section id="operator"><h2>{escape(copy["operator_title"])}</h2><p>{escape(copy["purpose"])}</p></section>'
        f'<section><h2>{escape(copy["free_title"])}</h2><p>{escape(copy["free"])}</p><p>{escape(copy["ads"])}</p></section>'
    )
    after = (
        f'<section id="reference-care"><h2>{escape(copy["quality_title"])}</h2><p>{escape(copy["quality"])}</p><p>{escape(copy["limits"])}</p></section>'
        f'<section id="feedback"><h2>{escape(copy["feedback_title"])}</h2><p>{escape(copy["feedback"])}</p><ul>{items(copy["report_items"])}</ul>'
        f'<p><a class="primary" href="{escape(report_url, quote=True)}" rel="noopener noreferrer">{escape(copy["report_button"])}</a></p><p>{escape(copy["public_note"])}</p></section>'
        f'<section id="updates"><h2>{escape(copy["updates_title"])}</h2><p><time datetime="2026-10-02">{escape(copy["date"])}</time></p><ul>{items(copy["updates"])}</ul></section>'
    )
    return before, after
