"""Разпространение на топ 10 негативни ме/ми конструкции в БНК: по период, устна реч и жанр."""
import json, random, subprocess, sys, time, collections

S = '/tmp/claude-0/-home-user-yslow/f40c1e64-6683-5eac-959b-f114669b70ac/scratchpad'
OUT = sys.argv[1]
TOP = [
    ('трудно ми е', ['трудно ми', 'ми е трудно', 'ми беше трудно']),
    ('боли ме', ['боли/F/ ме']),
    ('страх ме е', ['страх ме']),
    ('плаши ме', ['плаши/F/ ме', 'уплаши/F/ ме']),
    ('мъчи ме', ['мъчи/F/ ме', 'измъчва/F/ ме']),
    ('жал ми е', ['жал ми', 'ми е жал', 'ми беше жал']),
    ('мъчно ми е', ['мъчно ми', 'ми е мъчно', 'ми беше мъчно']),
    ('омръзна ми', ['омръзна/F/ ми']),
    ('тревожи ме', ['тревожи/F/ ме', 'разтревожи/F/ ме']),
    ('пречи ми', ['пречи/F/ ми']),
    ('дразни ме', ['дразни/F/ ме']),
]
BASE = [('ме (всички)', ['ме']), ('ми (всички)', ['ми']), ('и (основа)', ['и'])]
PERIODS = {'1900–1944': '[1900:1944]', '1945–1989': '[1945:1989]', '1990–2009': '[1990:2009]', '2010–2026': '[2010:2026]'}


def call(q, meta=None, page=1):
    for k in range(4):
        r = subprocess.run([S + '/scripts/bnkm.sh', q, json.dumps(meta or {}, ensure_ascii=False), str(page)],
                           capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            time.sleep(0.4)
            return d
        except Exception:
            time.sleep(2 ** (k + 1))
    return {}


res = {}
random.seed(7)
for label, pats in TOP + BASE:
    rec = dict(total=0, periods=collections.Counter(), spoken=0, genres=collections.Counter(), sampled=0)
    for q in pats:
        d = call(q); n = d.get('count') or 0; rec['total'] += n
        for pl, rng in PERIODS.items():
            rec['periods'][pl] += call(q, {'year_of_creation': rng}).get('count') or 0
        rec['spoken'] += call(q, {'medium': 'spoken'}).get('count') or 0
    # жанр: случайни страници от основната заявка
    q = pats[0]; n = call(q).get('count') or 0; pages = max(1, (n + 29) // 30)
    for p in random.sample(range(1, pages + 1), min(8 if label[0] != 'и' else 20, pages)):
        for f, _, _ in call(q, None, p).get('results', []):
            rec['genres'][f.split('/')[0]] += 1; rec['sampled'] += 1
    res[label] = rec
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(label, rec['total'], dict(rec['periods']), rec['spoken'], rec['genres'].most_common(4), flush=True)
print('done')
