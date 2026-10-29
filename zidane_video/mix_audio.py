import json,subprocess
tl=json.load(open('timeline.json'));T=tl['total']
ins=[];flt=[]
for i,it in enumerate(tl['items']):
    ins+=['-i',f"voice/{it['id']}.wav"]
    flt.append(f"[{i}:a]aresample=44100,adelay={int(it['real']*1000)}:all=1[v{i}]")
n=len(tl['items'])
flt.append(''.join(f'[v{i}]' for i in range(n))+f"amix=inputs={n}:normalize=0,loudnorm=I=-16:TP=-1.5,apad,atrim=0:{T}[voice]")
drone=f"aevalsrc='0.5*sin(2*PI*55*t)+0.3*sin(2*PI*82.41*t)*(0.6+0.4*sin(2*PI*0.1*t))+0.25*sin(2*PI*110.3*t)*(0.5+0.5*sin(2*PI*0.07*t))+0.08*sin(2*PI*164.8*t)*(0.5+0.5*sin(2*PI*0.23*t))':s=44100:d={T}"
flt.append(f"{drone},lowpass=f=500,volume=0.05,afade=t=in:d=2,afade=t=out:st={T-3}:d=3[dr]")
flt.append("[voice][dr]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-i','video_silent.mp4','-filter_complex',';'.join(flt),'-map',f'{n}:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart','zidane_tours_8-10.mp4'],check=True)
