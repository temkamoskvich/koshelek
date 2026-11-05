// renders transparent hero images of Zizu and Ушастый for the poster
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--allow-file-access-from-files']});
const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:2});
await p.goto('file://'+process.cwd()+'/index.html');await p.waitForFunction(()=>document.body.dataset.ready);
await p.addStyleTag({content:'.layer,#sub,#bgtext,#mark,#bg{display:none!important} html,body{background:transparent!important}'});
const out=process.argv[2];
const shots={
 zizu:()=>{seek(1);ground.visible=false;P.g.visible=false;renderer.setPixelRatio(2);renderer.setSize(1080,1920,false);
  Z.g.rotation.y=-0.42;Z.head.rotation.set(0.04,0.3,0);Z.mouth.scale.y=0.12;Z.lids.forEach(l=>l.visible=false);
  Z.arms[0].rotation.set(-0.12,0,-0.1);Z.arms[1].rotation.set(0.1,0,0.12);Z.legs.forEach(l=>l.rotation.set(0,0,0));Z.body.scale.y=1;
  key.position.set(-3,8,6);key.intensity=70;rim.intensity=2.2;
  frame([0,2.25,6.2],[0,2.1,0],34,540,1000);renderer.render(scene,camera)},
 ushastyi:()=>{seek(1);ground.visible=false;Z.g.visible=false;renderer.setPixelRatio(2);renderer.setSize(1080,1920,false);
  P.g.position.set(0,1.6,0);P.g.rotation.set(0,0.45,0);P.g.scale.setScalar(1);P.ears.forEach((e,i)=>e.rotation.z=(i?-1:1)*0.12);P.mouth.scale.y=1.2;P.lid.forEach(l=>l.visible=false);P.legs.forEach(l=>l.rotation.x=0.2);
  frame([0,1.75,4.4],[0,1.6,0],38,540,960);renderer.render(scene,camera)}};
for(const k of Object.keys(shots)){await p.evaluate(`(${shots[k].toString()})()`);await p.screenshot({path:`${out}/${k}.png`,omitBackground:true})}
await b.close()})();
