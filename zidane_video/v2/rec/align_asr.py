import json,re,difflib,subprocess
norm=lambda w:re.sub(r'[^а-яa-z0-9]','',w.lower().replace('ё','е'))
sc=json.load(open('../script.json'))
for who,fn in (('p','tykva_full'),('z','zizu_full')):
    texts=[t for s in sc for sp,t in s['lines'] if sp==who]
    words=json.load(open(fn.split('_')[0]+'_words.json'))
    aw=[norm(w) for w,_ in words];at=[t for _,t in words]
    sw=[];owner=[]
    for i,t in enumerate(texts):
        for w in t.split():
            n=norm(w)
            if n:sw.append(n);owner.append(i)
    sm=difflib.SequenceMatcher(None,sw,aw,autojunk=False);m={}
    for a,b,n in sm.get_matching_blocks():
        for k in range(n):m[a+k]=b+k
    # fuzzy fill: for unmatched script words, match by similarity within opcodes
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=='replace':
            for k in range(i1,i2):
                best=max(range(j1,j2),key=lambda j:difflib.SequenceMatcher(None,sw[k],aw[j]).ratio())
                if difflib.SequenceMatcher(None,sw[k],aw[best]).ratio()>0.5:m[k]=best
    first=[];last=[]
    for i in range(len(texts)):
        ks=[k for k in range(len(sw)) if owner[k]==i and k in m]
        first.append(at[m[ks[0]]] if ks else None);last.append(at[m[ks[-1]]] if ks else None)
    sil=[tuple(map(float,l.split())) for l in open(fn+'.sil') if l.strip()]
    total=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',fn+'.mp3']))
    segs=[];start=sil[0][1] if sil and sil[0][0]<0.05 else 0.0
    for i in range(len(texts)):
        if i==len(texts)-1:
            end=sil[-1][0] if sil and sil[-1][1]>=total-0.05 else total
        else:
            lo=last[i]+0.05;hi=first[i+1]+0.6
            c=[s for s in sil if s[0]>=lo and s[1]<=hi and s[1]<total-0.05]
            if not c: raise SystemExit(f'no gap {who}{i} {lo}-{hi}')
            g=max(c,key=lambda s:s[2]);end=g[0]
        segs.append((round(start,3),round(end,3)))
        if i<len(texts)-1:start=g[1]
    json.dump(segs,open(fn+'.segs.json','w'))
    for (a,b),t,f in zip(segs,texts,first):print(f"{who} {a:6.2f}-{b:6.2f} first={f} | {t}")
