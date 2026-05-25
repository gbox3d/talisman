# 웹 타로 카드 (talisman)

Rider-Waite 타로 덱의 78장 + 표지 2장을 **언어 무관한 JSON REST 엔드포인트**로 노출하는 정적 웹 서비스.
백엔드 서버 없이 GitHub Pages / nginx 같은 정적 호스팅만으로 동작하며,
curl, Python, 앱 인벤터, JavaScript 등 어느 환경에서든 동일한 HTTP GET 인터페이스로 호출합니다.

> 무작위 카드 뽑기는 **호출자 측 책임**입니다 (정적 호스팅의 본질). 서버가 무작위를 못 만들기 때문에, ID 목록을 받아 호출자가 random index를 고른 뒤 카드 메타를 GET 하는 2-step 패턴을 사용합니다 — 어느 시스템에서든 동일하게 적용됩니다.

## 목차

- [엔드포인트](#엔드포인트)
- [응답 형식](#응답-형식)
- [사용법 — 어느 환경에서나 동일한 GET](#사용법--어느-환경에서나-동일한-get)
  - [curl](#curl)
  - [Python](#python)
  - [JavaScript (브라우저 / Node)](#javascript-브라우저--node)
  - [앱 인벤터 (개념 흐름)](#앱-인벤터-개념-흐름)
- [JS 편의 라이브러리 (부록)](#js-편의-라이브러리-부록)
- [디렉터리 구조](#디렉터리-구조)
- [로컬 실행](#로컬-실행)
- [데이터 재생성](#데이터-재생성)
- [출처 · 라이센스](#출처--라이센스)

## 엔드포인트

`{BASE}` = 정적 호스팅 루트. 예) `https://yourhost/taro` 또는 `https://username.github.io/talisman`.

| 메서드 / 경로 | 응답 | 설명 |
|---|---|---|
| `GET {BASE}/cards/ids.json` | JSON | 카드 78장의 ID 목록 + count + 표지 2장 ID. 무작위 뽑기용 인덱스. |
| `GET {BASE}/cards/{id}.json` | JSON | 카드 1장 메타 (한글명, 키워드, 이미지 경로, 출처, 라이센스). |
| `GET {BASE}/cards/{id}.jpeg` | image/jpeg | 카드 1장 이미지. |
| `GET {BASE}/cards/cards.json` | JSON | 78장 + 표지 2장 전체 메타 (한 번에 받기). |
| `GET {BASE}/spreads.json` | JSON | 스프레드 정의 (single / three_card / situation_action_outcome). |

CORS는 호스팅 환경에 따라 다릅니다. 이 저장소의 nginx 21080 노드에서는 `Access-Control-Allow-Origin: *`로 열려 있어 다른 origin에서도 호출 가능.

## 응답 형식

`GET {BASE}/cards/major_00_fool.json` 응답:

```json
{
  "id": "major_00_fool",
  "arcana": "major",
  "suit": null,
  "number": 0,
  "name_en": "Fool",
  "name_ko": "바보",
  "keywords_upright": ["새로운 시작", "순수", "자유", "모험", "잠재력"],
  "keywords_reversed": ["무모함", "어리석음", "부주의", "리스크"],
  "image": "cards/major_00_fool.jpeg",
  "source_url": "https://commons.wikimedia.org/wiki/File:RWS1909_-_00_Fool.jpeg",
  "license": "Public domain",
  "original_filename": "RWS1909 - 00 Fool.jpeg"
}
```

`image` 필드는 `{BASE}` 기준 상대 경로입니다. 이미지 절대 URL은 `{BASE}/{image}`로 결합하세요.

`GET {BASE}/cards/ids.json` 응답:

```json
{
  "count": 78,
  "ids": ["major_00_fool", "major_01_magician", "...", "pentacles_king"],
  "covers": ["cover_cropped", "cover_full"]
}
```

카드 ID 명명 규칙:

- 메이저: `major_NN_slug` — 예) `major_00_fool`, `major_21_world`
- 마이너: `{suit}_{rank}` — 예) `wands_ace`, `cups_07`, `swords_page`, `pentacles_king`
  - suit: `wands` / `cups` / `swords` / `pentacles`
  - rank: `ace`, `02`~`10`, `page`, `knight`, `queen`, `king`

## 사용법 — 어느 환경에서나 동일한 GET

아래 모든 예제의 핵심 흐름은 동일합니다:

1. `cards/ids.json` 으로 ID 목록을 받는다 (또는 알고 있는 ID를 바로 사용).
2. 호출 측에서 random index 선택.
3. `cards/{id}.json` 으로 카드 메타 GET.
4. `image` 필드와 `{BASE}`를 결합해서 이미지 URL을 만든다.

### curl

특정 카드 한 장:

```bash
curl -s https://yourhost/taro/cards/major_00_fool.json | jq .
```

무작위 카드 1장 (2-step):

```bash
BASE=https://yourhost/taro
ID=$(curl -s "$BASE/cards/ids.json" | jq -r '.ids[]' | shuf -n1)
curl -s "$BASE/cards/$ID.json" | jq '{id, name_ko, keywords_upright, image}'
```

ID 목록만:

```bash
curl -s "$BASE/cards/ids.json" | jq -r '.ids[]'
```

### Python

```python
import json
import random
import urllib.request

BASE = "https://yourhost/taro"

def get(path):
    with urllib.request.urlopen(f"{BASE}/{path}") as r:
        return json.load(r)

# 무작위 카드 1장
ids = get("cards/ids.json")["ids"]
card = get(f"cards/{random.choice(ids)}.json")
print(card["name_ko"], card["keywords_upright"])
print("image:", f"{BASE}/{card['image']}")

# 스프레드 3장 (과거-현재-미래)
spread = get("spreads.json")["three_card"]
picked = random.sample(ids, len(spread["positions"]))
for pos, cid in zip(spread["positions"], picked):
    c = get(f"cards/{cid}.json")
    print(f"[{pos['name_ko']}] {c['name_ko']} — {c['keywords_upright']}")
```

### JavaScript (브라우저 / Node)

```js
const BASE = 'https://yourhost/taro';

const get = (path) => fetch(`${BASE}/${path}`).then(r => r.json());

const { ids } = await get('cards/ids.json');
const id = ids[Math.floor(Math.random() * ids.length)];
const card = await get(`cards/${id}.json`);

console.log(card.name_ko, card.keywords_upright);
console.log('image:', `${BASE}/${card.image}`);
```

### 앱 인벤터 (개념 흐름)

Web 컴포넌트 1개로 가능:

1. `Web1.Url = "{BASE}/cards/ids.json"` → `Web1.Get`
2. `GotText` 콜백에서 JSON 파싱 → `ids` 리스트 추출
3. `ids`에서 `random integer from 1 to length` 로 인덱스 선택 → 카드 ID 변수 저장
4. `Web1.Url = "{BASE}/cards/" + cardId + ".json"` → `Web1.Get`
5. 두 번째 `GotText`에서 카드 JSON 파싱 → `name_ko`, `keywords_upright`, `image` 사용
6. 이미지 표시: `Image1.Picture = "{BASE}/" + image`

`Web1.Get`을 두 번 사용 (또는 별도 Web 컴포넌트 2개)하는 방식.

## JS 편의 라이브러리 (부록)

브라우저 JS에서만 동작하는 얇은 wrapper입니다. **이 라이브러리 없이도 위의 모든 REST 호출이 동일하게 가능**하며, 다른 언어/시스템에서는 사용할 필요가 없습니다. 단지 데모 페이지의 편의용입니다.

```html
<script type="module">
  import { Tarot } from 'https://yourhost/taro/tarot.js';

  const tarot = await Tarot.load({ baseUrl: 'https://yourhost/taro/' });
  console.log(tarot.draw(1));                      // 무작위 1장
  console.log(tarot.drawSpread('three_card'));     // 스프레드
</script>
```

내부적으로는 위 REST 엔드포인트를 호출합니다.

## 디렉터리 구조

```
public/                       # ← 정적 호스팅 루트 ({BASE})
├── index.html                # 카드 뽑기 데모 UI (선택)
├── example.html              # 사용 예제 페이지 (선택)
├── tarot.js                  # JS 편의 라이브러리 (선택)
├── spreads.json              # GET /spreads.json
└── cards/
    ├── ids.json              # GET /cards/ids.json
    ├── cards.json            # GET /cards/cards.json (전체)
    ├── {id}.json             # GET /cards/{id}.json (×80장)
    ├── {id}.jpeg             # GET /cards/{id}.jpeg (×80장)
    └── _raw/                 # Wikimedia 원본 보존 (배포 제외 가능)
scripts/                      # Python 데이터 도구
├── fetch_cards.py            # Wikimedia에서 카드 수집
├── card_meanings.py          # 한글명 + 키워드 마스터 데이터
├── enrich_cards.py           # cards.json에 의미 머지
├── split_cards.py            # cards.json → 카드별 JSON 분할 + ids.json
└── verify_cards.py           # 완결성 검증
```

## 로컬 실행

빌드 없음. 어떤 정적 서버든 OK.

```bash
cd public
python3 -m http.server 8765
# → http://localhost:8765/
# → curl http://localhost:8765/cards/ids.json
```

## 데이터 재생성

```bash
python3 scripts/fetch_cards.py     # Wikimedia에서 카드 다운로드 (캐시됨)
python3 scripts/enrich_cards.py    # name_ko + 정/역 키워드 머지
python3 scripts/split_cards.py     # cards.json → 카드별 JSON + ids.json
python3 scripts/verify_cards.py    # 전수 검증
```

## 출처 · 라이센스

- 카드 이미지: [Rider-Waite tarot deck (Roses & Lilies) — Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:Rider-Waite_tarot_deck_(Roses_%26_Lilies)) — **Public domain**
- 원작: Pamela Colman Smith (1878–1951), Arthur Edward Waite
- 각 카드 JSON의 `source_url` / `license` 필드에 개별 파일 출처가 기록되어 있습니다.
