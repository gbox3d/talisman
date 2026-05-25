// 웹 타로 카드 — 정적 클라이언트 라이브러리 (브라우저 ESM)
//
// 사용법:
//   import { Tarot } from './tarot.js';
//   const tarot = await Tarot.load();           // cards.json + spreads.json fetch
//   const one  = tarot.draw(1)[0];               // 1장 뽑기
//   const spread = tarot.drawSpread('three_card');
//
// 반환 형식 (카드 1장):
//   {
//     id, name_en, name_ko, arcana, suit, number,
//     image,             // baseUrl 기준 상대 경로 (예: "cards/cups_ace.jpeg")
//     image_url,         // 절대 URL (현재 페이지 기준으로 resolve)
//     license, source_url, artist_html,
//     orientation,       // 'upright' | 'reversed'
//     keywords,          // orientation에 맞춘 키워드 배열
//     keywords_upright, keywords_reversed,  // 원본 데이터도 같이 노출
//     position,          // draw() 결과의 인덱스 (0부터)
//   }

const DEFAULT_CARDS_PATH = 'cards/cards.json';
const DEFAULT_SPREADS_PATH = 'spreads.json';

export class Tarot {
  /**
   * cards.json과 spreads.json을 fetch해서 Tarot 인스턴스를 만든다.
   * @param {object} [opts]
   * @param {string} [opts.baseUrl] - 정적 자산의 기준 경로. 기본은 이 모듈 파일의 디렉터리.
   * @param {string} [opts.cardsPath]  - baseUrl 기준 cards.json 경로.
   * @param {string} [opts.spreadsPath] - baseUrl 기준 spreads.json 경로. null이면 안 받음.
   */
  static async load(opts = {}) {
    const baseUrl = new URL(opts.baseUrl ?? './', import.meta.url);
    const cardsUrl = new URL(opts.cardsPath ?? DEFAULT_CARDS_PATH, baseUrl);
    const spreadsUrl = opts.spreadsPath === null
      ? null
      : new URL(opts.spreadsPath ?? DEFAULT_SPREADS_PATH, baseUrl);

    const cardsRes = await fetch(cardsUrl);
    if (!cardsRes.ok) throw new Error(`Failed to fetch cards.json: ${cardsRes.status}`);
    const cardsData = await cardsRes.json();

    let spreads = {};
    if (spreadsUrl) {
      const sRes = await fetch(spreadsUrl);
      if (sRes.ok) {
        spreads = await sRes.json();
      }
    }

    return new Tarot(cardsData, spreads, baseUrl);
  }

  constructor(cardsData, spreads, baseUrl) {
    this._data = cardsData;
    this._cards = cardsData.cards;
    this._covers = cardsData.covers ?? [];
    this._spreads = spreads;
    this._baseUrl = baseUrl;
  }

  /** 덱 전체 (카피, image_url 포함). */
  get cards() {
    return this._cards.map((c) => this._enrich(c));
  }

  /** 표지/장식 이미지들. */
  get covers() {
    return this._covers.map((c) => this._enrich(c));
  }

  /** 사용 가능한 스프레드 메타 목록. */
  get spreads() {
    return Object.values(this._spreads);
  }

  /** id로 카드 1장 조회. 없으면 null. */
  byId(id) {
    const c = this._cards.find((x) => x.id === id);
    return c ? this._enrich(c) : null;
  }

  /**
   * 무작위로 n장 뽑는다 (비복원 추출).
   * @param {number} n
   * @param {object} [opts]
   * @param {boolean} [opts.allowReversed=true] - 역방향 허용 여부.
   * @param {() => number} [opts.rng=Math.random] - 0~1 난수 생성기.
   * @returns {Array<object>}
   */
  draw(n = 1, opts = {}) {
    const { allowReversed = true, rng = Math.random } = opts;
    if (!Number.isInteger(n) || n < 1) throw new Error(`draw(n): n must be a positive integer, got ${n}`);
    if (n > this._cards.length) throw new Error(`draw(n=${n}) > deck size ${this._cards.length}`);

    // Fisher-Yates 셔플 (원본 배열 보존)
    const idxs = this._cards.map((_, i) => i);
    for (let i = idxs.length - 1; i > 0; i--) {
      const j = Math.floor(rng() * (i + 1));
      [idxs[i], idxs[j]] = [idxs[j], idxs[i]];
    }

    return idxs.slice(0, n).map((deckIdx, position) => {
      const card = this._cards[deckIdx];
      const orientation = allowReversed && rng() < 0.5 ? 'reversed' : 'upright';
      const keywords = orientation === 'upright' ? card.keywords_upright : card.keywords_reversed;
      return {
        ...this._enrich(card),
        position,
        orientation,
        keywords,
      };
    });
  }

  /**
   * 스프레드 ID로 뽑는다. 결과는 spread 메타 + 각 포지션에 카드 매칭.
   */
  drawSpread(spreadId, opts = {}) {
    const spread = this._spreads[spreadId];
    if (!spread) throw new Error(`unknown spread: ${spreadId}. available: ${Object.keys(this._spreads).join(', ')}`);
    const cards = this.draw(spread.positions.length, opts);
    return {
      spread: spread.id,
      name_ko: spread.name_ko,
      description_ko: spread.description_ko,
      positions: spread.positions.map((pos, i) => ({
        ...pos,
        card: cards[i],
      })),
    };
  }

  // ── 내부 헬퍼 ──────────────────────────────────────────────
  _enrich(card) {
    return {
      ...card,
      image_url: new URL(card.image, this._baseUrl).href,
    };
  }
}

// 편의용 전역 export — `import tarot from './tarot.js'`로 default 사용도 허용.
export default Tarot;
