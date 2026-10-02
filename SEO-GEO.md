# PoseToki SEO · AI 검색 개선 기록

검토·수정일: 2026-10-02. 대상: https://posetoki.com. 실제 검색 순위, 유입 및 AI 인용은 아직 측정하지 않았습니다.

## 평가와 구현

기존 사이트에는 canonical, robots.txt, 사이트맵, 번역된 교육 페이지가 있었습니다. 그러나 연습실의 언어 전환은 같은 주소에서 JavaScript로 이루어졌고, 전체 포즈는 대화상자 안에 있어 검색엔진이 읽고 연결하기 어려웠습니다. 교육 페이지의 작성자와 서비스의 구조를 설명하는 데이터도 부족했습니다.

| 항목 | 수정 전 | 구현 결과 |
| --- | --- | --- |
| 연습실 언어별 주소 | 기본 주소 1개 | 한국어 `/`, 영어 `/en/`, 일본어 `/ja/`, 번체 `/zh-tw/`의 정적 HTML |
| 사이트맵 페이지 | 25개 | 36개 |
| 공개 포즈 자료실 | 없음 | 4개 언어, 각 120개 포즈의 이름·난이도·관찰 목표·권장 시간 |
| 초보자 실습 | 기존 종합 가이드 | 10분 실습 가이드 4개 언어 추가 |
| 언어별 연결 | 교육 글 중심 | 모든 페이지에 상호 hreflang 및 한국어 x-default |
| 구조화 데이터 | 없음 | WebSite, WebApplication, Article, BreadcrumbList 및 자료실 ItemList |
| 작성·운영 정보 | 소개 페이지 | 교육 페이지에서도 작성자 프로필과 업데이트 날짜 연결 |
| 콘텐츠 접근 | 메뉴·팝업 중심 | 홈 학습 카드 → 실습 글·자료실 → 해당 설정의 연습실 |
| 이미지 검색 발견 | 페이지 이미지 | 포즈 이름 alt, 지연 로딩, 사이트맵의 이미지 120개 |
| 첫 화면 이미지 | 불필요한 이전 포즈 묶음 배경 포함 | 실제 첫 포즈 이미지 사전 로딩, 이전 배경 제거 |

모든 페이지의 title·description은 고유합니다. Open Graph, 대표 이미지, 공유용 메타정보와 canonical을 적용했습니다. 계정 인증 태그, AdSense 코드, ads.txt는 유지했습니다. 개인정보 안내는 현재 AdSense 코드 설치 상태와 브라우저 저장 항목을 사실대로 설명하도록 고쳤습니다.

## 키워드와 페이지 역할

키워드를 나열하는 메타 태그보다 사용자가 질문하는 내용에 답하는 본문과 제목을 사용합니다.

| 검색 의도 | 페이지 |
| --- | --- |
| 무료 크로키 사이트, 크로키 타이머, 인체 크로키 연습 | 한국어 연습실 `/` |
| 크로키 초보, 크로키 연습 방법, 10분 크로키 | `/ko/beginner.html` |
| 크로키 포즈 자료, 인체 포즈 자료, 무료 크로키 자료 | `/ko/poses.html` |
| 30초 크로키, 동작선 그리기 | `/ko/gesture.html` |
| 인체 무게중심, 골반과 지지 발 | `/ko/balance.html` |
| 앉은 자세 크로키, 다리 겹침 | `/ko/seated.html` |
| gesture drawing timer, free figure drawing practice | `/en/` 및 영어 자료실·실습 글 |
| クロッキー タイマー, 人物ポーズ, 初心者 クロッキー | `/ja/` 및 일본어 자료실·실습 글 |
| 人物速寫, 人體姿勢素材, 速寫計時器 | `/zh-tw/` 및 번체 자료실·실습 글 |

이 표는 콘텐츠 의도 매핑이며, 검색량이나 경쟁 정도를 실측한 순위 예측표가 아닙니다.

## AI 검색: 가능한 조치와 한계

- `OAI-SearchBot`의 수집을 명시적으로 허용합니다. ChatGPT 검색과 GPTBot의 모델 학습은 구분합니다. GPTBot은 기존 전체 허용 정책을 유지했습니다. 실제 OpenAI IP의 방문이나 인용을 확인한 것은 아닙니다.
- `Google-Extended`를 허용합니다. Gemini의 학습 및 검색 그라운딩 관련 제어이며, Google 검색 순위에 직접 영향을 주는 신호가 아닙니다.
- 서비스가 누구를 위한 무엇인지, 무료·가입 불필요·AI 생성 포즈·로컬 사진 처리 등의 사실을 정적 HTML로 제공합니다.
- 교육 글은 과정, 관찰 목표, 시간별 비교, 실수와 복습을 설명합니다. 포즈 이름과 설명을 텍스트로 제공합니다.
- 임의 평점, 전문 자격, 이용자 수, Google/OpenAI 추천 이력은 만들어 넣지 않습니다. AI 이미지는 실제 사진이나 해부학 정답으로 표현하지 않습니다.
- Google의 AI 검색 기능에는 별도 AI 파일이나 특별한 구조화 데이터가 필수라는 근거가 없습니다. `llms.txt`로 인용을 보장한다는 주장에 기대지 않습니다.
- 로봇 허용·JSON-LD·좋은 설명은 수집 및 이해를 돕습니다. ChatGPT나 Gemini가 추천하거나 인용할지는 플랫폼의 수집·색인·답변 선택에 달려 있습니다.

공식 근거:

- Google AI 기능과 웹사이트: https://developers.google.com/search/docs/appearance/ai-features
- OpenAI 검색·사용자·학습 봇: https://developers.openai.com/api/docs/bots
- Google-Extended 제어: https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers
- 다국어 페이지: https://developers.google.com/search/docs/specialty/international/localized-versions
- Article 구조화 데이터: https://developers.google.com/search/docs/appearance/structured-data/article

## 검증

`python3 scripts/verify-seo.py`로 36개 페이지의 제목·설명·H1·canonical·robots·JSON-LD 구문·hreflang 상호 연결·내부 링크·이미지 존재 및 사이트맵 이미지 120개를 확인했습니다. Google의 색인 또는 리치 결과 노출 자체를 검증하는 도구는 아닙니다.

브라우저에서 영어·일본어·번체 전환, 영어 주소 새로고침, 포즈 자료실 → 지정 포즈 연습 시작, 초보자 글 → 1분·5장 설정, 390px 모바일 화면을 확인했습니다. 연습실과 새 교육 페이지에 가로 넘침이 없었습니다.

## 운영자가 다음에 할 일

1. Google Search Console과 네이버 서치어드바이저에 기존 `https://posetoki.com/sitemap.xml` 제출 상태를 확인합니다. 주소는 그대로이고 내용이 갱신되었습니다. 새 자료실·초보자 가이드의 수집/색인 상태를 확인합니다.
2. Search Console의 페이지 색인 보고서에서 오류, 선택된 canonical, 언어별 페이지 발견 상태를 살핍니다. 동일 URL의 색인 요청을 반복할 필요는 없습니다.
3. 검색 실적이 모이면 최근 28일의 노출·클릭·CTR·검색어·페이지·국가를 봅니다. 노출이 있는 페이지부터 제목과 설명이 실제 내용·검색 의도에 맞는지 개선합니다. 순위 보장은 하지 않습니다.
4. 포즈별 실제 크로키 예시와 동작선·골반·지지 발 표시를 직접 제작해 가장 유용한 교육 글부터 보강합니다. 해부학은 실제 인물 관찰과 검수로 보완합니다. 양산한 비슷한 글보다 비교 가능한 독창적 예제가 우선입니다.
5. 미술·웹툰 학습 커뮤니티와 교육자에게 도움이 되는 자료를 공유해 실제 사용 후기와 자연스러운 외부 링크를 얻습니다. 링크 구매·대량 자동 댓글은 사용하지 않습니다.
6. AI 추천 여부는 같은 질문의 답변이 매번 바뀔 수 있습니다. 날짜·질문·인용 URL을 함께 기록하고, 서버의 실제 봇 방문 및 분석 도구의 추천 유입과 구분해 확인합니다.

Search Console/네이버의 계정 내부 실적, 실제 봇 방문 로그, 유입 분석 대시보드는 이 작업에서 접근하거나 새로 연결하지 않았습니다. 따라서 트래픽 증가를 확인했다고 주장하지 않습니다.

## 유지보수와 한 번의 배포

홈 원본은 `templates/home.html`, 공통 메타정보는 `scripts/seo_common.py`, 신규 콘텐츠는 `scripts/discovery_content.py`입니다. `dist/index.html`만 직접 수정하면 다음 생성 때 덮어쓰므로 원본을 고칩니다. 홈 번역은 기존 `dist/i18n.js` 사전과 생성된 보완 번역을 함께 사용합니다.

```sh
python3 scripts/build-home-pages.py
python3 scripts/build-content-pages.py
python3 scripts/verify-seo.py
```

생성 결과인 `dist/`를 포함해 한 번에 커밋합니다. 기존 Vercel 정적 배포 방식(`outputDirectory: dist`)을 유지하므로 빌드 환경이나 비용 구조를 바꾸지 않습니다.
