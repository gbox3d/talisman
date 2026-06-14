# Dev Log

## 목차

- [2026-05-25](#2026-05-25)
- [2026-06-01](#2026-06-01)
- [2026-06-14](#2026-06-14)

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

## 2026-06-01

### 라이브 랜덤 뽑기 엣지 API (`/api/{n}`) 추가 — Deno Deploy

- **배경**: 사용자가 `gbox3d.github.io/talisman/api/3`처럼 **한 방에 뽑힌 JSON**(겹치지 않는 N장 + 이미지/타로 정보)을 원함. 핵심 제약을 명확히 함 — 정적 호스팅 + 브라우저 JS는 **브라우저(받는 쪽)에서만** 돌아서, 앱인벤터·curl·서버 fetch(JS 미실행)는 정적 페이지에서 뽑힌 JSON을 못 받는다. 따라서 "모든 클라이언트"를 원하면 서버(서버리스)가 필수.
- **결정(사용자 확정)**: 모든 클라이언트 지원 → 서버리스 엣지 도입. 호스팅 = **Deno Deploy**(GitHub repo 연동 자동 배포, CLI 불필요). 정적 2-step 패턴과 `tarot.js`는 그대로 유지(서버 0 경로 보존), 엣지는 추가 surface.
- **제약 메모**: Deno Deploy **Classic은 2026-07-20 종료** → 새 Deno Deploy 플랫폼 사용. 코드(`Deno.serve`)는 양쪽 호환.
- **신규 `deno/`**:
  - `deck.ts` — `public/tarot.js`의 `draw()` 포팅(Fisher-Yates 비복원 + 정/역 50% + orientation별 keywords). `IMAGE_BASE`(env, 기본 `https://gbox3d.github.io/talisman/`)로 절대 `image_url` 생성. 카드/스프레드 데이터는 `../public/cards/cards.json`·`../public/spreads.json`을 **정적 JSON import**(런타임 네트워크 의존 0, Deno Deploy 자동 모드가 모듈 그래프째 배포).
  - `main.ts` — `Deno.serve` 엔트리포인트. 라우트: `GET /api/{n}`(쿼리 `?reversed=false`), `GET /api/spread/{id}`, `GET /`(usage), `OPTIONS`(204). 모든 응답 CORS `*` + `application/json`.
  - `deno.json` — `dev`/`start`/`check` 태스크.
- **검증(로컬)**: `deno 2.8.1` user-local 설치(`~/.deno`). `deno check main.ts` 통과. `deno task dev`(localhost:8000)로 curl 전수 확인 — `/api/3` 비복원(unique=3), `?reversed=false` 전부 upright, keywords가 orientation과 일치(여러 회차), `image_url`이 실제 GitHub Pages에서 **HTTP 200 image/jpeg**, `/api/spread/three_card` 포지션 매칭, `/api/spread/nope` 404, `/api/999` 400, `/` usage JSON, OPTIONS·GET 모두 CORS 헤더.
- **문서**: `readme.md`에 "라이브 랜덤 뽑기 API" 섹션 + 배포 절차 추가, 디렉터리 구조에 `deno/` 추가, 인트로 blockquote를 ①서버없이(정적 2-step)/②한방에(라이브 API) 두 경로로 정리.
- **미완(사용자 작업)**: Deno Deploy 대시보드에서 repo 연결 + 엔트리포인트 `deno/main.ts` 지정(사용자 로그인 필요). 발급 URL은 `*.deno.dev` — GitHub Pages 경로(`gbox3d.github.io/...`)로는 못 씀(Pages는 정적 전용).

## 2026-06-14

### Deno Deploy 배포 경로 재검토 — 플랫폼 마이그레이션 반영, GitHub 연동 → CLI 배포로 권장 변경

- **배경**: 사용자가 GitHub Pages는 마쳤고(`gbox3d.github.io/talisman/` 라이브), 이제 `deno/` 엣지 API를 어떻게 띄우는지 + "별도 과정 없이 자동으로 되냐"를 물음. 답: **아니오 — Pages는 push 자동 배포지만 엣지는 Deno Deploy에 별도 1회 배포 필요**(Deno 로그인 필요, 내가 대신 못 함).
- **공식 문서로 2026-06 현황 확인**:
  - 새 플랫폼 = [console.deno.com](https://console.deno.com). 구 **Deploy Classic(`dash.deno.com`)은 2026-07-20 종료** → 새 플랫폼 강제. `deployctl`도 sunset → `deno deploy` 서브커맨드 사용.
  - `Deno.serve` 완전 지원(우리 코드 OK). 구 std `serve()`는 미지원(우리는 안 씀).
  - **GitHub 연동은 "앱이 서브디렉터리에 있는 모노레포 미지원"** — talisman은 `deno/main.ts`가 `../public/*.json`을 import하는 구조라 정확히 이 케이스에 걸림. → readme의 옛 "대시보드 GitHub 연결 + Automatic 모드" 안내는 이제 위험/부정확.
- **결정**: 권장 배포 경로를 **CLI(`deno deploy create`, 저장소 루트에서 실행)** 로 변경. 루트째 올리므로 서브디렉터리 모노레포 제약을 우회. 이미지(약 45MB)는 엣지가 안 쓰므로 `--ignore 'public/cards/*.jpeg'` 선택지 안내.
- **로컬 검증**: `deno 2.8.1`, `deno deploy`(v0.0.99) 서브커맨드 존재 확인, `deno check main.ts` 통과, 서버 띄워 `GET /api/3`(unique 3장)·`/api/spread/three_card`(과거/현재/미래 포지션 매칭) 정상 응답 재확인.
- **문서**: `readme.md` 배포 섹션을 console.deno.com + CLI 우선 + 모노레포 제약 경고 + Classic 종료일로 재작성. `plan.md` Current goal의 "대시보드 연결 1회" → "CLI 배포 1회"로 정정.
- **남은 건 여전히 사용자 작업**: Deno 계정 로그인 + `deno deploy create` 실행(엔트리포인트 `deno/main.ts`). 그 전에 console.deno.com에서 org 1회 생성.

### Deno Deploy 라이브 배포 완료 — https://talisman.gbox3d.deno.net

- 사용자가 console.deno.com 로그인 + org 생성 + **24h access token(`ddp_`)** 발급해 전달. CLI 배포는 내가 사용자 머신에서 실행.
- **배포 과정에서 발견한 함정 3가지**(readme/스크립트에 반영):
  1. `deno deploy create`는 `--region`(us/eu/global) **필수**. → `global` 사용.
  2. 빌드 자동감지가 `public/`을 보고 **runtime=static**으로 잡아버림. `--do-not-use-detected-build-config`로 꺼야 `--runtime-mode dynamic --entrypoint deno/main.ts`가 먹음.
  3. `--source local`은 디렉터리를 통째로 올림 → `.git`(24M)+카드 이미지(23M)+`_raw`(23M)가 딸려갈 위험. **최소 스테이징**(코드 + cards.json + spreads.json = 약 100KB, 5파일)을 임시 폴더에 만들어 거기서 배포. 이미지는 엣지가 안 쓰고 GitHub Pages에 그대로 있음(`image_url`이 그쪽을 가리킴).
- **최초 생성 명령**: `deno deploy create --org gbox3d --app talisman --source local --runtime-mode dynamic --entrypoint deno/main.ts --do-not-use-detected-build-config --region global`. 5파일 업로드 → build/warm/route → 성공.
- **결과 URL**: Production `https://talisman.gbox3d.deno.net` (새 플랫폼은 `.deno.net`, `.deno.dev` 아님). console: https://console.deno.com/gbox3d/talisman.
- **라이브 전수 검증**: `/`(usage), `/api/3`(비복원·unique 3장), `/api/spread/three_card`(과거/현재/미래 매칭), CORS `*`, `?reversed=false` 전부 upright, `image_url`이 GitHub Pages에서 **HTTP 200 image/jpeg 273KB**, 에러 케이스 `/api/999`→400·`/api/spread/nope`→404·OPTIONS→204. 모두 정상.
- **재배포 워크플로**: 기존 앱은 `deno deploy --org gbox3d --app talisman` (저장된 빌드 설정 재사용). 단 **`--prod` 없으면 프리뷰로만** 나감(확인함). 재현용 [`scripts/deploy_edge.sh`](../scripts/deploy_edge.sh) 추가 — 최소 스테이징 + `--prod`. 첫 재배포 시도에서 Deno 측 "unexpected internal error"가 한 번 났으나 **일시적**(재시도 성공), 프로덕션엔 무영향(실패 빌드는 승격 안 됨).
- **토큰**: 24h 제한이라 자동 만료. console.deno.com/account/access-tokens 에서 즉시 revoke도 가능.
- **남은 선택지**: (1) `public/index.html` 데모가 라이브 `/api/*`를 쓰도록 연결, (2) Gemini 해석(`?interpret=1`)을 같은 엣지에 얹기, (3) org verify(한도 100배, 현재 불필요).
