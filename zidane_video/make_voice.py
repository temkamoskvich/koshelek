import json,sys,subprocess
sys.path.insert(0,sys.argv[1])
from synth import say
items=json.load(open('narration.json'))
for it in items:
    say(it['text'],f"voice/{it['id']}.wav",'aleksandr',rate_=1.25)
    it['len']=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f"voice/{it['id']}.wav"]))
holds=[]
def real(tau): return tau+sum(d for h,d in holds if h<tau)
for it in items:
    s=real(it['start']); avail=real(it['end'])-0.25-s
    if it['len']>avail:
        h=it.get('hold',it['start']); holds.append((h,round(it['len']-avail+0.15,3)))
    it['real']=round(real(it['start']),3)
total=real(52.0)
json.dump({'holds':holds,'items':items,'total':total},open('timeline.json','w'),ensure_ascii=False,indent=1)
open('timeline.js','w').write('const HOLDS='+json.dumps(holds)+';const TOTAL='+str(total)+';\n')
for it in items:print(f"{it['id']:7} len={it['len']:.2f} at {it['real']:.2f}")
print('holds',holds,'total',round(total,2))
