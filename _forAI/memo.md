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
- 빌드 환경: 미정 (프론트엔드 스택 결정 필요)

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

- 미정. 단, 초기 구상은 다음과 같다:
  1. 정적 자산: 카드 이미지 + 카드 메타데이터(JSON)
  2. 프론트엔드: 스프레드 선택, 카드 뽑기 UI, 결과 표시
  3. 백엔드(또는 서버리스): Gemini 호출 프록시
- 코드 작성 시점에 이 절을 다시 채울 것.

## 동작 규칙

- 카드 데이터 스키마는 카드 수집 단계에서 확정하며, 이후 모든 기능(드로우, 해석, 스프레드)이 이 스키마를 기반으로 한다.
- 카드 이미지와 메타데이터는 1:1 매칭되어야 한다 (이미지 파일명과 카드 ID 일치).

## 반복 금지

- TODO: 누적되는 대로 기록.
