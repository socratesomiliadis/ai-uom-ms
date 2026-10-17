from pathlib import Path
import json, base64, html, re, struct

ROOT=Path(__file__).resolve().parents[2]
BUILD=Path(__file__).resolve().parent
OUT=ROOT/'outputs'
data=json.loads((ROOT/'source/deck-content.json').read_text(encoding='utf-8'))
H=html.escape

def icon(name):
    paths={
      'left':'<path d="m14 6-6 6 6 6"/>',
      'right':'<path d="m10 6 6 6-6 6"/>',
      'expand':'<path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5"/>',
      'notes':'<path d="M5 3h14v18H5zM8 7h8M8 11h8M8 15h5"/>',
      'grid':'<path d="M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z"/>',
      'close':'<path d="m6 6 12 12M18 6 6 18"/>',
      'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
      'play':'<path d="m9 5 10 7-10 7z"/>',
      'pause':'<path d="M9 5v14M15 5v14"/>',
      'reset':'<path d="M3 10a9 9 0 1 1 2 8M3 4v6h6"/>',
      'check':'<path d="m5 12 4 4L19 6"/>',
      'link':'<path d="M14 3h7v7M21 3l-9 9M10 4H4v16h16v-6"/>',
      'print':'<path d="M6 9V3h12v6M6 17H3V9h18v8h-3M6 14h12v7H6z"/>',
      'info':'<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7v.01"/>',
    }
    return '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+paths[name]+'</svg>'

def label(text): return '<p class="label">'+text+'</p>'
def title(text): return '<h2>'+text+'</h2>'
def cols(a,b,extra=''): return f'<div class="columns {extra}"><div>{a}</div><div>{b}</div></div>'
def note(text): return '<p class="caption">'+text+'</p>'
def timer(minutes):
    return f'<div class="exercise-clock" data-duration="{minutes*60}"><span class="clock-readout">{minutes:02d}:00</span><div class="clock-actions"><button class="start-clock" type="button">{icon("play")}<span>Έναρξη</span></button><button class="reset-clock" type="button" aria-label="Επαναφορά χρονομέτρου">{icon("reset")}</button></div></div>'
def steps(items):
    return '<ol class="steps">'+''.join(f'<li><span class="step-number">{i:02d}</span><div>{text}</div></li>' for i,text in enumerate(items,1))+'</ol>'
def rows(items): return '<div class="editorial-rows">'+''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in items)+'</div>'

layouts=[]
def slide(content,theme='',classes=''): layouts.append((content,theme,classes))

slide(cols(
    label('Software Engineering MSc')+'<h1>AI στην<br>παραγωγή<br><em>λογισμικού.</em></h1><p class="cover-sub">Από το ticket έως το merge</p><p class="cover-meta">Java και CI<br>Διάλεξη και εργαστήριο 60 λεπτών</p>',
    '<div class="cover-flow">'+''.join(f'<div><span>{i:02d}</span><strong>{t}</strong></div>' for i,t in enumerate(['Ticket','Implementation','Evaluation','Review','Merge'],1))+'</div>'
),'dark','cover')

slide(label('Το πρόγραμμα')+title('Μία αλλαγή. Ολόκληρη η διαδικασία.')+
 '<div class="agenda">'+''.join(f'<div><span class="time-range">{t}</span><h3>{a}</h3><p>{b}</p></div>' for t,a,b in [
 ('0–15′','Απαίτηση','Ticket και context του agent'),('15–31′','Υλοποίηση','AI κώδικας και πραγματικό CI'),('31–45′','Αξιολόγηση','Έλεγχοι, μέτρηση και εξήγηση'),('45–60′','Merge','Review και αυτοματοποίηση')])+'</div>'+note('Το setup προηγείται του μαθήματος. Οι δραστηριότητες περιλαμβάνονται στα 60 λεπτά.'))

slide(label('Συζήτηση σε ζεύγη · 2 λεπτά')+title('Τι ακριβώς ζητά το ticket;')+
 '<blockquote>«10% έκπτωση για παραγγελίες<br>πάνω από 50 ευρώ»</blockquote>'+
 '<div class="question-row"><p>Το 50.00<br>περιλαμβάνεται;</p><p>Πότε<br>στρογγυλοποιούμε;</p><p>Υπάρχει<br>ανώτατη έκπτωση;</p></div>'+
 '<button class="reveal-button" data-reveal-target="contract-reveal">Αποκάλυψη συμβολαίου '+icon('right')+'</button>'+
 '<p id="contract-reveal" class="reveal-answer" hidden>Subtotal ≥ 50.00. HALF_UP στην έκπτωση πριν την αφαίρεση. Cap 20.00.</p>','green','discussion')

slide(label('Ticket PRICING-142')+title('Το συμβόλαιο αποδοχής')+cols(
 '<div class="formula"><span class="formula-label">Επιλεξιμότητα</span><strong>subtotal <span>≥</span> 50.00</strong><span class="formula-label">Έκπτωση</span><strong>min(10% × subtotal,<br><span>20.00</span>)</strong></div>',
 rows([('Η έκπτωση στρογγυλοποιείται πρώτη','HALF_UP σε δύο δεκαδικά. Έπειτα αφαιρείται.'),('Η είσοδος έχει σαφή όρια','0 έως 10000. Invalid subtotal προκαλεί IllegalArgumentException.'),('Το API παραμένει ίδιο','BigDecimal αποτέλεσμα με scale 2. Χωρίς νέες εξαρτήσεις.')])
)+note('Null ή άγνωστο coupon: καμία έκπτωση. strip() και αναγνώριση χωρίς διάκριση πεζών και κεφαλαίων.'))

slide(label('Συμφωνημένα expected results')+title('Τα παραδείγματα ορίζουν την αποδοχή')+
 '<table class="price-table"><colgroup><col style="width:16%"><col style="width:24%"><col style="width:21%"><col style="width:39%"></colgroup><thead><tr><th>Subtotal</th><th>Coupon</th><th>Τελικό ποσό</th><th>Τι ελέγχει</th></tr></thead><tbody>'+''.join(
 f'<tr class="{"focus-row" if x in ["50.00","50.05"] else ""}"><td>{x}</td><td>{c}</td><td class="answer-cell"><span hidden>{o}</span></td><td>{d}</td></tr>' for x,c,o,d in [
 ('49.99','STUDENT10','49.99','Κάτω από το όριο'),('50.00','STUDENT10','45.00','Συμπερίληψη ορίου'),('50.05','STUDENT10','45.04','Σειρά στρογγυλοποίησης'),('500.00','STUDENT10','480.00','Cap έκπτωσης'),('100.00','OTHER','100.00','Συμπεριφορά χωρίς έκπτωση')])+'</tbody></table>'+
 '<button class="reveal-button ink" id="show-prices">Αποκάλυψη τιμών '+icon('right')+'</button>','', 'table-slide')

slide(label('Context')+title('Ο agent χρειάζεται τρόπο να ελέγξει')+cols(
 '<div class="file-tree"><span>production-lab/</span><pre>ticket.md\nAGENTS.md\ndocs/feature-map.md\nsrc/main/.../PriceCalculator.java\nci/evaluate.py</pre></div>',
 rows([('Τι πρέπει να πετύχει','Απαιτήσεις, examples και δημόσιο API.'),('Πώς θα το επαληθεύσει','Feature map, ακριβείς εντολές και πραγματικά reports.'),('Πού επιτρέπεται να δράσει','Απομονωμένο workspace, επιτρεπόμενα paths και όρια.')])
)+note('Η Tan προτείνει κοινά verification tools και ενημερωμένο feature map για κάθε agent.'))

slide(label('Prompt κατανόησης')+title('Η επανεξήγηση προηγείται της αλλαγής')+
 '<blockquote class="prompt-quote english-prompt" lang="en">“Restate the acceptance contract.<br>Give expected outputs for 49.99, 50.00,<br>50.05, and 500.00.<br><em>Flag ambiguity before changing code.</em>”</blockquote>'+
 '<p class="bottom-statement language-choice">Αγγλικά για τις τεχνικές οδηγίες. Η ποιότητα επιβεβαιώνεται με evals.</p><p class="caption">Ίδιο σύντομο instruction: 37 EN / 64 EL tokens με o200k_base. Χωρίς context ή output.</p>','', 'quote-slide')

slide(label('Εργαστήριο 1')+cols(
 title('Το AI υλοποιεί.<br>Εσείς ανοίγετε το PR.')+steps(['Δώστε το ticket και το σχετικό context.','Αλλάξτε μόνο <code>PriceCalculator.java</code>.','Ανοίξτε PR προς το main του δικού σας fork.'])+note('Για checks που δεν εκτέλεσε, ο agent δηλώνει NOT RUN.'),
 timer(5)
),'green','exercise')

slide(label('Το αρχικό candidate')+title('Τα υπάρχοντα tests αφήνουν σφάλματα')+
 '<div class="metrics-pair"><div><span class="metric-label">Legacy tests</span><strong>3<span>/3</span></strong><p class="positive">PASS</p></div><div><span class="metric-label">Πλήρης evaluator</span><strong class="negative">5</strong><p class="negative">failures σε 27 tests</p></div></div>'+
 '<div class="terminal"><div class="terminal-title">Πραγματικό αποτέλεσμα του lab</div><pre><span class="positive">[PASS]</span> LegacyTest: 3 tests, 0 failures\n<span class="negative">[FAIL]</span> Full evaluator: 27 tests, 5 failures</pre></div>'+note('Ο starter είναι εσκεμμένα λανθασμένος για τη διδασκαλία. Τα στοιχεία προέρχονται από τοπική εκτέλεση.'))

slide(label('Counterexamples')+title('Δύο αποκλίσεις από το ίδιο ticket')+cols(
 '<div class="counter"><h3>Το όριο 50.00</h3><pre>subtotal.compareTo(\n    new BigDecimal(&quot;50&quot;)) &gt; 0</pre><div class="expected">Expected <strong>45.00</strong></div><div class="actual">Actual <strong>50.00</strong></div><p>Η ισότητα αποκλείστηκε.</p></div>',
 '<div class="counter rounding"><h3>Το subtotal 50.05</h3><div class="rounding-tabs"><button class="active" data-rounding="discount">Discount first</button><button data-rounding="payable">Payable first</button></div><div id="rounding-trace"><p>10% έκπτωση <strong>5.005</strong></p><p>HALF_UP έκπτωση <strong>5.01</strong></p><p>Τελικό ποσό <strong class="positive">45.04</strong></p></div></div>'
)+note('Το failure δίνει συγκεκριμένο παράδειγμα για τη διόρθωση. Τα expected values παραμένουν στο συμφωνημένο συμβόλαιο.'))

slide(label('Εργαστήριο 2')+cols(
 title('Το report<br>οδηγεί τη διόρθωση.')+steps(['Διαβάστε <code>result.json</code> και <code>build.log</code>.','Συνδέστε ένα failure με απαίτηση του ticket.','Δώστε το counterexample στο AI. Ζητήστε νέο fix.'])+note('Αν το candidate πέρασε, συγκρίνετε με το baseline report.'),
 timer(3)
),'green','exercise')

slide(label('Ανεξάρτητη αξιολόγηση')+title('Ο evaluator εξετάζει το τελικό artifact')+
 '<div class="pipeline simple">'+''.join(f'<div><span>{n:02d}</span><h3>{a}</h3><p>{b}</p></div>' for n,(a,b) in enumerate([
 ('Base commit','Tests και build configuration'),('Candidate','Μόνο η Java κλάση'),('Workspace','Νέα, επαναλήψιμη εκτέλεση'),('Report','Αποτέλεσμα και hashes')],1))+'</div>'+
 '<div class="wide-fact"><strong>500 inputs</strong><p>Oracle σε ακέραια cents μέσα σε ένα property test.</p></div>'+note('Το demo δεν είναι πλήρες sandbox. Σε παραγωγή ο grader και η αναφορά αποτελέσματος χρειάζονται προστατευμένη υποδομή.'))

slide(label('Αξιολόγηση του evaluator')+title('Θα απέρριπταν οι έλεγχοι ένα γνωστό λάθος;')+cols(
 '<div class="single-metric"><strong>5<span>/5</span></strong><p>επιλεγμένα σφάλματα<br>απορρίφθηκαν</p><small>Η λύση αναφοράς περνά 27/27.</small></div>',
 '<table class="fault-table"><tbody>'+''.join('<tr><td>'+a+'</td><td>'+icon('check')+' Απορρίφθηκε</td></tr>' for a in ['Exclusive threshold','Payable-first rounding','Missing discount cap','Missing normalization','Missing validation'])+'</tbody></table>'
)+note('100% detection σε αυτό το σύνολο. Δεν είναι PIT mutation score ή εκτίμηση της πιθανότητας άγνωστων bugs.'))

slide(label('Μέτρηση')+title('Ο χρόνος review είναι μέρος του κόστους')+
 rows([('Ανθρώπινος χρόνος','Ενεργός χρόνος review ανά αποδεκτό PR.'),('Επαναλήψεις','Πρώτη αποδοχή, rework και εγκαταλειμμένα tasks.'),('Ποιότητα','Confirmed defects σε σταθερό παράθυρο παρακολούθησης.'),('Συνολικό κόστος','Όλα τα attempts, CI και συντήρηση του pipeline.')])+note('Σύγκριση σε ίδιο task set και budget. Η μείωση του χρόνου review αξιολογείται μαζί με την ποιότητα.'),'','measurement')

slide(label('Εξήγηση με αρχές ASD-STE100')+title('Μια εξήγηση που ελέγχεται γρήγορα')+cols(
 '<div class="explanation-before"><span class="small-heading">Αόριστο</span><blockquote>«Robust handling όλων των pricing scenarios.»</blockquote></div>',
 '<div class="explanation-after"><span class="small-heading">Συγκεκριμένο</span><blockquote>«Στο 50.05 η έκπτωση γίνεται 5.01.<br>Η τελική τιμή είναι 45.04.»</blockquote></div>'
)+ '<p class="principles">Μία ιδέα ανά πρόταση. Σταθεροί όροι. Αριθμοί και προϋποθέσεις που διατηρούνται.</p>'+note('Το ASD-STE100 αφορά αγγλικά. Εδώ προσαρμόζουμε αρχές σαφήνειας στα ελληνικά. Η σαφήνεια χρειάζεται τεκμήρια.'))

slide(label('Περιγραφή PR από το AI')+title('Το PR συνοψίζει τα τελικά reports')+cols(
 '<div class="pr-example"><h3>PRICING-142: STUDENT10</h3><p>Εφαρμόζει το κουπόνι από 50.00. Στρογγυλοποιεί την έκπτωση πριν την αφαίρεση.</p><p><strong>Έλεγχοι:</strong> 27/27 PASS.<br><strong>Τεκμήρια:</strong> result.json, build.log.<br><strong>AI review:</strong> NOT RUN.</p><p><strong>Όριο:</strong> εξετάστηκε η Java μέθοδος.<br><strong>Revert:</strong> αναίρεση του commit.</p></div>',
 '<div class="pr-guidance"><p class="serif">Σύντομο.<br>Συγκεκριμένο.<br>Τεκμηριωμένο.</p><p>Τι αλλάζει και γιατί.<br>Τελικό run και tested SHA.<br>Ευρήματα, όρια και revert.</p></div>'
)+note('Ενδεικτικό PR μετά από successful evaluation. Στη ζωντανή διαδικασία προσθέτουμε το πραγματικό run URL και SHA.'),'','pr-slide')

slide(label('Εργαστήριο 3')+cols(
 title('Review<br>άλλης ομάδας.')+steps(['Ελέγξτε το τρέχον CI και το scope.','Διαβάστε την εξήγηση μαζί με τα evidence.','Δώστε APPROVE, REQUEST CHANGES ή WAIT.'])+note('Μία αιτιολόγηση με συγκεκριμένο στοιχείο. Αλλάξτε ρόλους.'),
 timer(3)
),'green','exercise')

slide(label('Instructor demo · 48–50′ · δωρεάν σε public repo')+title('Το AI review δίνει συγκεκριμένο εύρημα')+cols(
 '<div class="demo-context"><h3>Το PR αλλάζει τον υπολογισμό</h3><p>Named constants, με σκόπιμο rounding bug.</p><p class="serif">CodeRabbit review<br>+ πραγματικό CI</p></div>',
 rows([('Location και απαίτηση','Ποια γραμμή αλλάζει τη συμφωνημένη συμπεριφορά;'),('Counterexample','50.05 → expected 45.04, actual 45.05.'),('Επαλήθευση','Το finding ελέγχεται με το ticket και το report.')])
)+note('Δείχνουμε πραγματικό rehearsal review. Αν ο reviewer χάσει το bug, το δηλώνουμε. Το fixture δεν είναι AI output.'),'','demo-review')

slide(label('Instructor demo · 50–52′')+title('Finding → διόρθωση → νέο run → PR')+
 '<div class="automation-flow demo-flow">'+''.join(f'<div><span>{n:02d}</span><h3>{a}</h3><p>{b}</p></div>' for n,(a,b) in enumerate([
 ('Review','Επαληθευμένο finding'),('Repair','AI fix και δικό μας commit'),('CI','Φρέσκο run και tested SHA'),('AI PR','Σύντομη τελική περιγραφή')],1))+'</div>'+
 '<p class="principles">Ο άνθρωπος μεταφέρει το finding και κάνει push. Το PR review και τα tests εκτελούνται αυτόματα.</p>'+
note('Για τους χρόνους υπηρεσίας χρησιμοποιούμε πραγματικό αποθηκευμένο run. Το πλήρως αυτόνομο repair και το auto-merge είναι συνέχεια.'),'','demo-repair')

slide(label('Merge')+title('Συγχωνεύουμε την αξιολογημένη κατάσταση')+
 steps(['Required checks και ανεξάρτητο approval.','Νέο commit ή αλλαγή στο base απαιτεί επανέλεγχο.','Run URL, tested SHA και σαφής τρόπος revert.'])+
 '<div class="merge-command"><code>python ci/evaluate.py --candidate candidate --trusted policy</code><p>Ο ίδιος evaluator σε GitHub Actions και Jenkins.</p></div>'+note('Το merge ολοκληρώνει αυτή την αλλαγή. Deployment και monitoring έχουν ξεχωριστή διαδικασία.'))

slide(label('Lauren Tan / @poteto')+title('Οι πρακτικές που κρατάμε')+
 '<div class="takeaways">'+''.join(f'<div><span>{n:02d}</span><h3>{a}</h3><p>{b}</p></div>' for n,(a,b) in enumerate([
 ('Verification tools','Κάθε agent μπορεί να ασκήσει την πραγματική συμπεριφορά.'),('Hard constraints','Κανόνες μέσα στον κώδικα, στον compiler και στο CI.'),('Επιθεωρήσιμα artifacts','Evidence που διαβάζεται χωρίς replay όλου του run.'),('Συντήρηση του pipeline','Κάθε επαναλαμβανόμενο σφάλμα γίνεται μόνιμος έλεγχος.')],1))+'</div>'+note('Σύνθεση από πρωτογενή posts της Tan. Η εφαρμογή στη Java και στο lab είναι διδακτική πρόταση.'))

slide(label('Περαιτέρω αυτοματοποίηση')+title('Το lab μπορεί να γίνει συνεχής κύκλος')+
 '<div class="automation-flow">'+''.join(f'<div class="{"accent-stage" if n in [3,5] else ""}"><span>{n:02d}</span><h3>{a}</h3><p>{b}</p></div>' for n,(a,b) in enumerate([
 ('Ticket','Συμφωνημένα κριτήρια'),('Agent + CI','Κώδικας και tests'),('AI review','Συγκεκριμένα findings'),('Repair','Διόρθωση και νέο run'),('AI PR','Σύνοψη τελικών reports'),('Merge','Policy και monitoring')],1))+'</div>'+
 '<div class="loop-line"><svg viewBox="0 0 1360 95" preserveAspectRatio="none" aria-hidden="true"><path d="M795 3V60H335V3" fill="none" stroke="currentColor" stroke-width="2"/><path d="m325 15 10-12 10 12" fill="none" stroke="currentColor" stroke-width="2"/></svg><span>Εύρημα που χρειάζεται διόρθωση: νέο run</span></div>'+note('Το demo δείχνει PR review και CI. Η αυτόματη σύνδεση με repair και το auto-merge είναι συνέχεια.'))

slide(label('Αυτονομία με policy')+title('Η ανθρώπινη προσοχή εστιάζει στις εξαιρέσεις')+cols(
 '<div class="autonomy-routine"><span class="small-heading">Γνωστές κατηγορίες αλλαγών</span><h3>Σύντομος έλεγχος<br>των evidence.</h3><p>Σταδιακή εφαρμογή auto-merge όταν το ιστορικό και η policy το στηρίζουν.</p></div>',
 '<div class="autonomy-exception"><span class="small-heading">Έξω από την policy</span><h3>Στοχευμένο<br>ανθρώπινο review.</h3><p>Νέος κίνδυνος, ασάφεια, ανεπίλυτο finding ή ανεπαρκής αξιολόγηση.</p></div>'
)+note('Η Tan περιγράφει agents που κάνουν merge και δικό της review στο main αργότερα. Αυτό αφορά το δικό της περιβάλλον.'))

slide(label('Το τελικό takeaway')+'<h2 class="closing-title">Η βασική δουλειά<br>μεταφέρεται στο<br><em>αξιόπιστο pipeline.</em></h2>'+
 '<p class="closing-body">Ο engineer κατασκευάζει και συντηρεί το σύστημα που παράγει, ελέγχει και παραδίδει αποδεκτές αλλαγές.</p>'+
 '<div class="closing-bottom"><span>Tests</span><span>AI reviews</span><span>Σύντομα PRs</span><span>Μετρημένη ποιότητα</span></div>','dark','closing')

slide(label('Exit ticket · 2 λεπτά')+title('Τι θα αυτοματοποιούσατε στη συνέχεια;')+
 steps(['Ποιο failure mode θα κάνατε μόνιμο check;','Ποιο μέρος του review μπορεί να αναλάβει το pipeline;','Ποια μέτρηση θα δικαιολογούσε μεγαλύτερη αυτονομία;']),'green','exit-slide')

source_groups=[
 ('Loops You Can Trust','24 Ιουνίου 2026','https://x.com/poteto/status/2069824386283319343'),
 ('Organic architecture','18 Ιουλίου 2026','https://x.com/poteto/status/2078527882499150286'),
 ('Verification και feature maps','30 Ιουλίου 2026','https://x.com/poteto/status/2082874054483255805'),
 ('Agentic review και repair','8 Αυγούστου 2026','https://x.com/poteto/status/2085885450468909083'),
 ('Agents που κάνουν merge','11 Αυγούστου 2026','https://x.com/poteto/status/2087244771849089270'),
 ('Ο gardener του codebase','20 Αυγούστου 2026','https://x.com/poteto/status/2090546476464451907'),
 ('Constraints και engineering','5 Οκτωβρίου 2026','https://x.com/poteto/status/2106916667599278365')]
slide(label('Παράρτημα · πρωτογενείς πηγές')+title('Lauren Tan / @poteto')+
 '<div class="source-list">'+''.join(f'<a href="{u}" target="_blank" rel="noopener"><span><strong>{a}</strong><small>{b}</small></span>{icon("link")}</a>' for a,b,u in source_groups)+'</div>','', 'sources-slide')

tech=[('Agent evaluations','Anthropic','https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents'),('Σαφήνεια output και ASD-STE100','Karpathy','https://x.com/karpathy/status/2105819303471976479'),('Required checks και approvals','GitHub','https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches'),('Pipeline syntax','Jenkins','https://www.jenkins.io/doc/book/pipeline/syntax/'),('BigDecimal','Java 17','https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/math/BigDecimal.html'),('Mutation testing','PIT','https://pitest.org/quickstart/maven/'),('Coverage checks','JaCoCo','https://www.jacoco.org/jacoco/trunk/doc/check-mojo.html'),('Simplified Technical English','ASD-STE100','https://www.asd-ste100.org/')]
slide(label('Παράρτημα · τεχνική τεκμηρίωση')+title('Πηγές αξιολόγησης και εξήγησης')+
 '<div class="source-list">'+''.join(f'<a href="{u}" target="_blank" rel="noopener"><span><strong>{a}</strong><small>{b}</small></span>{icon("link")}</a>' for a,b,u in tech)+'</div>','', 'sources-slide')

slide(label('Παράρτημα · AI reviewer')+title('Ένα review με ελέγξιμα ευρήματα')+
 '<div class="review-prompt" lang="en"><p>Read the ticket, final diff, and actual CI reports in a fresh context.</p><p>For each material finding: code location, violated requirement, specific counterexample, and evidence.</p><p>Label unverified hypotheses. Check evaluation gaps and whether the PR description matches the final reports.</p></div>'+note('Νέο context βοηθά τη χωριστή εξέταση. Η ορθότητα του reviewer χρειάζεται δικά της evals και ανθρώπινα ελεγμένα παραδείγματα.'))

assert len(layouts)==len(data)==28

def source_label(url):
    if 'coderabbit' in url: return 'CodeRabbit'
    if '/poteto/' in url: return 'Lauren Tan / @poteto'
    if '/karpathy/' in url: return 'Andrej Karpathy'
    if 'anthropic' in url:return 'Anthropic'
    if 'help.openai.com' in url:return 'OpenAI token counting'
    if 'aclanthology.org' in url:return 'Multilingual prompting research'
    if 'github.com/cursor' in url:return 'pstack'
    if 'docs.github' in url:return 'GitHub Docs'
    if 'oracle' in url:return 'Java documentation'
    if 'jenkins' in url:return 'Jenkins documentation'
    if 'pitest' in url:return 'PIT'
    if 'jacoco' in url:return 'JaCoCo'
    return 'ASD-STE100'

slides=[]
for i,((content,theme,classes),d) in enumerate(zip(layouts,data),1):
    citations=''
    if d['sources'] and i not in [24,25]:
        unique=[]
        for u in d['sources']:
            name=source_label(u)
            if name not in [n for n,v in unique]: unique.append((name,u))
        citations='<div class="slide-sources">'+''.join(f'<a href="{u}" target="_blank" rel="noopener">{H(n)}</a>' for n,u in unique[:2])+'</div>'
    slides.append(f'<section class="slide {theme} {classes}" data-index="{i-1}" data-title="{H(d["title"])}" aria-label="Διαφάνεια {i}: {H(d["title"])}" {"hidden" if i>1 else ""}><div class="slide-content">{content}</div>{citations}<footer class="slide-footer"><span>AI στην παραγωγή λογισμικού</span><span>{"Παράρτημα" if not d["minutes"] else "Java / CI"}</span><span>{i:02d} / {len(data)}</span></footer></section>')

font_css=[]
fonts=json.loads((BUILD/'fonts.json').read_text())
for f in fonts:
    encoded=base64.b64encode((BUILD/f['file']).read_bytes()).decode()
    font_css.append(f"@font-face{{font-family:'{f['family']}';font-style:{f['style']};font-weight:{f['weight']};font-display:block;src:url(data:font/ttf;base64,{encoded}) format('truetype');}}")

css=r'''
:root{--paper:#f6f4ed;--ink:#1d302b;--green:#225f4d;--mint:#c4dccd;--line:#d9ddd2;--muted:#66756d;--orange:#bf5736;--stage-width:1600px;--stage-height:900px}
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden}body{font-family:'Noto Sans',Arial,sans-serif;background:#172720;color:var(--ink);font-synthesis:none}button,a{-webkit-tap-highlight-color:transparent}button{font:inherit;cursor:pointer}button:focus-visible,a:focus-visible{outline:3px solid #d57b50;outline-offset:5px}a{color:inherit}button svg{flex-shrink:0}[hidden]{display:none!important}
.viewport{position:absolute;inset:0 0 58px;display:flex;align-items:center;justify-content:center;overflow:hidden}.stage{position:relative;width:1600px;height:900px;flex-shrink:0;transform-origin:center center;box-shadow:0 14px 65px #0005}.slide{position:absolute;inset:0;background:var(--paper);overflow:hidden}.slide-content{position:relative;height:100%;padding:68px 100px 118px}.label{margin:0 0 24px;text-transform:uppercase;letter-spacing:.11em;font-size:17px;font-weight:600;color:var(--green)}h1,h2,h3,p,blockquote{margin:0}h2{font-size:56px;line-height:1.23;letter-spacing:-.034em;font-weight:600;max-width:1370px;margin-bottom:50px}h3{font-size:28px;font-weight:600;line-height:1.38}p{font-size:27px;line-height:1.58}em,.serif{font-family:'Noto Serif',Georgia,serif;font-weight:400}.caption{position:absolute;left:100px;right:100px;bottom:104px;font-size:19px;line-height:1.55;color:var(--muted);max-width:1370px}.columns{display:grid;grid-template-columns:1fr 1fr;column-gap:85px;align-items:start}.columns>div{min-width:0}.slide-footer{position:absolute;left:100px;right:100px;bottom:37px;padding-top:16px;border-top:1px solid var(--line);display:flex;justify-content:space-between;font-size:14px;letter-spacing:.025em;color:var(--muted)}.slide-sources{position:absolute;bottom:75px;left:100px;display:flex;gap:24px;font-size:13px;color:var(--muted)}.slide-sources a{text-decoration:none;border-bottom:1px solid currentColor}.dark{background:var(--ink);color:var(--paper)}.dark .label,.dark .caption{color:var(--mint)}.dark .slide-footer{border-color:#547165;color:#c0cec5}.dark .slide-sources{color:#b4c7b9}.green{background:var(--green);color:var(--paper)}.green .label{color:#c4d9cb}.green .caption{color:#d3e1d6}.green .slide-footer{border-color:#659580;color:#d3e1d6}.green .slide-sources{color:#cfdfd3}
.cover .columns{grid-template-columns:1.7fr 1fr;gap:105px;align-items:center;height:100%}.cover h1{font-size:92px;line-height:1.08;letter-spacing:-.035em;margin-top:50px}.cover h1 em{color:var(--mint)}.cover-sub{font-size:31px;margin-top:32px}.cover-meta{font-size:18px;color:#bfd0c3;margin-top:29px;line-height:1.65}.cover-flow{padding-top:58px}.cover-flow>div{display:flex;align-items:center;gap:27px;padding:22px 0;border-bottom:1px solid #547165}.cover-flow>div:first-child{border-top:1px solid #547165}.cover-flow span{font-size:16px;color:var(--mint)}.cover-flow strong{font-weight:400;font-size:34px}.agenda{display:grid;grid-template-columns:repeat(4,1fr);gap:36px;margin-top:104px}.agenda>div{border-top:2px solid var(--green);padding-top:24px}.time-range{font-size:25px;color:var(--green)}.agenda h3{font-size:33px;margin:49px 0 18px}.agenda p{font-size:24px;max-width:270px}.discussion h2{margin-bottom:39px}.discussion blockquote{font-size:46px;font-weight:500;line-height:1.5;letter-spacing:-.015em}.question-row{display:grid;grid-template-columns:repeat(3,1fr);gap:30px;margin-top:60px;padding-top:25px;border-top:1px solid #679785}.question-row p{font-size:28px;line-height:1.4}.reveal-button{position:absolute;bottom:147px;left:100px;display:inline-flex;align-items:center;gap:12px;color:var(--paper);border:1px solid #a6c5b3;border-radius:3px;padding:12px 18px;background:transparent;font-size:18px}.reveal-button.ink{color:var(--green);border-color:var(--green);bottom:130px}.reveal-answer{position:absolute;bottom:142px;left:560px;right:100px;font-size:20px;line-height:1.5;color:#e1ece4}.formula{margin-top:12px}.formula-label{display:block;font-size:18px;color:var(--muted);margin:0 0 18px}.formula strong{display:block;font-weight:500;font-size:45px;margin-bottom:60px;letter-spacing:-.035em}.formula strong span{color:var(--green)}.editorial-rows>div{padding:0 0 25px;margin:0 0 24px;border-bottom:1px solid var(--line)}.editorial-rows h3{margin-bottom:10px}.editorial-rows p{font-size:23px;color:var(--muted);line-height:1.55}.price-table{border-collapse:collapse;table-layout:fixed;width:100%;font-size:29px}.price-table th{text-align:left;font-size:16px;font-weight:500;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;padding:0 15px 20px;border-bottom:2px solid var(--ink)}.price-table td{padding:20px 15px;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}.price-table td:nth-child(2){font-size:21px}.price-table td:last-child{font-size:23px;color:var(--muted)}.price-table th:first-child,.price-table td:first-child{padding-left:0}.price-table .focus-row td:first-child,.price-table .focus-row td:nth-child(3){color:var(--green);font-weight:600}.answer-cell{width:220px}.answer-cell>span[hidden]{display:inline-block!important;visibility:hidden}.price-table.answers .answer-cell>span{visibility:visible}.file-tree{border-top:2px solid var(--green);padding-top:24px}.file-tree>span{font-size:22px;color:var(--green)}pre,code{font-family:Consolas,'Noto Sans',monospace}.file-tree pre{font-size:25px;line-height:2.5;color:var(--ink);margin-top:23px}.prompt-quote{font-size:48px;line-height:1.65;letter-spacing:-.02em;margin-top:44px}.prompt-quote em{color:var(--green)}.english-prompt{font-size:42px;line-height:1.55}.language-choice{font-size:24px!important;margin-top:32px!important}.bottom-statement{margin-top:70px;font-size:26px;color:var(--muted)}.exercise .columns{grid-template-columns:1.65fr 1fr;gap:80px;align-items:center;height:650px}.exercise h2{font-size:65px;margin-bottom:45px;line-height:1.2}.steps{list-style:none;padding:0;margin:0}.steps li{display:flex;gap:24px;align-items:flex-start;padding:22px 0;border-bottom:1px solid var(--line);font-size:29px;line-height:1.55}.step-number{font-size:18px;flex-shrink:0;line-height:2.5;color:var(--green);width:30px}.steps code{font-size:24px}.green .steps li{border-color:#5c8f78;font-size:26px;padding:19px 0}.green .step-number{color:#c1d7c8}.exercise-clock{align-self:center;text-align:center}.clock-readout{font-size:111px;line-height:1.3;font-weight:400;letter-spacing:-.065em;font-variant-numeric:tabular-nums}.clock-actions{display:flex;justify-content:center;gap:12px;margin-top:30px}.clock-actions button{background:transparent;border:1px solid #97b8a3;border-radius:3px;padding:13px 18px;display:flex;align-items:center;gap:10px;color:var(--paper);font-size:18px}.clock-actions .reset-clock{padding:13px}.exercise .caption{font-size:18px}.metrics-pair{display:grid;grid-template-columns:1fr 1fr;margin-top:10px}.metrics-pair>div:last-child{border-left:1px solid var(--line);padding-left:80px}.metric-label{font-size:24px;color:var(--muted)}.metrics-pair strong{display:block;font-size:120px;letter-spacing:-.07em;line-height:1.35;font-weight:500}.metrics-pair strong span{font-size:70px;color:#819085}.metrics-pair p{font-size:26px}.positive{color:var(--green)}.negative{color:var(--orange)}.terminal{margin-top:38px;border-top:1px solid var(--line);padding-top:18px}.terminal-title{font-size:16px;color:var(--muted);margin-bottom:17px}.terminal pre{font-size:25px;line-height:1.7;margin:0}.counter{padding-top:18px;border-top:2px solid var(--green)}.counter h3{font-size:32px;margin-bottom:35px}.counter pre{font-size:24px;line-height:1.4;padding:20px 0;margin:0 0 31px}.expected,.actual{display:flex;justify-content:space-between;font-size:25px;align-items:baseline;padding:16px 0;border-bottom:1px solid var(--line)}.expected strong,.actual strong{font-size:41px;font-weight:500}.actual strong{color:var(--orange)}.counter>p{font-size:23px;color:var(--muted);margin-top:25px}.rounding-tabs{display:flex;gap:16px;margin-bottom:46px}.rounding-tabs button{padding:8px 0;border:0;border-bottom:2px solid transparent;background:none;font-size:19px;color:var(--muted)}.rounding-tabs button.active{border-color:var(--green);color:var(--green)}#rounding-trace p{display:flex;justify-content:space-between;padding:17px 0;border-bottom:1px solid var(--line);font-size:25px}#rounding-trace strong{font-size:35px;font-weight:500}.pipeline{display:grid;grid-template-columns:repeat(4,1fr);gap:34px;margin-top:80px}.pipeline>div{border-top:2px solid var(--green);padding-top:17px}.pipeline span{font-size:17px;color:var(--green)}.pipeline h3{margin:34px 0 20px;font-size:31px}.pipeline p{font-size:23px;color:var(--muted)}.wide-fact{display:flex;gap:54px;align-items:center;border-top:1px solid var(--line);margin-top:66px;padding-top:28px}.wide-fact strong{font-size:41px;font-weight:500;color:var(--green)}.wide-fact p{font-size:24px}.single-metric strong{display:block;font-size:160px;font-weight:400;line-height:1.3;letter-spacing:-.08em;color:var(--green)}.single-metric strong span{font-size:90px;color:#87948a}.single-metric p{font-size:32px;line-height:1.45}.single-metric small{display:block;font-size:20px;margin-top:35px;color:var(--muted)}.fault-table{width:100%;border-collapse:collapse;font-size:23px;margin-top:20px}.fault-table td{border-bottom:1px solid var(--line);padding:22px 0}.fault-table td:last-child{color:var(--green);white-space:nowrap;text-align:right;font-size:20px}.fault-table svg{vertical-align:middle;margin-right:8px;width:18px}.measurement .editorial-rows{margin-top:22px}.measurement .editorial-rows>div{display:grid;grid-template-columns:350px 1fr;padding-bottom:22px;margin-bottom:22px}.measurement .editorial-rows h3{font-size:30px}.measurement .editorial-rows p{font-size:28px;color:var(--ink)}.small-heading{display:block;font-size:18px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:40px}.explanation-before,.explanation-after{border-top:2px solid var(--line);padding-top:22px}.explanation-before .small-heading{color:var(--orange)}.explanation-after .small-heading{color:var(--green)}.explanation-before blockquote{font-size:39px;line-height:1.5;color:var(--muted)}.explanation-after blockquote{font-size:39px;line-height:1.5}.principles{border-top:1px solid var(--line);padding-top:27px;margin-top:54px;font-size:23px}.pr-example{border-top:2px solid var(--green);padding-top:25px}.pr-example h3{font-size:31px;margin-bottom:26px}.pr-example p{font-size:24px;line-height:1.65;margin:0 0 21px}.pr-guidance{padding:19px 0 0 40px}.pr-guidance .serif{font-size:48px;line-height:1.4;margin-bottom:36px}.pr-guidance>p:last-child{font-size:24px;line-height:1.9;color:var(--muted)}.merge-command{border-top:1px solid var(--line);padding-top:25px;margin-top:43px}.merge-command code{font-size:25px}.merge-command p{font-size:22px;color:var(--muted);margin-top:16px}.takeaways{display:grid;grid-template-columns:1fr 1fr;column-gap:90px;row-gap:46px;margin-top:20px}.takeaways>div{border-top:1px solid var(--line);padding-top:20px}.takeaways span{font-size:16px;color:var(--green)}.takeaways h3{font-size:32px;margin-top:19px;margin-bottom:14px}.takeaways p{font-size:25px;color:var(--muted);max-width:560px}.demo-flow{grid-template-columns:repeat(4,1fr)!important;gap:30px!important}.demo-context p{font-size:32px;line-height:1.55}.demo-context .serif{font-size:45px;margin-top:42px}.automation-flow{display:grid;grid-template-columns:repeat(6,1fr);gap:22px;margin-top:105px}.automation-flow>div{border-top:2px solid var(--ink);padding-top:20px;position:relative}.automation-flow>div:not(:last-child)::after{content:'';position:absolute;top:36px;right:-18px;width:10px;height:10px;border-top:1.5px solid var(--muted);border-right:1.5px solid var(--muted);transform:rotate(45deg)}.automation-flow span{font-size:17px;color:var(--muted)}.automation-flow h3{font-size:29px;margin-top:39px;margin-bottom:17px}.automation-flow p{font-size:23px;color:var(--muted)}.automation-flow .accent-stage{border-color:var(--green)}.automation-flow .accent-stage h3{color:var(--green)}.loop-line{position:relative;margin-top:36px;height:120px;color:var(--green)}.loop-line svg{width:100%;height:95px}.loop-line span{position:absolute;top:82px;left:0;right:0;text-align:center;font-size:20px}.autonomy-routine,.autonomy-exception{padding-top:26px;border-top:2px solid var(--green)}.autonomy-exception{border-color:var(--orange)}.autonomy-routine h3,.autonomy-exception h3{font-size:45px;margin-bottom:35px;line-height:1.35}.autonomy-routine>p,.autonomy-exception>p{font-size:26px;color:var(--muted)}.autonomy-exception .small-heading{color:var(--orange)}.closing-title{font-size:85px;line-height:1.16;margin-top:45px;margin-bottom:44px;max-width:1390px;font-weight:500}.closing-title em{color:var(--mint)}.closing-body{font-size:28px;max-width:1040px;color:#d0ddd3}.closing-bottom{display:flex;gap:55px;margin-top:50px;padding-top:22px;border-top:1px solid #5d7767;font-size:19px;color:#c4d9c9}.exit-slide h2{margin-bottom:76px}.exit-slide .steps li{font-size:37px;padding:30px 0}.exit-slide .step-number{font-size:20px;line-height:2.8}.source-list{margin-top:-8px;display:grid;grid-template-columns:1fr 1fr;column-gap:75px;row-gap:18px}.source-list a{display:flex;justify-content:space-between;align-items:center;gap:18px;border-bottom:1px solid var(--line);padding:20px 0 24px;text-decoration:none}.source-list strong{font-size:25px;font-weight:500;display:block}.source-list small{display:block;font-size:18px;color:var(--muted);margin-top:12px}.source-list svg{flex-shrink:0;width:22px;color:var(--green)}.review-prompt{border-top:2px solid var(--green);padding-top:28px;max-width:1280px}.review-prompt p{font-size:33px;line-height:1.65;margin-bottom:32px}
.controls{position:fixed;bottom:0;left:0;right:0;height:58px;display:flex;align-items:center;justify-content:space-between;padding:0 23px;background:#122119;color:#dce5dc;border-top:1px solid #405647;z-index:20}.controls-group{display:flex;align-items:center;gap:8px}.control{display:flex;align-items:center;justify-content:center;width:38px;height:36px;background:none;border:0;border-radius:4px;color:inherit}.control:hover{background:#304d3c}.counter-label{font-size:12px;min-width:68px;text-align:center;font-variant-numeric:tabular-nums}.current-title{font-size:12px;max-width:42vw;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#b9cebd}.progress{position:fixed;bottom:58px;left:0;height:2px;background:#7fae94;transition:width .15s;z-index:20}.overlay{position:fixed;inset:0;background:#112017ed;z-index:30;color:var(--paper);overflow:auto;padding:50px 7vw}.overlay header{display:flex;align-items:center;justify-content:space-between;margin-bottom:38px}.overlay h2{font-size:32px;margin:0}.overview-list{display:grid;grid-template-columns:1fr 1fr;gap:0 45px}.overview-item{display:flex;gap:20px;align-items:center;padding:17px 0;border:0;border-bottom:1px solid #3d5b49;color:var(--paper);background:none;text-align:left;font-size:17px}.overview-item span:first-child{color:#a6c5b2;font-size:13px;width:24px}.notes-overlay{padding:36px max(35px,12vw)}.notes-overlay h3{font-size:23px;margin:30px 0 17px}.notes-overlay p{font-size:20px;line-height:1.8;max-width:1050px;white-space:pre-line}.notes-overlay a{display:block;color:#c4dfcd;font-size:15px;margin-top:14px;overflow-wrap:anywhere}.notes-timing{font-size:15px!important;color:#a6c5b2}.help-grid{display:grid;grid-template-columns:1fr 1fr;gap:25px}.help-grid p{font-size:20px}kbd{display:inline-block;background:#2e4939;padding:4px 10px;border-radius:3px;font-family:inherit;font-size:16px;margin-right:7px}.help-note{font-size:17px;margin-top:40px;color:#b6ccb9}.font-license{font-size:12px!important;white-space:pre-wrap!important;opacity:.7}
@media(max-width:650px){.current-title{display:none}.controls{padding:0 8px}.overview-list{grid-template-columns:1fr}.overlay{padding:30px 22px}.notes-overlay p{font-size:17px}.help-grid{grid-template-columns:1fr}.control{width:33px}.overlay h2{font-size:26px}}
@media print{@page{size:1600px 900px;margin:0}html,body{width:1600px;height:auto;overflow:visible;background:var(--paper);print-color-adjust:exact;-webkit-print-color-adjust:exact}.viewport{position:static;display:block;overflow:visible}.stage{transform:none!important;box-shadow:none;width:1600px;height:auto}.slide,.slide[hidden]{display:block!important;position:relative;width:1600px;height:900px;break-after:page;page-break-after:always}.slide:last-child{break-after:auto}.controls,.progress,.overlay,.clock-actions,.reveal-button,.rounding-tabs{display:none!important}.answer-cell>span[hidden]{visibility:visible}.reveal-answer[hidden]{display:block!important;left:100px;bottom:142px}.rounding #rounding-trace{margin-top:65px}.slide a{text-decoration:none}.slide-content{height:900px}}
'''

script=r'''
const slides=[...document.querySelectorAll('.slide')];let index=0;let focusBeforeOverlay=null;
const stage=document.querySelector('.stage'),viewport=document.querySelector('.viewport');
function fit(){const scale=Math.min(viewport.clientWidth/1600,viewport.clientHeight/900);stage.style.transform=`scale(${scale})`;}
function go(n,updateHash=true){index=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>s.hidden=i!==index);document.getElementById('counter').textContent=`${String(index+1).padStart(2,'0')} / ${slides.length}`;document.getElementById('current-title').textContent=slides[index].dataset.title;document.getElementById('progress').style.width=((index+1)/slides.length*100)+'%';document.getElementById('prev').disabled=index===0;document.getElementById('next').disabled=index===slides.length-1;if(updateHash)history.replaceState(null,'',`#slide-${index+1}`);renderNotes();}
function openOverlay(id){focusBeforeOverlay=document.activeElement;document.getElementById(id).hidden=false;document.getElementById(id).querySelector('button').focus();}
function closeOverlays(){document.querySelectorAll('.overlay').forEach(e=>e.hidden=true);if(focusBeforeOverlay?.isConnected)focusBeforeOverlay.focus();}
function renderNotes(){const d=DECK_DATA[index];document.getElementById('notes-title').textContent=`${index+1}. ${d.title}`;const elapsed=DECK_DATA.slice(0,index).reduce((a,s)=>a+s.minutes,0);document.getElementById('notes-timing').textContent=d.minutes?`${elapsed}–${elapsed+d.minutes} λεπτά, μαζί με τη δραστηριότητα`:'Παράρτημα εκτός του προγράμματος των 60 λεπτών';document.getElementById('notes-body').textContent=d.notes;document.getElementById('notes-source-heading').hidden=!d.sources.length;document.getElementById('notes-sources').replaceChildren(...d.sources.map((url,i)=>{const a=document.createElement('a');a.href=url;a.target='_blank';a.rel='noopener';a.textContent=url;return a;}));}
document.getElementById('prev').onclick=()=>go(index-1);document.getElementById('next').onclick=()=>go(index+1);
document.getElementById('fullscreen').onclick=async()=>{try{if(!document.fullscreenElement)await document.documentElement.requestFullscreen();else await document.exitFullscreen();}catch{}};
document.getElementById('notes').onclick=()=>openOverlay('notes-overlay');document.getElementById('overview').onclick=()=>openOverlay('overview-overlay');document.getElementById('help').onclick=()=>openOverlay('help-overlay');document.getElementById('print').onclick=()=>window.print();
document.querySelectorAll('[data-close]').forEach(b=>b.onclick=closeOverlays);
document.getElementById('overview-list').replaceChildren(...DECK_DATA.map((d,i)=>{const b=document.createElement('button');b.className='overview-item';b.innerHTML=`<span>${String(i+1).padStart(2,'0')}</span><span></span>`;b.lastElementChild.textContent=d.title;b.onclick=()=>{go(i);closeOverlays();};return b;}));
document.addEventListener('keydown',e=>{if(e.ctrlKey||e.metaKey||e.altKey||e.target.closest('input,textarea,select'))return;const overlay=[...document.querySelectorAll('.overlay')].find(o=>!o.hidden);if(overlay){if(e.key==='Escape'){e.preventDefault();closeOverlays();}else if(e.key==='Tab'){const els=[...overlay.querySelectorAll('button,a[href]')];const first=els[0],last=els[els.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}return;}if((e.key===' '||e.key==='Enter')&&e.target.closest('button,a'))return;const key=['KeyN','KeyO','KeyF'].includes(e.code)?e.code.slice(3).toLowerCase():e.key;switch(key){case 'ArrowRight':case 'ArrowDown':case 'PageDown':case ' ':e.preventDefault();go(index+1);break;case 'ArrowLeft':case 'ArrowUp':case 'PageUp':e.preventDefault();go(index-1);break;case 'Home':go(0);break;case 'End':go(slides.length-1);break;case 'n':case 'N':openOverlay('notes-overlay');break;case 'o':case 'O':openOverlay('overview-overlay');break;case 'f':case 'F':document.getElementById('fullscreen').click();break;case '?':openOverlay('help-overlay');break;}});
document.querySelectorAll('[data-reveal-target]').forEach(b=>{b.onclick=()=>{const e=document.getElementById(b.dataset.revealTarget);e.hidden=!e.hidden;b.setAttribute('aria-expanded',String(!e.hidden));};b.setAttribute('aria-expanded','false');});
document.getElementById('show-prices').onclick=()=>{const t=document.querySelector('.price-table');const yes=t.classList.toggle('answers');document.querySelectorAll('.answer-cell span').forEach(s=>s.hidden=!yes);document.getElementById('show-prices').setAttribute('aria-expanded',String(yes));};
document.querySelectorAll('[data-rounding]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-rounding]').forEach(x=>x.classList.toggle('active',x===b));document.getElementById('rounding-trace').innerHTML=b.dataset.rounding==='discount'?'<p>10% έκπτωση <strong>5.005</strong></p><p>HALF_UP έκπτωση <strong>5.01</strong></p><p>Τελικό ποσό <strong class="positive">45.04</strong></p>':'<p>Ακριβές payable <strong>45.045</strong></p><p>HALF_UP payable <strong>45.05</strong></p><p>Απόκλιση από ticket <strong class="negative">+0.01</strong></p>';});
document.querySelectorAll('.exercise-clock').forEach(clock=>{let remaining=Number(clock.dataset.duration),running=false,last=0;const readout=clock.querySelector('.clock-readout'),start=clock.querySelector('.start-clock');const paint=()=>{readout.textContent=`${String(Math.floor(remaining/60)).padStart(2,'0')}:${String(remaining%60).padStart(2,'0')}`;start.querySelector('span').textContent=running?'Παύση':remaining===0?'Ξανά':'Έναρξη';};start.onclick=()=>{if(!remaining)remaining=Number(clock.dataset.duration);running=!running;last=Date.now();paint();};clock.querySelector('.reset-clock').onclick=()=>{running=false;remaining=Number(clock.dataset.duration);paint();};setInterval(()=>{if(!running)return;const elapsed=Math.floor((Date.now()-last)/1000);if(!elapsed)return;remaining=Math.max(0,remaining-elapsed);last+=elapsed*1000;if(!remaining)running=false;paint();},200);});
window.addEventListener('resize',fit);window.addEventListener('hashchange',()=>{const n=Number(location.hash.replace('#slide-',''));if(n)go(n-1,false);});window.addEventListener('beforeprint',()=>{document.querySelector('[data-rounding="discount"]').click();});document.fonts.ready.then(fit);fit();go(Math.max(0,Number(location.hash.replace('#slide-',''))-1),false);
'''

note_overlay='<aside class="overlay notes-overlay" id="notes-overlay" role="dialog" aria-modal="true" aria-labelledby="notes-title" hidden><header><h2 id="notes-title"></h2><button class="control" data-close aria-label="Κλείσιμο σημειώσεων">'+icon('close')+'</button></header><p class="notes-timing" id="notes-timing"></p><p id="notes-body"></p><h3 id="notes-source-heading">Πηγές</h3><div id="notes-sources"></div></aside>'
overview='<aside class="overlay" id="overview-overlay" role="dialog" aria-modal="true" aria-labelledby="overview-title" hidden><header><h2 id="overview-title">Όλες οι διαφάνειες</h2><button class="control" data-close aria-label="Κλείσιμο επισκόπησης">'+icon('close')+'</button></header><div class="overview-list" id="overview-list"></div></aside>'
licenses='\n\n'.join((BUILD/(f+'-OFL.txt')).read_text() for f in ['notosans','notoserif'])
help_overlay='<aside class="overlay" id="help-overlay" role="dialog" aria-modal="true" aria-labelledby="help-title" hidden><header><h2 id="help-title">Χειρισμός παρουσίασης</h2><button class="control" data-close aria-label="Κλείσιμο βοήθειας">'+icon('close')+'</button></header><div class="help-grid"><p><kbd>←</kbd><kbd>→</kbd> Προηγούμενη / επόμενη</p><p><kbd>Space</kbd> Επόμενη διαφάνεια</p><p><kbd>F</kbd> Fullscreen</p><p><kbd>N</kbd> Σημειώσεις ομιλητή</p><p><kbd>O</kbd> Επισκόπηση διαφανειών</p><p><kbd>Esc</kbd> Κλείσιμο παραθύρου</p></div><p class="help-note">Τα χρονόμετρα ξεκινούν μόνο όταν τα ενεργοποιήσετε. Οι απαντήσεις αποκαλύπτονται με το σχετικό κουμπί. Η εκτύπωση περιλαμβάνει όλες τις διαφάνειες και τις απαντήσεις.</p><p class="help-note">Οι Noto Sans και Noto Serif είναι ενσωματωμένες στο αρχείο και υποστηρίζουν ελληνικά. Η παρουσίαση λειτουργεί χωρίς σύνδεση στο internet. Οι σύνδεσμοι πηγών χρειάζονται internet.</p><details><summary class="help-note">Άδειες γραμματοσειρών</summary><pre class="font-license">'+H(licenses)+'</pre></details></aside>'
buttons=[('overview','grid','Επισκόπηση (O)'),('notes','notes','Σημειώσεις (N)'),('print','print','Εκτύπωση όλων των διαφανειών'),('fullscreen','expand','Fullscreen (F)'),('help','info','Βοήθεια (?)')]
controls='<nav class="controls" aria-label="Χειρισμός παρουσίασης"><div class="controls-group"><button id="prev" class="control" title="Προηγούμενη" aria-label="Προηγούμενη διαφάνεια">'+icon('left')+'</button><span id="counter" class="counter-label" aria-live="polite"></span><button id="next" class="control" title="Επόμενη" aria-label="Επόμενη διαφάνεια">'+icon('right')+'</button></div><span class="current-title" id="current-title"></span><div class="controls-group">'+''.join(f'<button id="{id}" class="control" title="{name}" aria-label="{name}">{icon(ic)}</button>' for id,ic,name in buttons)+'</div></nav><div class="progress" id="progress"></div>'
encoded_data=json.dumps(data,ensure_ascii=False).replace('</',r'<\/')
page='<!DOCTYPE html>\n<html lang="el"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Διάλεξη 60 λεπτών και εργαστήριο Java για την αξιολόγηση AI κώδικα από το ticket έως το merge."><title>AI στην παραγωγή λογισμικού</title><style>'+''.join(font_css)+css+'</style></head><body><main class="viewport"><div class="stage">'+''.join(slides)+'</div></main>'+controls+note_overlay+overview+help_overlay+'<script>const DECK_DATA='+encoded_data+';\n'+script+'</script></body></html>'
(OUT/'ai-production-lecture-el.html').write_text(page,encoding='utf-8')

# Inspect TrueType cmap tables directly, avoiding a runtime dependency.
def font_codepoints(path):
    b=path.read_bytes();n=struct.unpack_from('>H',b,4)[0];tables={}
    for j in range(n):
        tag,checksum,off,length=struct.unpack_from('>4sIII',b,12+16*j);tables[tag]=off
    cmap=tables[b'cmap'];subs=struct.unpack_from('>H',b,cmap+2)[0];chars=set()
    for j in range(subs):
        platform,enc,offset=struct.unpack_from('>HHI',b,cmap+4+8*j)
        if platform not in [0,3]:continue
        o=cmap+offset;fmt=struct.unpack_from('>H',b,o)[0]
        if fmt==12:
            groups=struct.unpack_from('>I',b,o+12)[0]
            for k in range(groups):
                start,end,glyph=struct.unpack_from('>III',b,o+16+12*k)
                chars.update(range(start,end+1))
        if fmt==4:
            seg=struct.unpack_from('>H',b,o+6)[0]//2
            ends=struct.unpack_from('>'+str(seg)+'H',b,o+14)
            starts=struct.unpack_from('>'+str(seg)+'H',b,o+16+2*seg)
            delta=struct.unpack_from('>'+str(seg)+'h',b,o+16+4*seg)
            roffset=struct.unpack_from('>'+str(seg)+'H',b,o+16+6*seg)
            for k,(start,end) in enumerate(zip(starts,ends)):
                for c in range(start,min(end,65534)+1):
                    if not roffset[k]:gid=(c+delta[k])%65536
                    else:
                        ptr=o+16+6*seg+2*k+roffset[k]+2*(c-start)
                        gid=struct.unpack_from('>H',b,ptr)[0]
                        if gid:gid=(gid+delta[k])%65536
                    if gid:chars.add(c)
    return chars
greek={ord(c) for c in page if 0x370<=ord(c)<=0x3ff or 0x1f00<=ord(c)<=0x1fff}
for font in fonts:
    missing=greek-font_codepoints(BUILD/font['file'])
    assert not missing,(font['file'],missing)
    print(font['family'],font['style'],font['weight'],'supports all',len(greek),'Greek characters used.')
print('Created standalone HTML:',len(page.encode('utf-8')),'bytes;',len(data),'slides')
