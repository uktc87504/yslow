import json, sys, collections, math
rows = json.load(open(sys.argv[1], encoding='utf-8'))
# лема -> (полярност, изискван падеж на клитиката като експериенцер или None за всеки)
LEX = {
 # негативни
 'безпокоя-(се)': ('neg','Acc'), 'вбеся-(се)': ('neg','Acc'), 'втресе-ме': ('neg','Acc'),
 'дразня-(се)': ('neg','Acc'), 'засегна-(се)': ('neg','Acc'), 'мързи-ме': ('neg','Acc'),
 'мъча-(се)': ('neg','Acc'), 'мъчно': ('neg','Dat'), 'мъка': ('neg','Dat'), 'неприятен': ('neg','Dat'),
 'омръзне-ми': ('neg','Dat'), 'писна': ('neg','Dat'), 'прималее-ми': ('neg','Dat'),
 'разочаровам': ('neg','Acc'), 'разтревожа-(се)': ('neg','Acc'), 'смущавам-(се)': ('neg','Acc'),
 'страх': ('neg','Acc'), 'тежа': ('neg','Dat'), 'унижавам-(се)': ('neg','Acc'), 'уморя-(се)': ('neg','Acc'),
 'уплаша-(се)': ('neg','Acc'), 'ядосвам-(се)': ('neg','Acc'), 'яд': ('neg','Acc'), 'домилее-ми': ('neg','Dat'),
 # позитивни
 'впечатля-(се)': ('pos','Acc'), 'добре': ('pos','Dat'), 'зарадвам-(се)': ('pos','Acc'),
 'интересно': ('pos','Dat'), 'интересувам-(се)': ('pos','Acc'), 'мил': ('pos','Dat'), 'пленя': ('pos',None),
 'поолекне-ми': ('pos','Dat'), 'радвам-(се)': ('pos','Acc'), 'съживявам-(се)': ('pos','Acc'),
 'успокоявам-(се)': ('pos','Acc'), 'удобно': ('pos','Dat'), 'харесвам-(се)': ('pos','Dat'),
 'харесам-(се)': ('pos','Dat'), 'изгодно': ('pos','Dat'), 'изнася-ми': ('pos','Dat'),
 # неутрални експериенцерни
 'хрумне-ми': ('neu','Dat'), 'доще-ми-се': ('neu','Dat'), 'прииска-ми-се': ('neu','Dat'),
 'струва-(си)': ('neu','Dat'), 'случа-(се)': ('neu','Dat'), 'случвам-(се)': ('neu','Dat'),
 'трябва': ('neu','Dat'), 'трябвам': ('neu','Dat'), 'нужен': ('neu','Dat'), 'нужно': ('neu','Dat'),
 'безразличен': ('neu','Dat'), 'изненадам-(се)': ('neu','Acc'), 'смая-(се)': ('neu','Acc'),
 'липсвам': ('neu','Dat'),
}
# ръчни решения за отделни изречения (подниз -> полярност; None = не е експериенцер)
OVR = {
 'Стана ми горещо': 'neg', 'й стана криво': 'neg', 'ще ви стане ясно': 'neu',
 'няма да ти е трудно': 'neg',
 'Понякога ми липсва даже': 'neg', 'Липсват ми двама или трима': 'neg',
 'Липсват й само кубинки': 'neu', 'му липсва ритъм': 'neu',
}
def ovr(r):
    for k, v in OVR.items():
        if k in r['text']:
            if r['head_lemma'] in ('стане','съм','липсвам'): return v
    return 'skip'
out = []
for r in rows:
    pol = None
    o = ovr(r)
    if o != 'skip': pol = o
    elif r['head_lemma'] in LEX:
        p, case = LEX[r['head_lemma']]
        if case is None or case == r['case']: pol = p
    if pol is None: continue
    final = pol
    if r['neg']:
        final = 'neg' if pol == 'pos' else 'neu'
    out.append(dict(r, base=pol, pol=final))
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

def wilson(k, n, z=1.96):
    if not n: return (0, 0)
    p = k/n; d = 1 + z*z/n; c = p + z*z/(2*n); m = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return ((c-m)/d, (c+m)/d)
def report(name, xs):
    c = collections.Counter(x['pol'] for x in xs)
    v = c['neg'] + c['pos']
    lo, hi = wilson(c['neg'], v)
    print(f"{name}: N={len(xs)} neg={c['neg']} pos={c['pos']} neu={c['neu']}  neg share of valenced={c['neg']/v if v else 0:.2f} [95% {lo:.2f}-{hi:.2f}]")
report('всички лица', out)
report('ме/ми', [x for x in out if x['p1sg']])
report('Dat', [x for x in out if x['case']=='Dat'])
report('Acc', [x for x in out if x['case']=='Acc'])
types = collections.defaultdict(set)
for x in out: types[x['base']].add(x['head_lemma'])
print('типове (леми) по базова полярност:', {k: len(v) for k, v in types.items()})
print('всички клитики в корпуса:', len(rows), ' от тях ме/ми:', sum(r['p1sg'] for r in rows))
