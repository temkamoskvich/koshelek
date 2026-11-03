const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/index.html');await p.waitForFunction(()=>document.body.dataset.ready);
await p.addStyleTag({content:'.layer,#sub,#bgtext,#mark{display:none!important}'});
const S='/tmp/claude-0/-home-user-koshelek/80ff568a-9c3f-5aa2-9dd3-c1517fbdba3b/scratchpad/uc_';
for(const [i,ry] of [[0,0],[1,0.7]]){await p.evaluate(ry=>{seek(1.0);Z.g.visible=false;P.g.position.set(0,1.6,0);P.g.rotation.set(0,ry,0);P.g.scale.setScalar(1);frame([0,1.7,4.2],[0,1.6,0],38,540,960);renderer.render(scene,camera)},ry);await p.screenshot({path:S+i+'.jpg',type:'jpeg',quality:80})}
await b.close()})();
