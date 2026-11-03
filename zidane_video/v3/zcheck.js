const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('pageerror',e=>console.log('PAGEERR',e.message));
await p.goto('file://'+process.cwd()+'/index.html');await p.waitForFunction(()=>document.body.dataset.ready,{timeout:20000});
const S='/tmp/claude-0/-home-user-koshelek/80ff568a-9c3f-5aa2-9dd3-c1517fbdba3b/scratchpad/zc_';
// turntable: hide UI, frame full body, rotate
await p.addStyleTag({content:'.layer,#sub,#bgtext,#mark{display:none!important}'});
for(const [i,ry,close] of [[0,0,0],[1,0.6,0],[2,Math.PI/2,0],[3,Math.PI,0],[4,0,1],[5,-0.5,1]]){
 await p.evaluate(([ry,close])=>{seek(48.0);Z.g.rotation.set(0,ry,0);Z.arms.forEach(a=>a.rotation.set(0,0,0));Z.legs.forEach(l=>l.rotation.set(0,0,0));Z.body.rotation.set(0,0,0);Z.head.rotation.set(0,0,0);Z.mouth.scale.y=0.12;P.g.visible=false;ball.visible=false;
  if(close)frame([0,2.8,3.2],[0,2.75,0],38,540,960);else frame([0,1.75,9],[0,1.7,0],38,540,960);renderer.render(scene,camera)},[ry,close]);
 await p.screenshot({path:S+i+'.jpg',quality:80,type:'jpeg'})}
await b.close()})();
