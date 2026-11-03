import json,sys,subprocess,wave,array,math
sys.path.insert(0,sys.argv[1])
from synth import say
FPS=30
sc=json.load(open('script.json'));lines=[];t=0.0;n=0
for s in sc:
    s['start']=round(t,3);cur=t+s['lead']
    for sp,text in s['lines']:
        f=f'voice/{n:02d}.wav'
        if sp=='z': say(text,f,'aleksandr',rate_=1.2,pitch=0.95)
        else: say(text,f,'anna',rate_=1.2,pitch=1.35)
        w=wave.open(f);sr=w.getframerate();a=array.array('h',w.readframes(w.getnframes()));L=len(a)/sr
        hop=sr//FPS;env=[math.sqrt(sum(x*x for x in a[i:i+hop])/max(1,len(a[i:i+hop]))) for i in range(0,len(a),hop)]
        pk=sorted(env)[int(len(env)*.95)] or 1;env=[round(min(1,e/pk),2) for e in env]
        lines.append(dict(sp=sp,text=text,start=round(cur,3),end=round(cur+L,3),file=f,env=env,scene=s['id']))
        cur+=L+s.get('gap',0.3);n+=1
    t=max(cur-s.get('gap',0.3)+s['tail'],t+s.get('min',0));s['end']=round(t,3)
for s in sc: s.pop('lines')
json.dump(dict(scenes=sc,lines=lines,total=round(t,3)),open('timeline.json','w'),ensure_ascii=False)
open('timeline.js','w').write('const TL='+json.dumps(dict(scenes=sc,lines=lines,total=round(t,3)),ensure_ascii=False)+';\n')
for s in sc:print(f"{s['id']:7} {s['start']:6.2f}-{s['end']:6.2f}")
print('total',round(t,2))
