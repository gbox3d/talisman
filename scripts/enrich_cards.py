"""
public/cards/cards.json을 읽어 각 카드에 name_ko + 정/역 키워드를 머지한다.

입력 데이터: scripts/card_meanings.py
출력: public/cards/cards.json (덮어쓰기)
- card_meanings에 없는 카드 ID가 있으면 경고하고 종료한다.
- cards.json에 없는 ID가 데이터에 있어도 경고만 출력한다.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import card_meanings  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
META_PATH = REPO_ROOT / "public" / "cards" / "cards.json"


def main() -> int:
    data = json.loads(META_PATH.read_text(encoding="utf-8"))
    meanings = card_meanings.build_index()

    missing_in_data: list[str] = []
    unused_in_meanings = set(meanings.keys())

    for card in data["cards"]:
        cid = card["id"]
        m = meanings.get(cid)
        if not m:
            missing_in_data.append(cid)
            continue
        unused_in_meanings.discard(cid)
        card["name_ko"] = m["name_ko"]
        card["keywords_upright"] = m["keywords_upright"]
        card["keywords_reversed"] = m["keywords_reversed"]

    if missing_in_data:
        print("ERROR: cards.json에 있지만 card_meanings에 없는 카드:")
        for cid in missing_in_data:
            print("  -", cid)
        return 1

    if unused_in_meanings:
        print("WARN: card_meanings에만 있고 cards.json에는 없는 카드 (확장 데이터?):")
        for cid in sorted(unused_in_meanings):
            print("  -", cid)

    META_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"OK: enriched {len(data['cards'])} cards in {META_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
