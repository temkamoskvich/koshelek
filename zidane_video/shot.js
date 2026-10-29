const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/frames.html');await p.waitForFunction(()=>document.body.dataset.ready);await p.waitForTimeout(300);
for(const id of ['intro','table'])await p.locator('#'+id).screenshot({path:`style_${id}.png`});await b.close()})();
