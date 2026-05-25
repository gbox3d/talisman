"""
public/cards/cards.json + public/cards/*.jpeg 의 완결성을 검증한다.

체크 항목:
1. 메타데이터에 78장 카드 + 표지 2장이 모두 있는지
2. 메이저 0~21이 모두 있는지
3. 마이너 4 suit × 14 rank가 모두 있는지
4. 각 카드의 image 경로 파일이 실제 존재하는지 + 확장자가 .jpeg인지
5. 각 카드의 필수 필드 (id, name_en, name_ko, keywords_upright, keywords_reversed, license, source_url, image)가 채워져 있는지
6. 표지 2장의 image 파일이 존재하는지

체크 실패 시 비-제로 종료 코드 + 사람-읽기-쉬운 보고서.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = REPO_ROOT / "public" / "cards"
META_PATH = CARDS_DIR / "cards.json"

SUITS = ("wands", "cups", "swords", "pentacles")
RANKS = ("ace", "02", "03", "04", "05", "06", "07", "08", "09", "10",
         "page", "knight", "queen", "king")
REQUIRED_CARD_FIELDS = (
    "id", "name_en", "name_ko",
    "arcana", "image",
    "license", "source_url",
    "keywords_upright", "keywords_reversed",
)


def main() -> int:
    if not META_PATH.exists():
        print(f"FAIL: metadata not found at {META_PATH}")
        return 2

    data = json.loads(META_PATH.read_text(encoding="utf-8"))
    cards = data.get("cards", [])
    covers = data.get("covers", [])

    errors: list[str] = []
    warnings: list[str] = []

    # 1) 총 개수
    if len(cards) != 78:
        errors.append(f"카드 수가 78이 아님: {len(cards)}")
    if len(covers) != 2:
        warnings.append(f"표지 수가 2가 아님: {len(covers)}")

    by_id = {c["id"]: c for c in cards}

    # 2) 메이저 22장
    for n in range(22):
        prefix = f"major_{n:02d}_"
        if not any(cid.startswith(prefix) for cid in by_id):
            errors.append(f"메이저 누락: {prefix}*")

    # 3) 마이너 56장
    for suit in SUITS:
        for rank in RANKS:
            cid = f"{suit}_{rank}"
            if cid not in by_id:
                errors.append(f"마이너 누락: {cid}")

    # 4) image 파일 존재 + 확장자
    for c in cards + covers:
        img = c.get("image", "")
        if not img.endswith(".jpeg"):
            errors.append(f"{c.get('id', '?')}: image 확장자가 .jpeg가 아님 ({img})")
        # image는 "cards/foo.jpeg" 형태 → public/cards/foo.jpeg
        rel = img.removeprefix("cards/")
        path = CARDS_DIR / rel
        if not path.exists():
            errors.append(f"{c.get('id', '?')}: 파일 없음 → {path}")

    # 5) 필수 필드
    for c in cards:
        for f in REQUIRED_CARD_FIELDS:
            v = c.get(f)
            if v in (None, "", [], {}):
                errors.append(f"{c.get('id', '?')}: 필수 필드 비어 있음 → {f}")
        # 키워드 개수 sanity check
        if isinstance(c.get("keywords_upright"), list) and len(c["keywords_upright"]) < 2:
            warnings.append(f"{c['id']}: keywords_upright 개수가 적음 ({len(c['keywords_upright'])})")
        if isinstance(c.get("keywords_reversed"), list) and len(c["keywords_reversed"]) < 2:
            warnings.append(f"{c['id']}: keywords_reversed 개수가 적음 ({len(c['keywords_reversed'])})")

    # 6) 보고
    print(f"cards in metadata : {len(cards)}")
    print(f"covers in metadata: {len(covers)}")
    print(f"files in public/cards: {sum(1 for p in CARDS_DIR.glob('*.jpeg'))}")
    print()

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print("  !", w)
        print()

    if errors:
        print("ERRORS:")
        for e in errors:
            print("  X", e)
        print(f"\nFAIL: {len(errors)} error(s)")
        return 1

    print("OK: 78장 카드 + 표지 2장 모두 검증 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
