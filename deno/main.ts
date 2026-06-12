// talisman 라이브 랜덤 뽑기 엣지 API (Deno Deploy 엔트리포인트)
//
// 정적 호스팅(GitHub Pages)은 서버에서 코드를 실행 못 해 "한 방에 뽑힌 JSON"을 줄 수 없다.
// 이 엣지 함수가 /api/* 랜덤 뽑기만 담당하고, 카드 데이터/이미지는 정적 호스팅에 그대로 둔다.
// 어떤 클라이언트(앱인벤터·curl·fetch)든 GET 한 번으로 겹치지 않는 카드 JSON을 받는다.
//
// 로컬:  deno task dev   →  http://localhost:8000/api/3
// 배포:  Deno Deploy 대시보드에서 repo 연결 + 엔트리포인트 deno/main.ts (Automatic)

import {
  DECK_SIZE,
  draw,
  type DrawnCard,
  getSpread,
  spreadIds,
} from "./deck.ts";

const CORS_HEADERS: Record<string, string> = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, OPTIONS",
  "access-control-allow-headers": "*",
};

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      ...CORS_HEADERS,
    },
  });
}

function err(status: number, message: string, extra: unknown = {}): Response {
  return json({ error: message, ...(extra as object) }, status);
}

const USAGE = {
  service: "talisman tarot draw API",
  description:
    "겹치지 않게 카드를 뽑아 이미지+타로 정보를 한 번에 JSON으로 돌려준다.",
  endpoints: {
    "GET /api/{n}":
      `카드 n장 비복원 뽑기 (n: 1..${DECK_SIZE}). 쿼리 ?reversed=false 면 전부 정방향.`,
    "GET /api/spread/{id}": `스프레드로 뽑기. id: ${spreadIds().join(" | ")}`,
  },
  examples: [
    "/api/1",
    "/api/3",
    "/api/3?reversed=false",
    "/api/spread/three_card",
  ],
};

// 쿼리에서 역방향 허용 여부를 읽는다. ?reversed=false / 0 / no 면 끔.
function allowReversedFrom(url: URL): boolean {
  const v = url.searchParams.get("reversed");
  if (v === null) return true;
  return !["false", "0", "no", "off"].includes(v.toLowerCase());
}

function drawN(url: URL, nRaw: string): Response {
  const n = Number(nRaw);
  if (!Number.isInteger(n) || n < 1 || n > DECK_SIZE) {
    return err(400, `n must be an integer between 1 and ${DECK_SIZE}`, {
      got: nRaw,
    });
  }
  const cards = draw(n, { allowReversed: allowReversedFrom(url) });
  return json({ count: cards.length, spread: null, cards });
}

function drawSpread(url: URL, id: string): Response {
  const spread = getSpread(id);
  if (!spread) {
    return err(404, `unknown spread: ${id}`, { available: spreadIds() });
  }
  const cards = draw(spread.positions.length, {
    allowReversed: allowReversedFrom(url),
  });
  const merged = cards.map((c: DrawnCard, i: number) => ({
    ...c,
    position_key: spread.positions[i].key,
    position_name_ko: spread.positions[i].name_ko,
  }));
  return json({
    count: merged.length,
    spread: {
      id: spread.id,
      name_ko: spread.name_ko,
      description_ko: spread.description_ko,
    },
    cards: merged,
  });
}

function handler(req: Request): Response {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }
  if (req.method !== "GET") {
    return err(405, "method not allowed");
  }

  const url = new URL(req.url);
  const path = url.pathname.replace(/\/+$/, ""); // 끝 슬래시 제거

  if (path === "" || path === "/api") {
    return json(USAGE);
  }

  const spreadMatch = path.match(/^\/api\/spread\/([^/]+)$/);
  if (spreadMatch) {
    return drawSpread(url, decodeURIComponent(spreadMatch[1]));
  }

  const nMatch = path.match(/^\/api\/([^/]+)$/);
  if (nMatch) {
    return drawN(url, nMatch[1]);
  }

  return err(404, "not found", { try: USAGE.examples });
}

Deno.serve(handler);
