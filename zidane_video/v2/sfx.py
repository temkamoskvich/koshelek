import json,math,wave,numpy as np
SR=44100;rng=np.random.default_rng(5)
tl=json.load(open('timeline.json'));T=tl['total'];S={s['id']:s for s in tl['scenes']};L=tl['lines']
out=np.zeros(int((T+2)*SR))
def put(x,t,g=1.0):
    i=int(t*SR);x=x[:max(0,len(out)-i)];out[i:i+len(x)]+=x*g
def env(n,a=0.005,d=0.2):
    t=np.arange(n)/SR;return np.minimum(1,t/a)*np.exp(-t/d)
def svf(x,fc,q=0.7):  # time-varying lowpass/bandpass (state variable filter)
    fc=np.broadcast_to(fc,x.shape);lp=bp=0.0;y=np.empty_like(x);yb=np.empty_like(x)
    for i in range(len(x)):
        f=2*math.sin(math.pi*min(fc[i],SR/6)/SR);hp=x[i]-lp-q*bp;bp+=f*hp;lp+=f*bp;y[i]=lp;yb[i]=bp
    return y,yb
def whoosh(d=0.5,f0=300,f1=2500):
    n=int(d*SR);x=rng.standard_normal(n);fc=np.geomspace(f0,f1,n);_,b=svf(x,fc,0.5)
    w=np.sin(np.linspace(0,math.pi,n))**2;return b*w/np.max(np.abs(b))
def thump(f0=150,f1=45,d=0.25):
    n=int(d*2.5*SR);t=np.arange(n)/SR;f=f1+(f0-f1)*np.exp(-t/0.04);ph=2*math.pi*np.cumsum(f)/SR
    c=rng.standard_normal(n)*np.exp(-t/0.004)*0.4;return (np.sin(ph)+c)*env(n,0.002,d)
def bonk():
    n=int(0.5*SR);t=np.arange(n)/SR;f=220+500*np.exp(-t/0.03);ph=2*math.pi*np.cumsum(f)/SR
    return (np.sin(ph)+0.4*np.sin(2.7*ph))*env(n,0.001,0.12)
def boing():
    n=int(0.9*SR);t=np.arange(n)/SR;f=320+140*np.sin(2*math.pi*9*t)*np.exp(-t/0.5)+200*np.exp(-t/0.3)
    return np.sin(2*math.pi*np.cumsum(f)/SR)*env(n,0.005,0.35)
def boom(big=False):
    n=int(1.8*SR);t=np.arange(n)/SR;f=48+(70 if big else 40)*np.exp(-t/0.08)
    x=np.sin(2*math.pi*np.cumsum(f)/SR)*env(n,0.003,0.6 if big else 0.4)
    lp,_=svf(rng.standard_normal(n)*env(n,0.001,0.08),np.full(n,900.0));return x+0.6*lp/np.max(np.abs(lp))*env(n,0.001,0.1)
def chime():
    n=int(2.2*SR);t=np.arange(n)/SR;x=np.zeros(n)
    for k,f in enumerate([1046.5,1318.5,1568,2093]):
        i=int(k*0.07*SR);m=n-i;tt=np.arange(m)/SR;x[i:]+=np.sin(2*math.pi*f*tt)*np.exp(-tt/0.6)*(0.5+0.5*np.sin(2*math.pi*6*tt))*0.3
    return x
def clap():
    n=int(0.12*SR);_,b=svf(rng.standard_normal(n),np.full(n,1500.0),0.8);x=b*env(n,0.001,0.02)
    for k in (1,2):j=int(k*0.007*SR);x[j:]+=0.6*b[:n-j]*env(n-j,0.001,0.02)
    return x/np.max(np.abs(x))
def groan():
    n=int(1.6*SR);t=np.arange(n)/SR;f=85+8*np.sin(2*math.pi*5*t)-15*t;ph=2*math.pi*np.cumsum(f)/SR
    saw=2*((ph/(2*math.pi))%1)-1;lp,_=svf(saw,np.full(n,700.0),0.9);w=np.sin(np.linspace(0,math.pi,n))**0.7
    return lp*w/np.max(np.abs(lp))
def tick(f=1800):
    n=int(0.05*SR);t=np.arange(n)/SR;return np.sin(2*math.pi*f*t)*env(n,0.0005,0.012)
def thunder():
    n=int(3.5*SR);t=np.arange(n)/SR;lp,_=svf(rng.standard_normal(n),np.full(n,180.0),0.8)
    a=np.exp(-t/1.1)*np.minimum(1,t/0.05)*(0.6+0.4*np.abs(np.sin(2*math.pi*1.7*t+np.sin(9*t))));return lp*a/np.max(np.abs(lp))
def sting():
    n=int(1.6*SR);t=np.arange(n)/SR;x=np.zeros(n)
    for f in (880,932,1245,1319):x+=np.sin(2*math.pi*f*t+3*np.sin(2*math.pi*7*t))*0.22
    x*=env(n,0.004,0.5);_,b=svf(rng.standard_normal(n),np.full(n,3000.0),0.6);return x+0.5*b/np.max(np.abs(b))*env(n,0.001,0.15)
def prop(d):
    # rotor chop (band-passed noise gated ~22 Hz) + small motor whine, sits in the 0.8-3 kHz range phones reproduce
    n=int(d*SR);t=np.arange(n)/SR;_,b=svf(rng.standard_normal(n),np.full(n,1400.0),0.35);b/=np.max(np.abs(b))
    chop=0.25+0.75*(0.5+0.5*np.sin(2*math.pi*22*t))**3
    ph=2*math.pi*(180*t+3*np.sin(2*math.pi*0.7*t));whine=0.25*np.sign(np.sin(ph))*0.5+0.15*np.sin(2*ph)
    lp,_=svf(whine,np.full(n,1600.0),0.7)
    fade=np.minimum(1,np.minimum(t/0.3,(d-t)/0.3));return (0.8*b*chop+lp)*fade
lines=lambda sid:[l for l in L if l['scene']==sid]
put(thunder(),0.0,0.55)
for s in tl['scenes']:
    st,en,lt0=s['start'],s['end'],s['start']
    if s['id']!='open': put(whoosh(0.45,500,3500),st-0.2,0.22)
    G={'close':0.32,'count':0.32,'card':0.22,'battle':0.22,'reveal':0.2,'table':0.16}[s['type']]
    pe=en
    if s['id']=='head': pe=st+lines('head')[2]['end']-st+0.25  # pumpkin is knocked out of frame
    put(prop(pe-st),st,G)
    if s['id']=='head': put(whoosh(0.9,1800,400)*0.6,pe-0.05,0.3)
    if s['type']=='table' and s['state']>0: put(whoosh(1.75,150,1800),st+0.35,0.16);put(thump(120,50,0.15),st+2.1,0.35)
    if s['type']=='card':
        put(thump(160,50,0.2),st+0.25,0.45)
        if s['card']==0: put(thump(220,60,0.12),st+0.9,0.8);put(whoosh(0.6,800,4000),st+0.92,0.35)
        if s['card']==1:
            put(groan(),st+0.3,0.35);prev=16
            for k in range(1,400):
                tt=0.6+k*0.003;p=min(1,(tt-0.6)/1.2);v=round(16-7*(1-(1-p)**3))
                if v!=prev: put(tick(1500+60*(16-v)),st+tt,0.25);prev=v
                if p>=1:break
        if s['card']==2:
            th=lines('head')[2]['end']-st+0.15
            put(whoosh(0.35,400,2000),st+th-0.55,0.2);put(bonk(),st+th+0.04,0.75);put(boing(),st+th+0.1,0.35);put(whoosh(0.8,2500,300),st+th+0.1,0.3)
    if s['type']=='battle':
        for a in (0.2,0.4,0.6,0.7,0.85): put(tick(1200),st+a,0.3)
    if s['type']=='count':
        cl=lines('count')
        for i in (1,2,3): put(boom(i==3),cl[i]['start']-0.05,0.6 if i<3 else 0.85)
    if s['type']=='reveal':
        put(chime(),st+0.5,0.45);k=0
        while True:
            tt=(math.pi/2+k*math.pi)/9;k+=1
            if st+tt>en-0.1:break
            put(clap(),st+tt+rng.uniform(-0.01,0.01),0.28)
        n=int((en-st)*SR);_,b=svf(rng.standard_normal(n),np.full(n,1800.0),0.7);put(b/np.max(np.abs(b))*np.minimum(1,np.arange(n)/SR/0.5)*np.minimum(1,(en-st-np.arange(n)/SR)/0.6),st,0.05)
    if s['id']=='outro':
        bt=lines('outro')[1]['start'];put(sting(),bt-0.02,0.5);put(boom(True),bt-0.02,0.6);put(whoosh(0.4,300,3000),bt+0.1,0.25)
out=out[:int(T*SR)];out=np.tanh(out*1.1)/1.1*0.95  # soft clip instead of global normalisation
w=wave.open('sfx.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
print('sfx ok',round(len(out)/SR,2))
