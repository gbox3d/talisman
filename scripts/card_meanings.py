"""
타로 78장(메이저 22 + 마이너 56)의 한글명과 정/역 키워드.

키워드는 일반적으로 통용되는 라이더-웨이트 의미를 짧게 정리한 것이며,
앱 안에서 Gemini가 더 풍부한 해석을 만들 때 시드/기준으로 사용한다.
"""

# 메이저 아르카나
MAJOR = {
    "major_00_fool": {
        "name_ko": "바보",
        "keywords_upright": ["새로운 시작", "순수", "자유", "모험", "잠재력"],
        "keywords_reversed": ["무모함", "어리석음", "부주의", "리스크"],
    },
    "major_01_magician": {
        "name_ko": "마법사",
        "keywords_upright": ["의지", "창조", "자신감", "능력", "발현"],
        "keywords_reversed": ["조작", "기만", "미숙", "재능 낭비"],
    },
    "major_02_high_priestess": {
        "name_ko": "여사제",
        "keywords_upright": ["직관", "신비", "내면의 지혜", "잠재의식"],
        "keywords_reversed": ["비밀", "단절", "표면적 지식", "혼란"],
    },
    "major_03_empress": {
        "name_ko": "여황제",
        "keywords_upright": ["풍요", "모성", "자연", "창조성", "양육"],
        "keywords_reversed": ["의존", "결핍", "창조성 막힘", "과보호"],
    },
    "major_04_emperor": {
        "name_ko": "황제",
        "keywords_upright": ["권위", "안정", "구조", "통제", "아버지상"],
        "keywords_reversed": ["독재", "경직", "권력 남용", "미숙한 통제"],
    },
    "major_05_hierophant": {
        "name_ko": "교황",
        "keywords_upright": ["전통", "가르침", "영적 권위", "관습"],
        "keywords_reversed": ["반항", "새로운 접근", "형식 거부"],
    },
    "major_06_lovers": {
        "name_ko": "연인",
        "keywords_upright": ["사랑", "조화", "선택", "결합"],
        "keywords_reversed": ["불화", "잘못된 선택", "단절"],
    },
    "major_07_chariot": {
        "name_ko": "전차",
        "keywords_upright": ["의지", "승리", "추진력", "통제"],
        "keywords_reversed": ["방향 상실", "자제력 부족", "좌절"],
    },
    "major_08_strength": {
        "name_ko": "힘",
        "keywords_upright": ["용기", "인내", "부드러운 힘", "자제"],
        "keywords_reversed": ["약함", "의심", "자제력 부족"],
    },
    "major_09_hermit": {
        "name_ko": "은둔자",
        "keywords_upright": ["내면 탐색", "고독", "지혜", "성찰"],
        "keywords_reversed": ["고립", "외로움", "길 잃음"],
    },
    "major_10_wheel_of_fortune": {
        "name_ko": "운명의 수레바퀴",
        "keywords_upright": ["변화", "운명", "전환점", "기회"],
        "keywords_reversed": ["불운", "통제 불능", "정체"],
    },
    "major_11_justice": {
        "name_ko": "정의",
        "keywords_upright": ["정의", "공정", "진실", "인과"],
        "keywords_reversed": ["불공정", "편견", "회피"],
    },
    "major_12_hanged_man": {
        "name_ko": "매달린 사람",
        "keywords_upright": ["희생", "관점 전환", "멈춤", "깨달음"],
        "keywords_reversed": ["무의미한 희생", "정체", "망설임"],
    },
    "major_13_death": {
        "name_ko": "죽음",
        "keywords_upright": ["끝", "변환", "재생", "전환"],
        "keywords_reversed": ["저항", "변화 거부", "정체"],
    },
    "major_14_temperance": {
        "name_ko": "절제",
        "keywords_upright": ["균형", "절제", "조화", "인내"],
        "keywords_reversed": ["불균형", "과잉", "갈등"],
    },
    "major_15_devil": {
        "name_ko": "악마",
        "keywords_upright": ["속박", "유혹", "집착", "물질주의"],
        "keywords_reversed": ["해방", "깨달음", "통제 회복"],
    },
    "major_16_tower": {
        "name_ko": "탑",
        "keywords_upright": ["급변", "파괴", "폭로", "충격"],
        "keywords_reversed": ["위기 회피", "두려움", "지연된 재앙"],
    },
    "major_17_star": {
        "name_ko": "별",
        "keywords_upright": ["희망", "영감", "평온", "신뢰"],
        "keywords_reversed": ["절망", "자신감 상실", "비관"],
    },
    "major_18_moon": {
        "name_ko": "달",
        "keywords_upright": ["환상", "직관", "불안", "무의식"],
        "keywords_reversed": ["혼란 해소", "진실 드러남", "두려움 극복"],
    },
    "major_19_sun": {
        "name_ko": "태양",
        "keywords_upright": ["기쁨", "성공", "활력", "명확함"],
        "keywords_reversed": ["일시적 좌절", "과도한 낙관", "지연된 성공"],
    },
    "major_20_judgement": {
        "name_ko": "심판",
        "keywords_upright": ["부활", "각성", "평가", "부름"],
        "keywords_reversed": ["자기 의심", "회피", "후회"],
    },
    "major_21_world": {
        "name_ko": "세계",
        "keywords_upright": ["완성", "통합", "성취", "여행"],
        "keywords_reversed": ["미완", "지연", "마무리 부족"],
    },
}

# 마이너 아르카나
SUIT_KO = {"wands": "완드", "cups": "컵", "swords": "소드", "pentacles": "펜타클"}
RANK_KO = {
    "ace": "에이스", "02": "2", "03": "3", "04": "4", "05": "5",
    "06": "6", "07": "7", "08": "8", "09": "9", "10": "10",
    "page": "페이지", "knight": "나이트", "queen": "퀸", "king": "킹",
}

# 마이너 카드별 키워드 (정/역). 한글명은 SUIT_KO + RANK_KO로 자동 생성.
MINOR = {
    # ── Wands (불 / 열정·창의성·행동) ─────────────────────────────
    "wands_ace": {
        "keywords_upright": ["영감", "새로운 시작", "활력", "잠재력"],
        "keywords_reversed": ["지연", "동기 부족", "의욕 상실"],
    },
    "wands_02": {
        "keywords_upright": ["계획", "결정", "미래 비전"],
        "keywords_reversed": ["두려움", "미루기", "시야 부족"],
    },
    "wands_03": {
        "keywords_upright": ["확장", "비전 실현", "진취"],
        "keywords_reversed": ["좌절", "지연", "시야 좁음"],
    },
    "wands_04": {
        "keywords_upright": ["축하", "화합", "안정", "가정"],
        "keywords_reversed": ["일시적 균열", "형식적 화합"],
    },
    "wands_05": {
        "keywords_upright": ["경쟁", "갈등", "다툼"],
        "keywords_reversed": ["갈등 해소", "협력", "회피"],
    },
    "wands_06": {
        "keywords_upright": ["승리", "인정", "성공"],
        "keywords_reversed": ["실패", "자만", "지연된 승리"],
    },
    "wands_07": {
        "keywords_upright": ["방어", "도전 극복", "용기"],
        "keywords_reversed": ["압도", "굴복", "자신감 부족"],
    },
    "wands_08": {
        "keywords_upright": ["빠른 진행", "행동", "소식"],
        "keywords_reversed": ["지연", "혼란", "좌절"],
    },
    "wands_09": {
        "keywords_upright": ["인내", "회복력", "경계"],
        "keywords_reversed": ["소진", "방어 과잉", "편집증"],
    },
    "wands_10": {
        "keywords_upright": ["부담", "책임", "과중"],
        "keywords_reversed": ["해방", "위임", "짐 내려놓기"],
    },
    "wands_page": {
        "keywords_upright": ["호기심", "새로운 아이디어", "모험가 정신"],
        "keywords_reversed": ["미성숙", "산만", "의욕 부재"],
    },
    "wands_knight": {
        "keywords_upright": ["모험", "추진력", "열정"],
        "keywords_reversed": ["충동", "무모함", "좌절"],
    },
    "wands_queen": {
        "keywords_upright": ["자신감", "매력", "결단력"],
        "keywords_reversed": ["질투", "변덕", "자기중심"],
    },
    "wands_king": {
        "keywords_upright": ["비전", "리더십", "카리스마"],
        "keywords_reversed": ["독재", "충동적 결정", "무모함"],
    },
    # ── Cups (물 / 감정·관계·직관) ─────────────────────────────
    "cups_ace": {
        "keywords_upright": ["새로운 사랑", "감정의 시작", "영성"],
        "keywords_reversed": ["감정 막힘", "공허", "거절"],
    },
    "cups_02": {
        "keywords_upright": ["결합", "관계", "화합"],
        "keywords_reversed": ["불화", "단절", "균형 상실"],
    },
    "cups_03": {
        "keywords_upright": ["축하", "우정", "공동체"],
        "keywords_reversed": ["과잉", "가십", "고립"],
    },
    "cups_04": {
        "keywords_upright": ["권태", "명상", "무관심"],
        "keywords_reversed": ["깨어남", "새로운 기회 수용"],
    },
    "cups_05": {
        "keywords_upright": ["상실", "후회", "슬픔"],
        "keywords_reversed": ["회복", "수용", "용서"],
    },
    "cups_06": {
        "keywords_upright": ["향수", "추억", "순수"],
        "keywords_reversed": ["과거 집착", "미성숙"],
    },
    "cups_07": {
        "keywords_upright": ["환상", "선택", "망상"],
        "keywords_reversed": ["현실 직시", "결단", "명료"],
    },
    "cups_08": {
        "keywords_upright": ["떠남", "단념", "더 큰 의미 추구"],
        "keywords_reversed": ["망설임", "두려움", "머무름"],
    },
    "cups_09": {
        "keywords_upright": ["만족", "행복", "소원 성취"],
        "keywords_reversed": ["표면적 만족", "자만"],
    },
    "cups_10": {
        "keywords_upright": ["가족 행복", "충만", "조화"],
        "keywords_reversed": ["가정 불화", "단절"],
    },
    "cups_page": {
        "keywords_upright": ["감수성", "영감", "메시지"],
        "keywords_reversed": ["감정 미성숙", "비현실적"],
    },
    "cups_knight": {
        "keywords_upright": ["로맨스", "매혹", "제안"],
        "keywords_reversed": ["변덕", "비현실", "실망"],
    },
    "cups_queen": {
        "keywords_upright": ["공감", "직관", "정서적 안정"],
        "keywords_reversed": ["의존", "감정 기복", "자기 연민"],
    },
    "cups_king": {
        "keywords_upright": ["정서적 균형", "지혜", "자비"],
        "keywords_reversed": ["감정 억압", "조종", "변덕"],
    },
    # ── Swords (바람 / 사고·갈등·진실) ─────────────────────────────
    "swords_ace": {
        "keywords_upright": ["명확함", "진실", "돌파"],
        "keywords_reversed": ["혼란", "잘못된 판단", "정체"],
    },
    "swords_02": {
        "keywords_upright": ["결정 회피", "균형", "막다른 길"],
        "keywords_reversed": ["결정", "진실 드러남"],
    },
    "swords_03": {
        "keywords_upright": ["상처", "비탄", "배신"],
        "keywords_reversed": ["치유 시작", "용서", "회복"],
    },
    "swords_04": {
        "keywords_upright": ["휴식", "회복", "명상"],
        "keywords_reversed": ["소진", "번아웃", "회피"],
    },
    "swords_05": {
        "keywords_upright": ["갈등", "패배", "자존심"],
        "keywords_reversed": ["화해", "후회", "양보"],
    },
    "swords_06": {
        "keywords_upright": ["이동", "전환", "평온으로"],
        "keywords_reversed": ["정체", "발이 묶임"],
    },
    "swords_07": {
        "keywords_upright": ["기만", "전략", "회피"],
        "keywords_reversed": ["양심", "자백", "정직"],
    },
    "swords_08": {
        "keywords_upright": ["속박", "무력감", "자기 제한"],
        "keywords_reversed": ["해방", "시야 회복"],
    },
    "swords_09": {
        "keywords_upright": ["불안", "악몽", "죄책감"],
        "keywords_reversed": ["회복", "희망", "두려움 직면"],
    },
    "swords_10": {
        "keywords_upright": ["끝", "배신", "절망"],
        "keywords_reversed": ["회복", "재기", "끝나는 고통"],
    },
    "swords_page": {
        "keywords_upright": ["호기심", "경계", "진실 추구"],
        "keywords_reversed": ["가십", "냉소", "잔꾀"],
    },
    "swords_knight": {
        "keywords_upright": ["추진", "야망", "직진"],
        "keywords_reversed": ["충동", "무모함", "공격성"],
    },
    "swords_queen": {
        "keywords_upright": ["통찰", "독립", "명료"],
        "keywords_reversed": ["냉정", "비판", "고립"],
    },
    "swords_king": {
        "keywords_upright": ["지성", "권위", "공정"],
        "keywords_reversed": ["독선", "냉혹", "권력 남용"],
    },
    # ── Pentacles (대지 / 물질·일·안정) ─────────────────────────────
    "pentacles_ace": {
        "keywords_upright": ["새로운 기회", "번영", "안정"],
        "keywords_reversed": ["기회 상실", "결핍", "불안정"],
    },
    "pentacles_02": {
        "keywords_upright": ["균형", "적응", "우선순위"],
        "keywords_reversed": ["과부하", "불균형", "혼란"],
    },
    "pentacles_03": {
        "keywords_upright": ["협업", "기술", "인정"],
        "keywords_reversed": ["협업 부족", "미숙", "비효율"],
    },
    "pentacles_04": {
        "keywords_upright": ["안정", "보존", "통제"],
        "keywords_reversed": ["인색", "집착", "손실 두려움"],
    },
    "pentacles_05": {
        "keywords_upright": ["결핍", "고난", "소외"],
        "keywords_reversed": ["회복", "도움", "새로운 기회"],
    },
    "pentacles_06": {
        "keywords_upright": ["나눔", "관대", "균형"],
        "keywords_reversed": ["불공정", "빚", "일방적 관계"],
    },
    "pentacles_07": {
        "keywords_upright": ["인내", "평가", "장기 투자"],
        "keywords_reversed": ["조급함", "헛수고", "보상 부족"],
    },
    "pentacles_08": {
        "keywords_upright": ["숙련", "노력", "학습"],
        "keywords_reversed": ["게으름", "정체", "완벽주의"],
    },
    "pentacles_09": {
        "keywords_upright": ["자립", "풍요", "성취"],
        "keywords_reversed": ["사치", "외로움", "의존"],
    },
    "pentacles_10": {
        "keywords_upright": ["유산", "가족", "부"],
        "keywords_reversed": ["가족 분쟁", "손실", "불안정"],
    },
    "pentacles_page": {
        "keywords_upright": ["학습", "새로운 기회", "성실"],
        "keywords_reversed": ["비현실", "미루기", "기회 놓침"],
    },
    "pentacles_knight": {
        "keywords_upright": ["성실", "책임", "꾸준함"],
        "keywords_reversed": ["정체", "보수성", "지루함"],
    },
    "pentacles_queen": {
        "keywords_upright": ["풍요", "실용", "양육"],
        "keywords_reversed": ["자기소홀", "물질주의", "의존"],
    },
    "pentacles_king": {
        "keywords_upright": ["성공", "안정", "풍요"],
        "keywords_reversed": ["탐욕", "부패", "물질주의"],
    },
}


def build_index() -> dict[str, dict]:
    """카드 ID → {name_ko, keywords_upright, keywords_reversed}."""
    out: dict[str, dict] = {}
    out.update(MAJOR)
    for card_id, kw in MINOR.items():
        suit, rank = card_id.split("_", 1)
        out[card_id] = {
            "name_ko": f"{SUIT_KO[suit]} {RANK_KO[rank]}",
            **kw,
        }
    return out


if __name__ == "__main__":
    idx = build_index()
    print(f"total: {len(idx)}")
    for cid in list(idx)[:3] + list(idx)[-3:]:
        print(cid, idx[cid])
