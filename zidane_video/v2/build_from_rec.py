import json,subprocess,wave,numpy as np
FPS=30;PAD=0.06;TYKVA_PITCH=1.26  # ~+4 semitones so the pumpkin differs from Zizu
sc=json.load(open('script.json'))
segs={'z':json.load(open('rec/zizu_full.segs.json')),'p':json.load(open('rec/tykva_full.segs.json'))}
src={'z':'rec/zizu_full.mp3','p':'rec/tykva_full.mp3'};idx={'z':0,'p':0}
lines=[];t=0.0;n=0
for s in sc:
    s['start']=round(t,3);cur=t+s['lead']
    for sp,text in s['lines']:
        a,b=segs[sp][idx[sp]];idx[sp]+=1;f=f'voice/{n:02d}.wav'
        af=f"atrim={max(0,a-PAD)}:{b+PAD},asetpts=PTS-STARTPTS,aresample=44100"+(f",rubberband=pitch={TYKVA_PITCH}:formant=preserved" if sp=='p' else '')+",afade=t=in:d=0.03,areverse,afade=t=in:d=0.05,areverse"
        subprocess.run(['ffmpeg','-loglevel','error','-y','-i',src[sp],'-af',af,'-ac','1',f],check=True)
        w=wave.open(f);sr=w.getframerate();x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float);L=len(x)/sr
        hop=sr//FPS;env=np.array([np.sqrt(np.mean(x[i:i+hop]**2)) for i in range(0,len(x),hop)])
        env=np.clip(env/(np.percentile(env,95) or 1),0,1);env=np.where(env<0.12,0,env)
        lines.append(dict(sp=sp,text=text,start=round(cur,3),end=round(cur+L,3),file=f,env=[round(float(e),2) for e in env],scene=s['id']))
        cur+=L+s.get('gap',0.3);n+=1
    t=max(cur-s.get('gap',0.3)+s['tail'],t+s.get('min',0));s['end']=round(t,3)
for s in sc: s.pop('lines')
assert idx['z']==len(segs['z']) and idx['p']==len(segs['p'])
tl=dict(scenes=sc,lines=lines,total=round(t,3))
json.dump(tl,open('timeline.json','w'),ensure_ascii=False)
open('timeline.js','w').write('const TL='+json.dumps(tl,ensure_ascii=False)+';\n')
for s in sc:print(f"{s['id']:7} {s['start']:6.2f}-{s['end']:6.2f}")
print('total',round(t,2))
