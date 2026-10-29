import json,math,sys,re
def load_sil(f): return [tuple(map(float,l.split())) for l in open(f) if l.strip()]
def weight(t): return len(re.findall(r'\w',t))+2*len(re.findall(r'[.!?…—,:]',t))
def align(silf,texts,total):
    sil=load_sil(silf); start=sil[0][1] if sil and sil[0][0]<0.05 else 0.0
    end=total
    if sil and sil[-1][1]>=total-0.05: end=sil[-1][0]
    cands=[s for s in sil if s[0]>start+0.05 and s[1]<end-0.05]
    K=len(texts);w=[weight(t) for t in texts];speech=end-start-sum(s[2] for s in cands)*0.5
    rate=speech/sum(w)
    # dp over candidates: state (i line, j cand index used as end of line i)
    N=len(cands);INF=1e18
    pts=[(None,start)]+[(c,c[0]) for c in cands]  # boundary starts
    def segcost(a,b,li):  # segment from end of cand a to start of cand b (b None => end)
        s=start if a<0 else cands[a][1]; e=end if b is None else cands[b][0]
        d=e-s
        if d<=0.15: return INF
        inner=sum(c[2] for c in cands[(a+1 if a>=0 else 0):(b if b is not None else N)] )
        long_inner=sum(max(0,c[2]-0.28) for c in cands[(a+1 if a>=0 else 0):(b if b is not None else N)])
        est=w[li]*rate+0.0
        return (math.log((d-inner*0.5)/est))**2+6*long_inner
    best={(-1,-1):(0,None)}
    for li in range(K):
        nxt={}
        for (pli,pa),(c,_) in best.items():
            ends=[None] if li==K-1 else range(pa+1,N)
            for b in ends:
                cc=c+segcost(pa,b,li)-(0 if b is None else 1.5*min(cands[b][2],0.5))
                key=(li,b if b is not None else N)
                if key not in nxt or cc<nxt[key][0]: nxt[key]=(cc,((pli,pa),))
        best={k:(v[0],v[1]) for k,v in nxt.items()}
        # keep backpointers
        globals().setdefault('BP',[]).append(nxt)
    # backtrack
    bp=globals()['BP'];key=(K-1,N);cuts=[]
    for li in range(K-1,-1,-1):
        cuts.append(key[1]);key=bp[li][key][1][0]
    cuts=cuts[::-1]
    segs=[];s=start
    for li,b in enumerate(cuts):
        e=end if b==N else cands[b][0];segs.append((round(s,3),round(e,3)));s=end if b==N else cands[b][1]
    globals()['BP']=[]
    return segs
if __name__=='__main__':
    sc=json.load(open('../script.json'))
    for who,fn in (('p','tykva_full'),('z','zizu_full')):
        texts=[t for s in sc for sp,t in s['lines'] if sp==who]
        import subprocess
        total=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',fn+'.mp3']))
        segs=align(fn+'.sil',texts,total)
        json.dump(segs,open(fn+'.segs.json','w'))
        for (a,b),t in zip(segs,texts): print(f"{who} {a:6.2f}-{b:6.2f} ({b-a:4.2f}s) {t}")
