"""
Wikimedia Commons "Rider-Waite tarot deck (Roses & Lilies)" 카테고리에서
타로 78장 + 덱 표지 2장(총 80장)을 받아 public/cards/에 저장한다.

생성물:
- public/cards/_raw/<원본 파일명>            : Wikimedia 원본 그대로
- public/cards/<canonical_id>.jpeg           : ID 명명 규칙 적용 사본
- public/cards/cards.json                    : 메타데이터 (id, 이름, 라이센스, source 등)

명명 규칙:
- 메이저: major_00_fool .. major_21_world
- 마이너: {suit}_{rank}
  - rank: 01→ace, 02~10→02~10, 11→page, 12→knight, 13→queen, 14→king
- 표지 2장: cover_full, cover_cropped (cards.json에는 별도로 기록, 78장 카드 목록과 분리)
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

CATEGORY = "Category:Rider-Waite_tarot_deck_(Roses_%26_Lilies)"
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "talisman-card-fetcher/0.1 (https://example.invalid; contact: local)"

REPO_ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = REPO_ROOT / "public" / "cards"
RAW_DIR = CARDS_DIR / "_raw"
META_PATH = CARDS_DIR / "cards.json"

MAJOR_NAMES = {
    0: "fool", 1: "magician", 2: "high_priestess", 3: "empress", 4: "emperor",
    5: "hierophant", 6: "lovers", 7: "chariot", 8: "strength", 9: "hermit",
    10: "wheel_of_fortune", 11: "justice", 12: "hanged_man", 13: "death",
    14: "temperance", 15: "devil", 16: "tower", 17: "star", 18: "moon",
    19: "sun", 20: "judgement", 21: "world",
}

MINOR_RANK = {
    1: "ace", 2: "02", 3: "03", 4: "04", 5: "05", 6: "06", 7: "07",
    8: "08", 9: "09", 10: "10", 11: "page", 12: "knight", 13: "queen", 14: "king",
}

SUITS = {"Wands": "wands", "Cups": "cups", "Swords": "swords", "Pentacles": "pentacles"}


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def http_download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp, dest.open("wb") as f:
        shutil.copyfileobj(resp, f)


def list_category_files() -> list[str]:
    url = (
        f"{API}?action=query&list=categorymembers"
        f"&cmtitle={CATEGORY}&cmlimit=200&cmtype=file&format=json"
    )
    data = http_get_json(url)
    return [m["title"] for m in data["query"]["categorymembers"]]


def get_image_info(titles: list[str]) -> dict[str, dict]:
    """Wikimedia API는 한 번에 최대 50개 title 처리. props: url + extmetadata."""
    result: dict[str, dict] = {}
    for i in range(0, len(titles), 50):
        batch = titles[i : i + 50]
        joined = "|".join(urllib.parse.quote(t) for t in batch)
        url = (
            f"{API}?action=query&prop=imageinfo"
            f"&iiprop=url|extmetadata&iiextmetadatafilter=LicenseShortName|UsageTerms|Artist|ImageDescription"
            f"&titles={joined}&format=json"
        )
        data = http_get_json(url)
        pages = data["query"]["pages"]
        for _pageid, page in pages.items():
            title = page["title"]
            info = page["imageinfo"][0]
            extm = info.get("extmetadata", {})
            result[title] = {
                "url": info["url"],
                "descriptionurl": info["descriptionurl"],
                "license": (extm.get("LicenseShortName") or {}).get("value", ""),
                "usage_terms": (extm.get("UsageTerms") or {}).get("value", ""),
                "artist": (extm.get("Artist") or {}).get("value", ""),
                "description": (extm.get("ImageDescription") or {}).get("value", ""),
            }
        time.sleep(0.3)
    return result


def parse_title(title: str) -> dict | None:
    """File 제목을 카드 ID로 변환. 표지/펼친 사진은 cover_*로."""
    name = title.removeprefix("File:")
    # Major: "RWS1909 - NN Name.jpeg"
    m_major = re.match(r"^RWS1909 - (\d{2}) ([A-Za-z][A-Za-z ]+)\.(jpe?g|png)$", name, re.IGNORECASE)
    if m_major:
        num = int(m_major.group(1))
        rest = m_major.group(2).strip()
        ext = m_major.group(3).lower().replace("jpg", "jpeg")
        slug = MAJOR_NAMES.get(num)
        if slug is None:
            return None
        return {
            "id": f"major_{num:02d}_{slug}",
            "arcana": "major",
            "suit": None,
            "number": num,
            "name_en": rest,
            "ext": ext,
            "kind": "card",
        }
    # Minor: "RWS1909 - Suit NN.jpeg"
    m_minor = re.match(r"^RWS1909 - (Wands|Cups|Swords|Pentacles) (\d{2})\.(jpe?g|png)$", name, re.IGNORECASE)
    if m_minor:
        suit_en = m_minor.group(1).capitalize()
        num = int(m_minor.group(2))
        ext = m_minor.group(3).lower().replace("jpg", "jpeg")
        suit = SUITS[suit_en]
        rank = MINOR_RANK[num]
        rank_label = rank.capitalize() if rank.isalpha() else str(num)
        return {
            "id": f"{suit}_{rank}",
            "arcana": "minor",
            "suit": suit,
            "number": num,
            "name_en": f"{rank_label} of {suit_en}",
            "ext": ext,
            "kind": "card",
        }
    # cover variants
    if "Roses and Lilies cropped" in name:
        ext = name.rsplit(".", 1)[-1].lower().replace("jpg", "jpeg")
        return {"id": "cover_cropped", "ext": ext, "kind": "cover", "name_en": "Roses and Lilies (cropped)"}
    if "Roses and Lilies" in name:
        ext = name.rsplit(".", 1)[-1].lower().replace("jpg", "jpeg")
        return {"id": "cover_full", "ext": ext, "kind": "cover", "name_en": "Roses and Lilies (full)"}
    return None


def main() -> int:
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[1/4] Listing category {CATEGORY}")
    titles = list_category_files()
    print(f"      Found {len(titles)} files")

    print("[2/4] Fetching imageinfo (url + license)")
    info = get_image_info(titles)

    cards: list[dict] = []
    covers: list[dict] = []
    skipped: list[str] = []

    print("[3/4] Downloading files")
    for title in titles:
        parsed = parse_title(title)
        if not parsed:
            skipped.append(title)
            continue
        meta = info[title]
        raw_name = title.removeprefix("File:")
        raw_path = RAW_DIR / raw_name
        out_name = f"{parsed['id']}.{parsed['ext']}"
        out_path = CARDS_DIR / out_name

        if not raw_path.exists():
            print(f"  - {parsed['id']:<28} <- {raw_name}")
            http_download(meta["url"], raw_path)
            time.sleep(0.15)
        else:
            print(f"  = {parsed['id']:<28} (raw exists)")

        if not out_path.exists():
            shutil.copy2(raw_path, out_path)

        record = {
            "id": parsed["id"],
            "name_en": parsed.get("name_en"),
            "image": f"cards/{out_name}",
            "source_url": meta["descriptionurl"],
            "license": meta["license"],
            "usage_terms": meta["usage_terms"],
            "artist_html": meta["artist"],
            "original_filename": raw_name,
        }
        if parsed["kind"] == "card":
            record.update({
                "arcana": parsed["arcana"],
                "suit": parsed["suit"],
                "number": parsed["number"],
            })
            cards.append(record)
        else:
            covers.append(record)

    cards.sort(key=lambda c: (c["arcana"] != "major", c.get("suit") or "", c["number"]))

    print("[4/4] Writing metadata to", META_PATH)
    META_PATH.write_text(
        json.dumps(
            {
                "source_category": f"https://commons.wikimedia.org/wiki/{CATEGORY}",
                "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S%z") or "",
                "naming_rule": {
                    "major": "major_NN_name",
                    "minor": "{suit}_{rank}",
                    "suits": list(SUITS.values()),
                    "ranks": list(MINOR_RANK.values()),
                },
                "count_cards": len(cards),
                "count_covers": len(covers),
                "cards": cards,
                "covers": covers,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Done. cards={len(cards)}, covers={len(covers)}, skipped={len(skipped)}")
    if skipped:
        print("Skipped titles:")
        for t in skipped:
            print("  -", t)
    return 0


if __name__ == "__main__":
    sys.exit(main())
