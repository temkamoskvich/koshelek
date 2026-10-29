const {chromium}=require('playwright');const {spawn}=require('child_process');
(async()=>{const FPS=30,out=process.argv[2]||'silent.mp4';
const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('pageerror',e=>console.log('PAGEERR',e.message));
await p.goto('file://'+process.cwd()+'/index.html');await p.waitForFunction(()=>document.body.dataset.ready);await p.waitForTimeout(800);
const n=Math.round(await p.evaluate(()=>TOTAL)*FPS);
const ff=spawn('ffmpeg',['-loglevel','error','-y','-f','image2pipe','-framerate',''+FPS,'-i','-','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',out],{stdio:['pipe','inherit','inherit']});
for(let i=0;i<n;i++){await p.evaluate(t=>seek(t),i/FPS);const buf=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%300==0)console.log('frame',i,'/',n,new Date().toISOString())}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('done')})();
