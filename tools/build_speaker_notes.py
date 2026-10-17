"""Regenerate the standalone Greek notes from the presentation metadata."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
deck=json.loads((ROOT/'source/deck-content.json').read_text(encoding='utf-8'))
core=sum(bool(slide['minutes']) for slide in deck)
parts=['# Σημειώσεις ομιλητή για την παρουσίαση AI στην παραγωγή λογισμικού',f'{core} κύριες διαφάνειες σε 60 λεπτά και {len(deck)-core} διαφάνειες παραρτήματος. Οι χρόνοι περιλαμβάνουν δραστηριότητες και το τετράλεπτο instructor demo. Όλα τα copy-paste prompts είναι αγγλικά. Το αναλυτικό script δίνεται στο rehearsal-script-el.md.']
elapsed=0
for i,slide in enumerate(deck,1):
    parts.append(f"## {i} {slide['title']}")
    minutes=slide['minutes']
    parts.append(f'{elapsed}-{elapsed+minutes} λεπτά' if minutes else 'Παράρτημα εκτός των 60 λεπτών')
    elapsed+=minutes
    notes=slide['notes'].replace('\\n','\n')
    if 'Copy-paste prompt:\n' in notes:
        text,prompt=notes.split('Copy-paste prompt:\n',1)
        notes=text+'Copy-paste prompt:\n\n```text\n'+prompt.strip()+'\n```'
    parts.append(notes)
    if slide['sources']:
        parts.append('Πηγές: '+', '.join(f'[Πηγή {n}]({url})' for n,url in enumerate(slide['sources'],1)))
assert elapsed==60
(ROOT/'outputs/deck-speaker-notes-el.md').write_text('\n\n'.join(parts)+'\n',encoding='utf-8')
print('Regenerated',len(deck),'slide notes; core timing',elapsed,'minutes.')
