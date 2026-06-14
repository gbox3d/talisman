# Memo

## 목차

- [제품 기준선](#제품-기준선)
- [Rider-Waite 덱 메모](#rider-waite-덱-메모)
- [Gemini API 메모](#gemini-api-메모)
- [기본 설정값](#기본-설정값)
- [런타임 구조 메모](#런타임-구조-메모)
- [동작 규칙](#동작-규칙)
- [반복 금지](#반복-금지)

## 제품 기준선

- 프로젝트명: `talisman` (스페인어 "talismán" = 부적; ASCII 표기는 영어 talisman과 동일) — 웹 타로 카드 앱
- 버전: 미정 (초기)
- 타깃 플랫폼: 웹 브라우저
- 빌드 환경: 빌드 없음 — 정적(HTML/CSS/JS) + Deno Deploy(Deno.serve)

## Rider-Waite 덱 메모

- 사용 덱: Rider-Waite, "Roses & Lilies" edition
- 출처 카테고리: https://commons.wikimedia.org/wiki/Category:Rider-Waite_tarot_deck_(Roses_%26_Lilies)
- 카드 구성 (표준 Rider-Waite 78장):
  - 메이저 아르카나(Major Arcana) 22장 — 0 The Fool ~ 21 The World
  - 마이너 아르카나(Minor Arcana) 56장 — Wands / Cups / Swords / Pentacles 각 14장 (Ace, 2~10, Page, Knight, Queen, King)
- 라이센스: 각 파일의 라이센스/저작권 표기를 수집 시점에 같이 기록할 것. 일반적으로 Rider-Waite 원본 자체는 미국 기준 퍼블릭 도메인이지만, Wikimedia 업로더가 스캔/스타일에 대해 별도 라이센스를 적용하는 경우가 있다.
- 파일 형식: Wikimedia에 JPG/PNG 혼재 가능 — 통일된 포맷과 해상도로 정규화하는 단계가 필요.

## Gemini API 메모

- 사용 예정: Google Gemini "무료" 등급 API
- 용도: 뽑힌 카드(또는 카드 조합)의 의미/해석 텍스트 생성
- 결정 필요:
  - 모델 선택 (예: `gemini-1.5-flash` 등 무료 등급에서 허용된 모델)
  - 호출 위치: 클라이언트 직접 호출 시 키 노출 위험 → 백엔드 프록시 권장
  - 레이트 리미트와 캐싱 전략 (자주 등장하는 카드/스프레드는 캐시)

## 기본 설정값

- 카드 이미지 표준 해상도: 미정 (수집 직후 결정)
- 카드 ID 명명 규칙: 미정 (예: `major_00_fool`, `wands_ace`, `cups_knight` 등 — 수집 단계에서 확정)

## 런타임 구조 메모

**구체화됨 — 라이브 운영 중.** 두 경로 모두 같은 카드 데이터(`public/cards/cards.json`)를 쓴다.

1. **정적 경로 (GitHub Pages)** — https://gbox3d.github.io/talisman/. 2-step(`ids.json` → 무작위 → `{id}.json`), 서버리스 불필요.
2. **라이브 뽑기 API (Deno Deploy 엣지)** — https://talisman.gbox3d.deno.net. `GET /api/{n}`·`/api/spread/{id}`가 비복원 뽑기 + 카드 JSON을 한 번에 응답. CORS `*`. 엔트리포인트 `deno/main.ts`(Deno.serve).
3. **플랫폼**: 새 Deno Deploy(console.deno.com, `*.deno.net`). 구 Classic(`*.deno.dev`)은 2026-07-20 종료. 재배포 `scripts/deploy_edge.sh`(CLI, `--prod`) — Pages 자동 배포와는 별개.
4. **다음(후보)**: Gemini 해석을 같은 엣지에 얹기(`?interpret=1`).

## 동작 규칙

- 카드 데이터 스키마는 카드 수집 단계에서 확정하며, 이후 모든 기능(드로우, 해석, 스프레드)이 이 스키마를 기반으로 한다.
- 카드 이미지와 메타데이터는 1:1 매칭되어야 한다 (이미지 파일명과 카드 ID 일치).
- 라이브 API(`/api/{n}`)와 정적 경로는 같은 `cards.json`을 쓴다. 엣지 배포는 `scripts/deploy_edge.sh`로 별도 — Pages 자동 배포와 다르다.

## 반복 금지

- TODO: 누적되는 대로 기록.
