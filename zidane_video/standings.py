import json,sys
t={r['team']:dict(r) for r in json.load(open('data_r7.json'))}
for f in sys.argv[1:]:
    prev={k:i for i,k in enumerate(sorted(t,key=lambda k:(-t[k]['pts'],-t[k]['diff'])),1)}
    for a,sa,sb,b in json.load(open(f)):
        for x,y,sx,sy in ((a,b,sa,sb),(b,a,sb,sa)):
            r=t[x];r['diff']+=sx-sy
            if sx>sy:r['w']+=1;r['pts']+=3
            elif sx==sy:r['d']+=1;r['pts']+=1
            else:r['l']+=1
    print('после',f)
    for i,k in enumerate(sorted(t,key=lambda k:(-t[k]['pts'],-t[k]['diff'])),1):
        r=t[k];print(f"{i:2} ({prev[k]-i:+d}) {k:24} {r['w']}-{r['d']}-{r['l']} {r['diff']:+5} {r['pts']}")
