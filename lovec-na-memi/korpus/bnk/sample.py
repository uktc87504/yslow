import json, random, re, subprocess, sys, time, html
S = '/tmp/claude-0/-home-user-yslow/f40c1e64-6683-5eac-959b-f114669b70ac/scratchpad'
word, npages, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
def q(page):
    r = subprocess.run([S + '/scripts/bnk.sh', word, str(page)], capture_output=True, text=True)
    return json.loads(r.stdout)
first = q(1); total = first['count']; pages = (total + 29) // 30
random.seed(seed)
picked = sorted(random.sample(range(1, pages + 1), npages))
span = re.compile(r'<span class="(word(?: match)?)" title="([^"]*)">(.*?)</span>', re.S)
res = []
for i, p in enumerate(picked):
    try: d = q(p)
    except Exception as e:
        print('fail', p, e, file=sys.stderr); time.sleep(5); continue
    for f, idx, h in d['results']:
        toks = [dict(m=c == 'word match', tag=t.strip(), w=html.unescape(re.sub(r'<[^>]+>', '', x)).strip())
                for c, t, x in span.findall(h)]
        res.append(dict(file=f, id=idx, page=p, toks=[t for t in toks if t['w'] or t['m']]))
    time.sleep(0.5)
    if i % 10 == 0: print(i, p, len(res), file=sys.stderr)
json.dump(dict(word=word, total=total, pages=picked, sents=res), open(out, 'w', encoding='utf-8'), ensure_ascii=False)
print(word, total, len(res))
