# Dev Log

## 목차

- [2026-05-25](#2026-05-25)

## 2026-05-25

### _forAI 문서 초기 생성

- `forai-scaffold`로 표준 문서 세트(`README.md`, `inventory.md`, `memo.md`, `plan.md`, `dev_log.md`)를 생성했다.
- 루트 `readme.md`를 읽어 프로젝트가 웹 타로 카드 앱이라는 것을 확인하고, 그 맥락으로 문서를 채웠다.
  - 사용 덱: Rider-Waite (Roses & Lilies), Wikimedia Commons
  - 해석 엔진(예정): Google Gemini 무료 API
- 첫 작업 단위를 **카드 수집**으로 정했다. 자세한 작업 순서는 `plan.md` 참조.

### 카드 수집 단계 1·2·3 완료 — 80장 다운로드

- 저장 위치: `public/cards/` (이미지) + `public/cards/cards.json` (메타데이터). 원본은 `public/cards/_raw/`에 보존.
- 카드 ID 명명 규칙 확정 (자세한 내용은 `plan.md` Near-term work 2번):
  - 메이저: `major_NN_slug` (예: `major_00_fool`)
  - 마이너: `{suit}_{rank}` (rank: 01→ace, 02~10, 11→page, 12→knight, 13→queen, 14→king)
- 수집 스크립트 `scripts/fetch_cards.py` 작성. Wikimedia Commons API로 카테고리 멤버 조회 → `imageinfo`로 url/license 확보 → 다운로드 → `cards.json` 생성.
- 결과: 78장 카드 + 표지 2장 = 80개 파일. 모두 Public domain (Wikimedia `extmetadata`로 확인). 총 ~45MB.

### 카드 수집 단계 4·5·6 완료 — 포맷 통일 + 메타데이터 보강 + 검증

- 포맷 통일: 모든 이미지 `.jpeg`로 통일 (fetch 시점에 `.jpg`→`.jpeg` 정규화 적용). 해상도 통일은 보류(현 단계에서 불필요).
- 메타데이터 보강: 78장 모두 `name_ko`, `keywords_upright`, `keywords_reversed` 추가.
  - 마스터 데이터: `scripts/card_meanings.py` (메이저 22 dict + 마이너 56 dict + suit/rank 한글 매핑)
  - 머지 스크립트: `scripts/enrich_cards.py` (cards.json에 in-place 머지, 누락/잉여 카드 ID를 명시적으로 보고)
- 검증: `scripts/verify_cards.py` 통과. 체크 항목 — 총 78+2장, 메이저 0~21, 마이너 4×14, image 경로 파일 실존, `.jpeg` 확장자, 필수 필드 비어있지 않음.

이로써 **카드 수집 단계는 종료**. 이후 작업(스택 선택, 카드 뽑기 UI 프로토타입, 스프레드 정의, Gemini 통합)은 `plan.md`의 "다음 단계" 항목 참고.

### 정적 카드 뽑기 라이브러리 + 데모 페이지 완성

- 결정: 백엔드 API 없이 **정적 호스팅(GitHub Pages)** 기반 + **단일 cards.json + 클라이언트 라이브러리** 패턴. 빌드 없음, 바닐라 ESM.
- 사이트 루트는 `public/`로 가정. `cards.json`의 `image` 필드를 절대 경로(`/cards/...`)에서 상대 경로(`cards/...`)로 변경해 어디에 publish해도 동작하도록 함. `fetch_cards.py`, `verify_cards.py`도 동일 규칙으로 수정.
- 추가 파일:
  - `public/index.html` — 다크 테마 데모 UI. 1장 / 3장 / 상황-행동-결과 버튼, 뽑힌 카드 + 정/역 회전 + 키워드 표시, 응답 JSON 펼침 뷰.
  - `public/tarot.js` — ESM 라이브러리. `Tarot.load() / draw(n) / drawSpread(id) / byId(id)`. `image_url`을 baseUrl과 결합해 제공. 셔플은 Fisher-Yates + 주입 가능한 `rng`.
  - `public/spreads.json` — 3개 스프레드 정의.
- 검증: `python3 -m http.server 8765` + curl로 모든 자산 200 응답 확인 후, node `--input-type=module`로 tarot.js를 dynamic import하여 `byId`, `draw(2)`, `drawSpread('three_card')` 동작까지 확인. 정/역 키워드 매핑, 포지션별 카드 배치 모두 정상.
- 미해결: 실제 브라우저에서의 시각적 확인은 안 했음 — UI 디테일(레이아웃/회전 애니메이션)은 사용자 검토 필요. GitHub Pages 배포 경로(루트/docs/Actions)도 미정.

### 디렉터리 이름 정정: talsman → talisman

- 사용자 지적으로 오타 발견 ("talisman"이 정확한 영어/스페인어 ASCII 표기, 스페인어 talismán = 부적).
- 디렉터리 `mv /home/gbox3d/work/talsman /home/gbox3d/work/talisman` 수행. `.git` 없는 상태였고 대상 경로가 비어있어 안전.
- 파일 내부 참조 5곳 정정 (README.md, inventory.md ×2, memo.md, fetch_cards.py의 USER_AGENT).
- memo.md에 어원 메모 추가.

### 로컬 nginx에 /taro 경로로 서비스 + API 사용 예제 페이지

- 시스템 상태 점검(`/home/gbox3d/work/server_info/server_status_report.md`)으로 nginx 1.18 + `/etc/nginx/sites-enabled/pds-21080.conf`가 21080 포트에서 `/home/gbox3d/www`(`= /mnt/data/pds`)를 정적 서빙 중이며 CORS도 `*`로 열려 있음을 확인.
- 단일 심볼릭 링크로 끝: `ln -s /home/gbox3d/work/talisman/public /mnt/data/pds/taro`. nginx config / sudo / reload 불필요.
- 검증: `/taro/`, `/taro/example.html`, `/taro/cards/cards.json`, `/taro/tarot.js`, `/taro/cards/major_00_fool.jpeg` 모두 200 + 올바른 content-type. CORS 헤더도 정상. node에서 `Tarot.load({ baseUrl: 'http://localhost:21080/taro/' })`로 `drawSpread('three_card')` 호출까지 정상 동작.
- 추가: `public/example.html` 작성 — (1) Tarot 라이브러리 한 줄 사용, (2) 라이브러리 없이 순수 fetch로 cards.json 호출, (3) 외부 origin에서 절대 URL로 import/fetch 하는 세 가지 사용 시나리오를 한 페이지에 정리. 코드 스니펫(pre) + 실행 버튼 + 결과 JSON 패널 + 카드 썸네일 포함.
- 노트: nginx 사용자(www-data)가 `/home/gbox3d`(750, others +x)와 `/mnt/data/work/talisman/public`(775)를 통과할 수 있음을 사전 확인.

### 설계 전환: JS 라이브러리 → REST 엔드포인트 1급 시민

- 사용자 지적: 클라이언트 JS가 random + slice 하는 패턴은 어떤 시스템에서든 호출 가능한 REST 인터페이스가 아니라 그냥 JS 라이브러리에 불과. 앱 인벤터·curl·다른 언어에서 동일하게 호출되려면 **카드별 JSON 엔드포인트**가 1급이어야 함.
- 신규 스크립트 `scripts/split_cards.py`: `public/cards/cards.json` → 카드별 80개 JSON 파일 + `ids.json`(78개 ID + count + covers).
- 결과 엔드포인트 셋 (`{BASE}` = 정적 호스팅 루트):
  - `GET {BASE}/cards/ids.json` — 무작위 인덱싱용 ID 목록
  - `GET {BASE}/cards/{id}.json` — 카드 1장 메타
  - `GET {BASE}/cards/{id}.jpeg` — 카드 1장 이미지
  - `GET {BASE}/cards/cards.json` — 전체 (한 번에)
  - `GET {BASE}/spreads.json` — 스프레드 정의
- 무작위 카드 뽑기는 **호출자 측 책임** (정적 호스팅 본질). 2-step 흐름: `ids.json` GET → random index → `{id}.json` GET.
- `readme.md` 전면 재작성: curl / Python / JavaScript / 앱 인벤터 4환경 동일 흐름 예제 + 엔드포인트 표 + 응답 JSON 형식. JS 편의 라이브러리 `tarot.js`는 부록으로 격하.
- nginx /taro 환경에서 curl로 검증 완료. 예: `ID=$(curl -s $BASE/cards/ids.json | jq -r '.ids[]' | shuf -n1); curl -s "$BASE/cards/$ID.json"` 정상 동작.

### 깃 초기화 + .gitignore + GitHub Pages 워크플로

- `git init` 후 브랜치 `main`으로 변경.
- `.gitignore`: Python 캐시 / venv / 에디터 설정 / OS 파일 / `public/cards/_raw/` 제외 (재현 가능, 약 23MB).
- `.github/workflows/pages.yml`: `public/` 디렉터리를 GitHub Pages artifact로 업로드 후 배포 (`actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4`). main push 또는 `workflow_dispatch`로 트리거.

### GitHub Pages 라이브 배포 완료

- 사용자 push 후 첫 워크플로는 Pages 미활성화로 실패 (`HttpError: Not Found ... Get Pages site failed`).
- `gh` CLI로 자동화: `gh api -X POST /repos/gbox3d/talisman/pages -f build_type=workflow`로 Pages 활성화 → `gh run rerun`으로 워크플로 재실행 → `gh run watch`로 완료 대기. 모든 단계 success.
- **라이브 URL**: https://gbox3d.github.io/talisman/
- 라이브 endpoint 전수 curl 확인: `/cards/ids.json`(78 IDs), `/cards/major_00_fool.json`(바보 + 정/역 키워드), 무작위 2-step draw 시뮬레이션, `/cards/{id}.jpeg`(HTTP/2 200, image/jpeg), `/spreads.json`(3종 스프레드) 모두 정상.
- 환경 메모: gh 2.92. 워크플로에 Node.js 20 deprecation 경고 (2026-09-16까지 동작 보장, 그 전까지 `actions/checkout` 등 메이저 버전 갱신 권장).

---

**오늘 마무리 (2026-05-25).** 다음 회차 시작 시 `plan.md`의 "다음 단계" 항목에서 선택. 추천: 데이터 보강(짧은 의미 문장) → Gemini 통합 → UX. 데이터 보강은 Gemini 없이도 가치 있고 baseline이 됨.
