"""
public/cards/cards.json 을 카드별 JSON 파일로 분할한다.

생성물:
- public/cards/<id>.json       : 카드 1장 메타 (78장 + 표지 2장)
- public/cards/ids.json        : { count, ids: [...] } — 무작위 뽑기용 인덱스

용도: 주소창/curl/앱 인벤터 등 정적 GET 한 번으로 카드 1장 정보를 받기 위함.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = REPO_ROOT / "public" / "cards"
META_PATH = CARDS_DIR / "cards.json"


def main() -> int:
    data = json.loads(META_PATH.read_text(encoding="utf-8"))
    cards = data["cards"]
    covers = data.get("covers", [])

    written = 0
    for record in cards + covers:
        cid = record["id"]
        out = CARDS_DIR / f"{cid}.json"
        out.write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        written += 1

    ids = [c["id"] for c in cards]
    cover_ids = [c["id"] for c in covers]
    (CARDS_DIR / "ids.json").write_text(
        json.dumps(
            {
                "count": len(ids),
                "ids": ids,
                "covers": cover_ids,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"OK: wrote {written} per-card JSONs ({len(ids)} cards + {len(cover_ids)} covers) + ids.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
