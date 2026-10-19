import sys, glob, json, collections
SHORT = {'ме','те','го','я','ни','ви','ги','ми','ти','му','ѝ','й','им','си','се'}
def sents(path):
    meta, toks = {}, []
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line:
            if toks: yield meta, toks
            meta, toks = {}, []
        elif line.startswith('#'):
            if ' = ' in line:
                k, v = line[2:].split(' = ', 1); meta[k] = v
        else:
            c = line.split('\t')
            if '-' in c[0] or '.' in c[0]: continue
            toks.append(c)
rows = []
seen = set()
nsent = 0
ntok = 0
for p in sorted(glob.glob(sys.argv[1] + '/*.conllu')):
    for meta, toks in sents(p):
        tx = meta.get('text','')
        if tx in seen: continue
        seen.add(tx); nsent += 1; ntok += len(toks)
        byid = {t[0]: t for t in toks}
        for t in toks:
            form = t[1].lower(); feats = t[5]
            if form not in SHORT or form in ('си', 'се') or t[3] != 'PRON': continue
            if 'Case=Acc' not in feats and 'Case=Dat' not in feats: continue
            if 'Poss=Yes' in feats: continue
            head = byid.get(t[6])
            if not head: continue
            neg = any(u[6] == head[0] and u[2] == 'не' for u in toks) or any(u[6] == t[6] and u[2]=='не' for u in toks)
            refl = any(u[6] == head[0] and u[1].lower() == 'се' for u in toks)
            person = 'Person=1' in feats and 'Number=Sing' in feats
            rows.append(dict(form=form, case='Dat' if 'Case=Dat' in feats else 'Acc', p1sg=person,
                             head_lemma=head[2], head_form=head[1].lower(), head_upos=head[3], deprel=t[7],
                             neg=neg, refl=refl, sid=meta.get('sent_id',''), text=meta.get('text','')))
json.dump(rows, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False)
print(nsent, 'unique sentences,', ntok, 'tokens,', len(rows), 'clitics;', sum(r['p1sg'] for r in rows), 'ме/ми')
