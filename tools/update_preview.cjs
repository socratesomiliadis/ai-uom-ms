const fs=require('node:fs');const path=require('node:path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE_PATH||'playwright');
const root=path.resolve(__dirname,'..');
(async()=>{
 const launch=process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{channel:'chrome'};
 const browser=await chromium.launch({headless:true,...launch});
 try{
  const page=await browser.newPage({viewport:{width:1636,height:936},deviceScaleFactor:1});
  const imgs=[1,9,18,19].map(n=>'<img src="data:image/png;base64,'+fs.readFileSync(path.join(root,`build/deck-qa/slide-${String(n).padStart(2,'0')}.png`)).toString('base64')+'">').join('');
  await page.setContent('<html><head><style>*{box-sizing:border-box}body{margin:0;padding:12px;background:#172720;display:grid;grid-template-columns:800px 800px;gap:12px}img{width:800px;height:450px;display:block}</style></head><body>'+imgs+'</body></html>');
  await page.evaluate(()=>Promise.all([...document.images].map(im=>im.decode())));
  await page.screenshot({path:path.join(root,'outputs/lecture-preview.png')});
 }finally{await browser.close();}
 console.log('Updated lecture preview.');
})().catch(e=>{console.error(e);process.exitCode=1;});
