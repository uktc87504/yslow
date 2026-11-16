"""Ръчни корекции след преглед на всички оцветени попадения в извадката."""
import json, sys, collections, math
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from classify_sample import wilson
r = json.load(open(sys.argv[1], encoding='utf-8'))
# X = не е експериенцерна конструкция (клитиката е обект/стимул, или наречие за начин)
DROP = {2, 27, 28, 48, 155, 198, 254, 1909, 186, 168, 693, 1561, 363, 650, 959, 992, 1059, 1277, 1324,
        1587, 1615, 843, 891, 2246, 2527, 2310, 2684, 3046, 2593, 3008, 3049}
NEU = {1216, 1929, 880, 2017, 2181, 3066, 2435}
NEG = {3090}
for i, x in enumerate(r):
    if i in DROP: x['pol'] = None; x['review'] = 'drop'
    elif i in NEU: x['pol'] = 'neu'; x['review'] = 'neu'
    elif i in NEG: x['pol'] = 'neg'; x['review'] = 'neg'
json.dump(r, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for cl in ('ме', 'ми'):
    xs = [x for x in r if x['clitic'] == cl]
    c = collections.Counter(x['pol'] for x in xs); v = c['neg'] + c['pos']; lo, hi = wilson(c['neg'], v)
    print(f"{cl}: лични={len(xs)} неутр={c['neu']} neg={c['neg']} pos={c['pos']} дял={c['neg']/v:.3f} [{lo:.3f}-{hi:.3f}]")
    # чувствителност: без "не ме интересува"/интересува изобщо
    ys = [x for x in xs if x.get('label') != 'интересува']
    c2 = collections.Counter(x['pol'] for x in ys); v2 = c2['neg'] + c2['pos']; lo2, hi2 = wilson(c2['neg'], v2)
    print(f"   без 'интересува': neg={c2['neg']} pos={c2['pos']} дял={c2['neg']/v2:.3f} [{lo2:.3f}-{hi2:.3f}]")
    ys = [x for x in xs if not (x.get('label') == 'приятно' and x['clitic'] == 'ми')]
    c3 = collections.Counter(x['pol'] for x in ys); v3 = c3['neg'] + c3['pos']
    print(f"   без 'приятно ми е' (поздрав): neg={c3['neg']} pos={c3['pos']} дял={c3['neg']/v3:.3f}")
    print('   ', collections.Counter((x['label'], x['pol']) for x in xs if x['pol'] in ('neg', 'pos')).most_common(12))
a = collections.Counter(x['pol'] for x in r if x['clitic'] == 'ме'); b = collections.Counter(x['pol'] for x in r if x['clitic'] == 'ми')
print('2x2', a['neg'], a['pos'], b['neg'], b['pos'])
