#!/bin/bash
# usage: bnkm.sh "query" 'META_JSON' [page]
S=/tmp/claude-0/-home-user-yslow/f40c1e64-6683-5eac-959b-f114669b70ac/scratchpad/bnk; J=$S/cj2.txt
[ -s $S/tok2 ] || { curl -sS -m 30 -c $J -b $J https://search.dcl.bas.bg/ | grep -oE '_csrf = "[^"]+"' | cut -d'"' -f2 > $S/tok2; }
Q=$(python3 -I -c 'import json,sys; print(json.dumps({"query":sys.argv[1],"meta":json.loads(sys.argv[2]),"aligns":[]},ensure_ascii=False))' "$1" "${2:-{\}}")
curl -sS -m 120 -c $J -b $J -e https://search.dcl.bas.bg/ -X POST https://search.dcl.bas.bg/api/search --data-urlencode "csrfmiddlewaretoken=$(cat $S/tok2)" --data-urlencode "page=${3:-1}" --data-urlencode "query=$Q"
