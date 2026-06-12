# Inventory

## 목차

- [Repository](#repository)
- [Top-level structure](#top-level-structure)
- [REST endpoints](#rest-endpoints)
- [Live draw API (Deno Deploy)](#live-draw-api-deno-deploy)
- [Entrypoints and key modules](#entrypoints-and-key-modules)
- [Build and validation commands](#build-and-validation-commands)
- [Tests](#tests)
- [Deployment](#deployment)
- [Local nginx serving](#local-nginx-serving)
- [Notes](#notes)

## Repository

- Name: `talisman`
- Path: `/home/gbox3d/work/talisman`
- Branch: `main`
- Summary: 정적 호스팅 기반 웹 타로 카드 서비스. Rider-Waite (Roses & Lilies) 덱 78장 + 표지 2장을 REST GET 엔드포인트로 노출. 향후 Google Gemini API로 자연어 해석 추가 예정.

## Top-level structure

- `readme.md` — 프로젝트 소개 + REST 엔드포인트 + curl/Python/JS/앱 인벤터 사용 예제 (깃허브 공개용)
- `.gitignore` — Python 캐시, 에디터 설정, OS 파일, `public/cards/_raw/` 제외
- `.github/workflows/pages.yml` — `public/` 디렉터리를 GitHub Pages로 자동 배포
- `_forAI/` — AI 작업 문맥 문서
- `public/` — **사이트 루트** (= `{BASE}`). GitHub Pages가 이 폴더를 그대로 publish.
  - `public/index.html` — 카드 뽑기 데모 UI
  - `public/example.html` — 사용 예제 페이지
  - `public/tarot.js` — JS 편의 라이브러리(ESM, 부수 도구)
  - `public/spreads.json` — 스프레드 정의
  - `public/cards/cards.json` — 78장 + 표지 2장 전체 메타
  - `public/cards/ids.json` — 78개 ID + 표지 2장 ID (무작위 인덱싱용)
  - `public/cards/{id}.json` — 카드별 메타 (×80)
  - `public/cards/{id}.jpeg` — 카드 이미지 (×80)
  - `public/cards/_raw/` — Wikimedia 원본 (git 제외, 재현 가능)
- `deno/` — **라이브 랜덤 뽑기 엣지 API** (Deno Deploy). 정적이 못 하는 "한 방에 뽑기"만 담당.
  - `main.ts` — `Deno.serve` 엔트리포인트 (라우팅 + CORS)
  - `deck.ts` — 뽑기 로직 (`public/tarot.js`의 `draw()` 포팅, `../public/cards/cards.json`·`../public/spreads.json` 정적 import)
  - `deno.json` — `dev`/`start`/`check` 태스크
- `scripts/` — Python 데이터 도구
  - `fetch_cards.py` — Wikimedia에서 카드 수집 (`imageinfo`로 url+license)
  - `card_meanings.py` — 78장 한글명 + 정/역 키워드 마스터 데이터
  - `enrich_cards.py` — `cards.json`에 의미 데이터 머지
  - `split_cards.py` — `cards.json` → 카드별 JSON + `ids.json`
  - `verify_cards.py` — 메타/파일 완결성 검증

## REST endpoints

`{BASE}` = 정적 호스팅 루트 (예: `https://gbox3d.github.io/talisman` 또는 `http://host:21080/taro`).

| 경로 | 응답 | 용도 |
|---|---|---|
| `GET {BASE}/cards/ids.json` | JSON | 카드 78개 ID + count + 표지 2장 ID |
| `GET {BASE}/cards/{id}.json` | JSON | 카드 1장 메타 |
| `GET {BASE}/cards/{id}.jpeg` | image/jpeg | 카드 1장 이미지 |
| `GET {BASE}/cards/cards.json` | JSON | 78장 + 표지 2장 전체 메타 |
| `GET {BASE}/spreads.json` | JSON | 스프레드 정의 |

호출자 흐름(어느 언어든 동일): `ids.json` → random index → `{id}.json`.

이건 **① 서버 없이 (정적 2-step)** 경로다. 서버에서 무작위를 못 만들기 때문에 뽑기는 호출자 책임.

## Live draw API (Deno Deploy)

**② 한 방에 뽑기** 경로. 정적이 못 하는 무작위 뽑기만 서버리스 엣지(`deno/`)가 담당. 카드 데이터/이미지는 그대로 정적 호스팅에 있고, 엣지는 `cards.json`/`spreads.json`을 정적 import해서 뽑기만 한다.

`{API}` = 배포된 엣지 URL (예: `https://<app>.deno.dev`). GitHub Pages 경로로는 못 씀(Pages는 정적 전용).

| 경로 | 응답 | 용도 |
|---|---|---|
| `GET {API}/api/{n}` | JSON | 카드 n장 비복원 뽑기 (n: 1..78). `?reversed=false` → 전부 정방향 |
| `GET {API}/api/spread/{id}` | JSON | 스프레드로 뽑기 (`single`/`three_card`/`situation_action_outcome`) |
| `GET {API}/` 또는 `/api` | JSON | 사용법 |

- 응답: `{ count, spread, cards: [...] }`. 각 카드 = 정적 카드 메타 + `orientation` + `keywords`(orientation 반영) + `image_url`(절대) + `position`. 스프레드는 `position_key`/`position_name_ko` 추가.
- 모든 응답 CORS `*` + `application/json`. `OPTIONS` preflight 204.
- 이미지 호스트: env `IMAGE_BASE` (기본 `https://gbox3d.github.io/talisman/`).
- **배포(새 Deno Deploy)**: 대시보드 → repo `gbox3d/talisman` 연결 → 엔트리포인트 `deno/main.ts` → Automatic 모드(빌드 없음). Classic은 2026-07-20 종료.
- **로컬**: `cd deno && deno task dev` → `http://localhost:8000/api/3`. 타입 체크 `deno check deno/main.ts`.

## Entrypoints and key modules

- 브라우저 데모: `public/index.html` → `public/tarot.js`.
- 데이터 파이프라인: `fetch_cards.py` → `enrich_cards.py` → `split_cards.py` → `verify_cards.py`.
- 카드 메타의 `image` 필드는 `{BASE}` 기준 상대 경로. 호출자가 `{BASE}/{image}`로 절대 URL 생성.

## Build and validation commands

빌드 없음. 모두 정적 파일.

로컬 미리보기:
```
cd public && python3 -m http.server 8765
# → http://localhost:8765/
# → curl http://localhost:8765/cards/ids.json
```

데이터 재생성/검증:
```
python3 scripts/fetch_cards.py     # Wikimedia에서 80장 (캐시됨)
python3 scripts/enrich_cards.py    # 한글명/키워드 머지
python3 scripts/split_cards.py     # 카드별 JSON + ids.json 분할
python3 scripts/verify_cards.py    # 78+2장, 필드, 파일 검증
```

JS 문법 체크:
```
node --check public/tarot.js
```

엣지 API (deno):
```
cd deno && deno check main.ts     # 타입 체크
cd deno && deno task dev          # localhost:8000, --watch
# deno는 ~/.deno/bin (user-local). PATH에 없으면: export PATH="$HOME/.deno/bin:$PATH"
```

## Tests

- 자동화된 유닛 테스트 없음.
- 데이터 검증은 `verify_cards.py`로 갈음.
- REST 엔드포인트는 로컬 nginx + curl로 동작 확인됨 (2026-05-25).

## Deployment

`.github/workflows/pages.yml`이 main push 시 자동 배포:

1. `actions/checkout@v4`로 저장소 체크아웃
2. `actions/configure-pages@v5`로 Pages 설정
3. `actions/upload-pages-artifact@v3`로 `public/` 디렉터리 업로드
4. `actions/deploy-pages@v4`로 배포

**사용자 1회 설정**: GitHub 저장소 → Settings → Pages → Source = "GitHub Actions".

배포 후 `{BASE}` = `https://<user>.github.io/<repo>` 형태.

## Local nginx serving

호스트의 nginx(21080)가 `/home/gbox3d/www` (= `/mnt/data/pds`)를 root로 정적 서빙 중이며 CORS는 `*`로 열려 있다 (`/etc/nginx/sites-enabled/pds-21080.conf`). 다음 한 줄로 talisman을 `/taro` 경로에 노출:

```
ln -s /home/gbox3d/work/talisman/public /mnt/data/pds/taro
```

- nginx 설정 / sudo / reload 불필요. 심볼릭 링크만으로 즉시 동작.
- 해제: `rm /mnt/data/pds/taro` (원본 디렉터리는 그대로).
- 헤더 `Access-Control-Allow-Origin: *` 가 자동 부착되어 다른 origin에서도 호출 가능.

## Notes

- 카드 이미지 출처: https://commons.wikimedia.org/wiki/Category:Rider-Waite_tarot_deck_(Roses_%26_Lilies) · Public domain
- `public/cards/_raw/`는 `.gitignore`로 제외 (약 23MB). 필요 시 `python3 scripts/fetch_cards.py`로 재다운.
