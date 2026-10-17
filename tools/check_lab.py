"""Check the lab evaluator, including multi-file/build freedom and missing evidence."""
from pathlib import Path
import json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent.parent
base=ROOT/'ai-production-lab'
checks=ROOT/'build/free-agent-checks';checks.mkdir(parents=True,exist_ok=True)
results={}
cases=[('legacy',None,'legacy',0),('baseline',None,'acceptance',5),('reference',ROOT/'instructor-assets/reference','acceptance',0)]
cases += [(p.name,p,'acceptance',None) for p in sorted((ROOT/'instructor-assets/mutants').iterdir())]
cases += [('multi-file-resources-build',ROOT/'demo/fixtures/fixed','acceptance',0),('missing-required-cases',ROOT/'instructor-assets/reference','acceptance',0)]
for name,fixture,mode,failures in cases:
    folder=Path(tempfile.mkdtemp(prefix=name+'-',dir=checks));candidate=folder/'candidate'
    shutil.copytree(base,candidate,ignore=shutil.ignore_patterns('.git','target','reports','__pycache__'))
    if fixture:shutil.copytree(fixture,candidate,dirs_exist_ok=True)
    if name=='multi-file-resources-build':
        p=candidate/'pom.xml';s=p.read_text();s=s.replace('</properties>','<lecture.freedom>enabled</lecture.freedom></properties>').replace('<build>','<build><testResources><testResource><directory>src/test/resources</directory><filtering>true</filtering></testResource></testResources>');p.write_text(s)
        resource=candidate/'src/test/resources/agent-choice.txt';resource.parent.mkdir(parents=True,exist_ok=True);resource.write_text('${lecture.freedom}\n')
        (candidate/'src/test/java/edu/ai/FreelyChosenStructureTest.java').write_text('''package edu.ai;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class FreelyChosenStructureTest {
 @Test void candidateBuildResourcesAndHelpersAreEvaluated() throws Exception {
  try (var resource=getClass().getResourceAsStream("/agent-choice.txt")) {
   assertNotNull(resource);
   assertEquals("enabled",new String(resource.readAllBytes(),StandardCharsets.UTF_8).strip());
  }
  assertEquals(new BigDecimal("45.04"),PriceCalculator.calculate(new BigDecimal("50.05"),"STUDENT10"));
 }
}
''')
    if name=='missing-required-cases':
        p=candidate/'pom.xml';p.write_text(p.read_text().replace('</properties>','<skipTests>true</skipTests></properties>'))
    out=folder/'evaluation'
    run=subprocess.run([sys.executable,str(base/'ci/evaluate.py'),'--candidate',str(candidate),'--trusted',str(base),'--mode',mode,'--out',str(out)],capture_output=True,text=True,encoding='utf-8')
    d=json.loads((out/'result.json').read_text(encoding='utf-8'))
    if name=='missing-required-cases':
        assert d['status']=='FAIL' and d['missing_required_tests'] and d['exit_code']==0,d
    else:
        assert d['tests']==(3 if mode=='legacy' else 28 if name=='multi-file-resources-build' else 27),(name,d)
        assert d['required_tests_observed']==(3 if mode=='legacy' else 27),(name,d)
        assert d['errors']==d['skipped']==0,(name,d)
        assert (d['failures']>0 if failures is None else d['failures']==failures),(name,d)
        assert d['status']==('PASS' if failures==0 else 'FAIL'),(name,d)
    assert (run.returncode==0)==(d['status']=='PASS')
    results[name]={k:d[k] for k in ['status','tests','failures','errors','skipped','required_tests','required_tests_observed','project_sha256']}
    print(name,d['status'],d['tests'],'tests;',d['required_tests_observed'],'required cases observed',flush=True)
summary=json.dumps({'date':'2026-10-18','checks':results},indent=2)+'\n'
(checks/'summary.json').write_text(summary)
(ROOT/'instructor-assets/verified-results/free-agent-checks.json').write_text(summary)
print('Complete-project evaluation verified, including helper/resource/build changes and rejection of missing acceptance evidence.')
