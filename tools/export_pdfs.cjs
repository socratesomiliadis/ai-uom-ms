// Requires Playwright and installed Chrome; uses no development server.
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE_PATH||'playwright');
const root=path.resolve(__dirname,'..');
(async()=>{
 const launch=process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{channel:'chrome'};
 const browser=await chromium.launch({headless:true,...launch});
 try{
  const page=await browser.newPage({viewport:{width:1600,height:958}});
  for(const [source,output] of [['outputs/ai-production-lecture-el.html','outputs/ai-production-lecture-el.pdf'],['build/proposal.html','outputs/lecture-proposal-el.pdf']]){
   await page.goto(pathToFileURL(path.join(root,source)).href);
   await page.evaluate(async()=>{await Promise.all([...document.fonts].map(f=>f.load()));});
   await page.emulateMedia({media:'print'});
   await page.pdf({path:path.join(root,output),printBackground:true,preferCSSPageSize:true,tagged:true});
   console.log('Exported',output);
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
