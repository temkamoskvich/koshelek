import json
base=json.load(open('data_r7.json'))
t={r['team']:dict(r) for r in base}
order=[r['team'] for r in base]
def snapshot(order):
    out=[];rank=0
    for i,k in enumerate(order):
        r=t[k]
        if i==0 or (r['pts'],r['diff'])!=(t[order[i-1]]['pts'],t[order[i-1]]['diff']): rank=i+1
        out.append(dict(team=k,idx=i,rank=rank,w=r['w'],d=r['d'],l=r['l'],diff=r['diff'],pts=r['pts']))
    return out
states=[snapshot(order)];rounds=[]
for x in states[0]: x['chg']=t[x['team']]['chg']
for f in ['r8.json','r9.json','r10.json']:
    ms=json.load(open(f));rounds.append(ms)
    for m in ms:
        a,sa,sb,b=m[:4];draw=len(m)>4
        for x,sx,sy in ((a,sa,sb),(b,sb,sa)):
            r=t[x];r['diff']+=sx-sy
            if draw:r['d']+=1;r['pts']+=1
            elif sx>sy:r['w']+=1;r['pts']+=3
            else:r['l']+=1
    prev={k:i for i,k in enumerate(order)}
    order=sorted(t,key=lambda k:(-t[k]['pts'],-t[k]['diff'],prev[k]))
    states.append(snapshot(order))
open('video_data.js','w').write('const STATES='+json.dumps(states,ensure_ascii=False)+';\n')
for s in states[1:]:print([ (x['rank'],x['team'],x['pts']) for x in s][:9])
# official order after round 10 from the platform (resolves the Мопед/Муслики tie)
OFFICIAL=["Лина Справедливости","Каткон","SaREAL","Мопед","Муслики","Los blancos","Sevastopol","Cherrypie","Bernabeu Bedlam","Олеся не прощает","Natalie Ramos","FC KAKA","ДыханиеКосмоса","Hazardous Burgers","Деды с Чамартина","А игроки? Так вот они"]
last={x['team']:x for x in states[-1]}
assert set(OFFICIAL)==set(last)
states[-1]=[dict(last[k],idx=i,rank=i+1) for i,k in enumerate(OFFICIAL)]
open('video_data.js','w').write('const STATES='+json.dumps(states,ensure_ascii=False)+';\n')
print([(x['rank'],x['team'],x['w'],x['d'],x['l'],x['pts']) for x in states[-1]])
