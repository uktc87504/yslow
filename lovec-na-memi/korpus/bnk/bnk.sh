#!/bin/bash
# usage: bnk.sh "query" [page]  -> prints JSON
S=/tmp/claude-0/-home-user-yslow/f40c1e64-6683-5eac-959b-f114669b70ac/scratchpad/bnk; J=$S/cj.txt
[ -f $S/tok ] || { curl -sS -m 30 -c $J -b $J https://search.dcl.bas.bg/ | grep -oE '_csrf = "[^"]+"' | cut -d'"' -f2 > $S/tok; }
Q=$(python3 -I -c 'import json,sys; print(json.dumps({"query":sys.argv[1],"meta":{},"aligns":[]},ensure_ascii=False))' "$1")
curl -sS -m 120 -c $J -b $J -e https://search.dcl.bas.bg/ -X POST https://search.dcl.bas.bg/api/search --data-urlencode "csrfmiddlewaretoken=$(cat $S/tok)" --data-urlencode "page=${2:-1}" --data-urlencode "query=$Q"
