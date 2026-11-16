import json, re, sys, collections
FUNC = set('е се не да ще беше бе си са съм сме сте било бил била ли пък на мен мене нас то и а но че що защо как какво кой която което които където когато ако или все още вече пак така много малко много толкова само даже дори просто наистина много ей ох о ах хей ами ето там тук сега после тогава вие ти аз той тя те ние вие той ни ви го му я ѝ й им ги ме ми те ти за от в във с със по при към до без над под между през след пред около вместо'.split())
PUNCT = re.compile(r'[.,!?;:…—–"„“”«»()\[\]]')
data = json.load(open(sys.argv[1], encoding='utf-8'))
target = data['word']
cnt = collections.Counter()
kinds = collections.Counter()
n = 0
for s in data['sents']:
    toks = s['toks']
    for i, t in enumerate(toks):
        if not t['m']:
            continue
        w = PUNCT.sub('', t['w']).lower()
        if w != target:
            continue
        kind = 'poss' if 'POSS' in t['tag'] else ('pers' if t['tag'].startswith('P') else 'other:' + t['tag'][:6])
        kinds[kind] += 1
        if kind != 'pers':
            continue
        n += 1
        seen = set()
        for d in (1, -1, 2, -2):
            j = i + d
            if j < 0 or j >= len(toks):
                continue
            # спира на граница на клауза
            lo, hi = sorted((i, j))
            if any(PUNCT.search(toks[k]['w']) for k in range(lo, hi)):
                continue
            u = PUNCT.sub('', toks[j]['w']).lower()
            if not u or u in FUNC or u in seen:
                continue
            seen.add(u)
            cnt[u] += 1
print(target, 'видове:', dict(kinds), 'лични:', n)
for w, c in cnt.most_common(int(sys.argv[2]) if len(sys.argv) > 2 else 150):
    print(c, w)
