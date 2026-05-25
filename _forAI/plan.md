# Plan

## 목차

- [Current goal](#current-goal)
- [Near-term work](#near-term-work)
- [Structure decisions](#structure-decisions)
- [Risks](#risks)

## Current goal

- **REST 엔드포인트 + GitHub Pages 자동 배포 워크플로 완성** ✅ (2026-05-25). 다음 단계는 **Gemini API 통합 설계** (가장 무거움) / **데이터 보강(짧은 의미 문장)** / **UX 보강** 중 선택.

## Near-term work

### 카드 수집 단계 (완료, 기록용)

1. **저장 위치** — `public/cards/` (이미지) + `public/cards/cards.json` (메타데이터). 확정 2026-05-25.
2. **카드 ID/파일명 규칙** — 확정 2026-05-25.
   - 메이저: `major_00_fool` ~ `major_21_world`
   - 마이너: `{suit}_{rank}` (suit ∈ wands/cups/swords/pentacles, rank ∈ ace/02~10/page/knight/queen/king)
3. **수집 스크립트** — `scripts/fetch_cards.py`. Wikimedia Commons API → `imageinfo`로 url+license → 다운로드 → `cards.json` 생성.
4. **이미지 포맷 통일** — 모두 `.jpeg` (원본 .jpg 표지 2장도 cards.json상 `.jpeg`로 노출). 해상도 통일은 보류(필요해지면 그때 진행).
5. **메타데이터 보강** — `scripts/card_meanings.py`에 78장 한글명 + 정/역 키워드 마스터 데이터. `scripts/enrich_cards.py`가 이를 cards.json에 머지.
6. **검증** — `scripts/verify_cards.py`. 78+2장 전수, 필수 필드, 파일 존재, 확장자 모두 통과.

### REST 엔드포인트 + 배포 (완료, 기록용)

확정 사항 (2026-05-25):
- **인터페이스 1급 시민**: REST GET 엔드포인트. JS 라이브러리(`tarot.js`)는 부수 도구.
  - `GET {BASE}/cards/ids.json` — 78개 ID + 표지 2장 ID
  - `GET {BASE}/cards/{id}.json` — 카드 1장 메타
  - `GET {BASE}/cards/{id}.jpeg` — 카드 1장 이미지
  - `GET {BASE}/cards/cards.json` — 전체 메타
  - `GET {BASE}/spreads.json` — 스프레드 정의
- **무작위 뽑기는 호출자 책임** (정적 호스팅 본질). 표준 흐름: `ids.json` → 호출자 random index → `{id}.json` GET.
- **분할 빌드**: `scripts/split_cards.py`로 `cards.json` → 카드별 80개 JSON + `ids.json`.
- **사이트 루트**: `public/`. 자체 완결.
- **이미지 경로**: 메타의 `image` 필드는 `{BASE}` 기준 상대 경로(`cards/foo.jpeg`). 호출자가 `{BASE}/{image}`로 절대 URL 생성.
- **GitHub Pages 배포**: `.github/workflows/pages.yml`이 `public/` 디렉터리를 artifact로 배포. main push 또는 수동 트리거.

### 다음 단계 (제안 — 순서 미확정)

- **A. Gemini API 통합 설계**: 정적 호스팅이므로 백엔드 프록시(예: Cloudflare Worker / Vercel Function / Cloud Run)가 필요. 호출 인터페이스(카드 ID + 스프레드 컨텍스트 → 해석 텍스트), 캐싱 키 전략(카드 조합 + 스프레드 ID), 비용/한도 보호.
- **B. 데이터 보강**: 키워드 외에 정/역 짧은 설명(`meaning_upright`/`meaning_reversed` 문장) 추가 — Gemini 통합 전 baseline으로 활용 가능.
- **C. UX 보강**: 카드 뒷면(`cover_full` 활용) + 뒤집기 애니메이션 + 모바일 레이아웃 점검.
- **D. 추가 엔드포인트**(필요 시): `cards/by_arcana/major.json`, `cards/by_suit/wands.json` 같은 파생 뷰. yagni 우선.

## Structure decisions

- **카드 데이터 구조가 모든 후속 기능의 기준이다.** 카드 ID 명명 규칙은 이 단계에서 고정한다(이후 변경 시 비용이 크다).
- 정적 자산과 코드를 분리한다. 카드 이미지/메타데이터는 프레임워크와 독립적으로 사용 가능해야 한다.
- 프론트엔드 프레임워크 선택은 카드 수집 단계 이후로 미룬다 (수집 자체는 스택에 의존하지 않는다).
- Gemini API 통합은 카드 데이터가 안정화된 뒤 별도 단계로 진행한다.

## Risks

- **라이센스 표기 누락**: Wikimedia 파일별로 라이센스가 다를 수 있다. 메타데이터 `license`/`source_url`을 빠짐없이 기록하지 않으면 재배포 시 문제가 될 수 있다.
- **이미지 품질 편차**: "Roses & Lilies" 카테고리 내에서도 스캔 품질이 균일하지 않을 수 있다. 정규화 단계에서 시각적 일관성 확인이 필요.
- **카드 ID 규칙 번복**: 명명 규칙을 늦게 바꾸면 파일명/메타데이터/코드 전체를 손봐야 한다 — 수집 시작 전에 확정한다.
- **Gemini 무료 등급 한도**: 호출량 한도와 모델 가용성이 추후 변경될 수 있음. 캐싱/프록시 설계 단계에서 다시 검토.
