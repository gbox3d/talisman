// 덱 로드 + 뽑기 로직 — public/tarot.js 의 draw() 포팅.
//
// 정적 JSON import로 카드/스프레드 데이터를 번들에 포함한다(런타임 네트워크 의존 없음).
// Deno Deploy 자동 모드는 엔트리포인트의 모듈 그래프를 그대로 배포하므로,
// 아래 상대경로 JSON import가 같이 올라간다.

import cardsData from "../public/cards/cards.json" with { type: "json" };
import spreadsData from "../public/spreads.json" with { type: "json" };

// 이미지 절대 URL의 기준. 카드 이미지는 GitHub Pages(정적)에 그대로 둔다.
const IMAGE_BASE = Deno.env.get("IMAGE_BASE") ??
  "https://gbox3d.github.io/talisman/";

export interface RawCard {
  id: string;
  name_en: string;
  name_ko: string;
  arcana: "major" | "minor";
  suit: string | null;
  number: number;
  image: string;
  source_url: string;
  license: string;
  keywords_upright: string[];
  keywords_reversed: string[];
}

export type Orientation = "upright" | "reversed";

export interface DrawnCard extends RawCard {
  orientation: Orientation;
  keywords: string[];
  image_url: string;
  position: number;
}

export interface Spread {
  id: string;
  name_ko: string;
  description_ko: string;
  positions: { key: string; name_ko: string }[];
}

// 78장만 뽑기 대상(covers 제외).
const DECK = cardsData.cards as RawCard[];
const SPREADS = spreadsData as Record<string, Spread>;

export const DECK_SIZE = DECK.length;

export function spreadIds(): string[] {
  return Object.keys(SPREADS);
}

export function getSpread(id: string): Spread | undefined {
  return SPREADS[id];
}

export interface DrawOptions {
  allowReversed?: boolean;
  rng?: () => number;
}

// 절대 이미지 URL을 붙인다(tarot.js의 _enrich와 동일 개념).
function imageUrl(image: string): string {
  return new URL(image, IMAGE_BASE).href;
}

/**
 * 무작위로 n장 뽑는다(비복원 추출). tarot.js draw()의 Fisher-Yates 포팅.
 */
export function draw(n: number, opts: DrawOptions = {}): DrawnCard[] {
  const { allowReversed = true, rng = Math.random } = opts;
  if (!Number.isInteger(n) || n < 1) {
    throw new RangeError(`draw(n): n must be a positive integer, got ${n}`);
  }
  if (n > DECK.length) {
    throw new RangeError(`draw(n=${n}) > deck size ${DECK.length}`);
  }

  // Fisher-Yates 셔플(원본 배열 보존).
  const idxs = DECK.map((_, i) => i);
  for (let i = idxs.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [idxs[i], idxs[j]] = [idxs[j], idxs[i]];
  }

  return idxs.slice(0, n).map((deckIdx, position) => {
    const card = DECK[deckIdx];
    const orientation: Orientation = allowReversed && rng() < 0.5
      ? "reversed"
      : "upright";
    const keywords = orientation === "upright"
      ? card.keywords_upright
      : card.keywords_reversed;
    return {
      ...card,
      orientation,
      keywords,
      image_url: imageUrl(card.image),
      position,
    };
  });
}
