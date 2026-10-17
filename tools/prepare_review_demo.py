"""Prepare a standalone, local instructor demo repository and portable Git bundle."""
from pathlib import Path
import argparse, shutil, subprocess

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--destination', default=str(ROOT / 'build/ai-review-demo'))
args = parser.parse_args()
dest = Path(args.destination).resolve()
if dest.exists():
    raise SystemExit('Destination already exists. Reuse it, or specify a new --destination. Nothing was overwritten.')
if dest == ROOT or ROOT.is_relative_to(dest):
    raise SystemExit('Destination cannot contain or replace the authoring repository.')
dest.mkdir(parents=True)
ignored = shutil.ignore_patterns('.git', 'target', 'reports', '.eval-work', '__pycache__', '*.log')
shutil.copytree(ROOT / 'ai-production-lab', dest, dirs_exist_ok=True, ignore=ignored)
source = Path('src/main/java/edu/ai/PriceCalculator.java')
shutil.copy2(ROOT / 'instructor-assets/reference' / source, dest / source)
shutil.copy2(ROOT / 'demo/.coderabbit.yaml', dest / '.coderabbit.yaml')
(dest / 'README.md').write_text('''# Instructor AI review demo

This is the separate instructor demo for the AI software engineering lecture.
The main branch is a correct baseline. demo/review-bug introduces a deliberate,
handwritten rounding regression. demo/review-fixed contains a prepared repair
for fallback. No branch is claimed to be actual AI output.

Read ticket.md for the contract. The acceptance job is ticket-evaluation.
Legacy demo is a separate demonstration check. CodeRabbit is installed through
the GitHub App, not an API key or a workflow. It reviews open PRs automatically.
The instructor passes a valid finding to a free implementation chat and commits
the fix manually. CI reruns; an AI can summarize the final actual evidence.
Merge stays under human control. This is not an autonomous repair/merge agent.
''', encoding='utf-8')

def git(*args):
    subprocess.run(['git', '-C', str(dest), *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    git('init', '-b', 'main')
    # Local fixture commits use a neutral identity; personal Git settings are untouched.
    git('config', 'user.name', 'AI lecture demo fixtures')
    git('config', 'user.email', 'lecture-demo@example.invalid')
    git('add', '.')
    git('update-index', '--chmod=+x', 'mvnw')
    git('commit', '-m', 'Prepare correct pricing baseline and free PR reviewer configuration')
    git('switch', '-c', 'demo/review-bug')
    shutil.copy2(ROOT / 'demo/fixtures/bug' / source, dest / source)
    git('add', source.as_posix())
    git('commit', '-m', 'Introduce deliberate rounding regression for classroom review')
    git('switch', '-c', 'demo/review-fixed')
    shutil.copy2(ROOT / 'demo/fixtures/fixed' / source, dest / source)
    git('add', source.as_posix())
    git('commit', '-m', 'Restore discount-first rounding for prepared fallback')
    git('switch', 'main')
    bundle = ROOT / 'outputs/ai-review-demo.bundle'
    git('bundle', 'create', str(bundle), '--all')
    git('bundle', 'verify', str(bundle))
    # Subsequent real instructor commits should inherit the user's normal identity.
    git('config', '--local', '--unset', 'user.name')
    git('config', '--local', '--unset', 'user.email')
except subprocess.CalledProcessError as error:
    raise SystemExit(error.stderr.decode(errors='replace')) from error
print('Prepared local repository:', dest)
print('Prepared portable Git bundle:', bundle)
print('Branches: main, demo/review-bug, demo/review-fixed. No remote configured; nothing published.')
