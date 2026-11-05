const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});
const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:2});
await p.goto('file://'+process.cwd()+'/poster.html');await p.waitForFunction(()=>document.body.dataset.ready);await p.waitForTimeout(400);
await p.screenshot({path:process.argv[2]||'afisha_tur11.png'});await b.close()})();
