"""Run the prepared demo states locally; this does not call an AI service."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,urllib.request

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'build/verification-deps'))
import yaml,jsonschema

schema_url='https://coderabbit.ai/integrations/schema.v2.json'
with urllib.request.urlopen(schema_url,timeout=30) as response:
    schema_bytes=response.read()
schema=json.loads(schema_bytes)
config=yaml.safe_load((ROOT/'demo/.coderabbit.yaml').read_text(encoding='utf-8'))
jsonschema.validators.validator_for(schema)(schema).validate(config)
print('CodeRabbit configuration validates against the published JSON schema.',flush=True)

repo=ROOT/'build/ai-review-demo'
policy=ROOT/'build/ai-review-policy'
if not (repo/'.git').exists():raise SystemExit('Run tools/prepare_review_demo.py first.')
def git(*args):
    return subprocess.check_output(['git','-C',str(repo),*args],text=True,stderr=subprocess.STDOUT).strip()
assert git('status','--porcelain')==''
if not policy.exists():git('worktree','add','--detach',str(policy),'main')
result_root=ROOT/'demo/verified-results';result_root.mkdir(exist_ok=True)
checks={}
cases=[('main','main','acceptance',0),('bug-legacy','demo/review-bug','legacy',0),('bug','demo/review-bug','acceptance',3),('fixed','demo/review-fixed','acceptance',0)]
try:
    for name,branch,mode,expected_failures in cases:
        git('switch',branch)
        out=ROOT/'build/demo-checks'/name
        command=[sys.executable,str(policy/'ci/evaluate.py'),'--candidate',str(repo),'--trusted',str(policy),'--mode',mode,'--out',str(out)]
        run=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
        report=json.loads((out/'result.json').read_text(encoding='utf-8'))
        assert report['tests']==(3 if mode=='legacy' else 27),(name,report)
        assert report['failures']==expected_failures and report['errors']==report['skipped']==0,(name,report)
        assert (run.returncode==0)==(expected_failures==0)
        if branch!='main':
            scope=subprocess.run([sys.executable,str(policy/'ci/check_scope.py'),str(repo),git('rev-parse','main')],capture_output=True,text=True)
            assert scope.returncode==0,scope.stdout
        target=result_root/name;target.mkdir(exist_ok=True)
        shutil.copy2(out/'result.json',target/'result.json')
        checks[name]={'branch':branch,'command':['python','ci/evaluate.py','--candidate','<demo-repository>','--trusted','<reviewed-main-checkout>','--mode',mode,'--out','<reports>'],**report}
        print(name,report['status'],report['tests'],'tests',report['failures'],'failures',flush=True)
finally:git('switch','main')

assert git('diff','--name-only','main','demo/review-fixed')=='src/main/java/edu/ai/PriceCalculator.java'
summary={'date':'2026-10-18','scope':'Local Windows execution only. CodeRabbit review and hosted GitHub CI NOT RUN. Fixtures are handwritten.','configuration_schema':{'url':schema_url,'sha256':hashlib.sha256(schema_bytes).hexdigest(),'valid':True},'java_version':subprocess.check_output(['java','-version'],stderr=subprocess.STDOUT,text=True).splitlines()[0],'checks':checks,'scope_checks':'Both PR branches change only PriceCalculator.java; fixed PR retains the named-constants refactor.'}
(result_root/'verification-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Saved local evidence. No external AI or hosted CI run claimed.')
