const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/video.html');await p.waitForFunction(()=>document.body.dataset.ready);await p.waitForTimeout(300);
for(const t of process.argv.slice(2)){await p.evaluate(t=>seek(+t),t);await p.screenshot({path:`/tmp/claude-0/-home-user-koshelek/80ff568a-9c3f-5aa2-9dd3-c1517fbdba3b/scratchpad/prev_${t}.jpg`,quality:70,type:'jpeg'})}
await b.close()})();
