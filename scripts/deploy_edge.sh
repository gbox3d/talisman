#!/usr/bin/env bash
# talisman 라이브 뽑기 엣지 API(/api/{n})를 Deno Deploy에 재배포한다.
#
# 사전 준비:
#   - deno 설치 (https://deno.com)
#   - 환경변수 DENO_DEPLOY_TOKEN 에 access token (ddp_...)
#       발급: https://console.deno.com/account/access-tokens → New Access Token
#       또는 토큰 없이 직접 `deno deploy` 실행 시 브라우저 로그인으로 인증됨.
#
# 이 스크립트는 .git / 카드 이미지(23MB) / _raw(23MB)를 빼고,
# 엣지가 실제로 쓰는 파일(코드 + cards.json + spreads.json)만 임시 폴더에 모아 올린다.
#
# 최초 1회 앱 생성은 이미 완료됨(아래 create 명령은 기록용 주석).
# 빌드 설정(dynamic / entrypoint deno/main.ts / region global)은 서버에 저장돼 있어
# 재배포 때는 --org/--app/--prod 만 있으면 그 설정을 재사용한다.
#
#   # 최초 1회만 (앱이 없을 때):
#   # cd <staging> && deno deploy create --org gbox3d --app talisman \
#   #   --source local --runtime-mode dynamic --entrypoint deno/main.ts \
#   #   --do-not-use-detected-build-config --region global
set -euo pipefail

ORG="${DENO_DEPLOY_ORG:-gbox3d}"
APP="${DENO_DEPLOY_APP:-talisman}"
SRC="$(cd "$(dirname "$0")/.." && pwd)"   # 저장소 루트

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/deno" "$STAGE/public/cards"
cp "$SRC/deno/main.ts" "$SRC/deno/deck.ts" "$SRC/deno/deno.json" "$STAGE/deno/"
cp "$SRC/public/cards/cards.json" "$STAGE/public/cards/"
cp "$SRC/public/spreads.json" "$STAGE/public/"
cat > "$STAGE/deno.jsonc" <<EOF
{ "deploy": { "org": "$ORG", "app": "$APP" } }
EOF

echo "배포 대상: org=$ORG app=$APP  (업로드 $(du -sh "$STAGE" | cut -f1))"
cd "$STAGE"
deno deploy --prod --org "$ORG" --app "$APP"
