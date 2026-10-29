const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('console',m=>{if(m.type()==='error')console.log('ERR',m.text())});p.on('pageerror',e=>console.log('PAGEERR',e.message));
await p.goto('file://'+process.cwd()+'/index.html');await p.waitForFunction(()=>document.body.dataset.ready,{timeout:20000});await p.waitForTimeout(500);
const S='/tmp/claude-0/-home-user-koshelek/80ff568a-9c3f-5aa2-9dd3-c1517fbdba3b/scratchpad/v2_';
for(const t of process.argv.slice(2)){const t0=Date.now();await p.evaluate(t=>seek(+t),t);await p.screenshot({path:S+t+'.jpg',quality:75,type:'jpeg'});console.log(t,Date.now()-t0,'ms')}
await b.close()})();
