from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent.parent
html=(ROOT/'outputs/ai-production-lecture-el.html').read_text(encoding='utf-8')
fontcss=''.join(re.findall(r'@font-face\{.*?\}',html,re.S))
style='''
@page{size:A4;margin:0}*{box-sizing:border-box}body{font-family:'Noto Sans',Arial,sans-serif;margin:0;background:#f6f4ed;color:#1d302b;font-synthesis:none;print-color-adjust:exact;-webkit-print-color-adjust:exact}.page{width:210mm;min-height:297mm;padding:19mm 20mm 16mm}.eyebrow{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#225f4d;margin:0 0 16px}h1{font-size:30px;line-height:1.2;letter-spacing:-.03em;margin:0 0 13px;font-weight:600}.subtitle{font-size:13px;color:#66756d;margin:0 0 25px;line-height:1.6}h2{font-size:15px;font-weight:600;margin:22px 0 8px;color:#225f4d}p{font-size:12px;line-height:1.75;margin:0 0 11px}.takeaway{font-size:15px;line-height:1.7;border-top:2px solid #225f4d;border-bottom:1px solid #d9ddd2;padding:17px 0;margin:22px 0}table{border-collapse:collapse;width:100%;font-size:11px;line-height:1.5}td{border-bottom:1px solid #d9ddd2;padding:9px 0}td:first-child{width:18%;color:#225f4d}footer{font-size:10px;line-height:1.65;color:#66756d;border-top:1px solid #d9ddd2;padding-top:13px;margin-top:25px}
'''
content='''
<p class="eyebrow">Πρόταση διάλεξης / Software Engineering MSc</p>
<h1>AI στην παραγωγή λογισμικού</h1>
<p class="subtitle">Από το ticket έως το merge<br>60 λεπτά με συμμετοχικό εργαστήριο Java και CI</p>
<h2>Σκοπός</h2>
<p>Οι φοιτητές μαθαίνουν να αναθέτουν την υλοποίηση στο AI και να αξιολογούν το αποτέλεσμα πριν από το merge. Η έμφαση είναι στα αυτοματοποιημένα tests, στην ποιότητα των ελέγχων, στα τεκμήρια και στη μέτρηση του ανθρώπινου χρόνου review.</p>
<p class="takeaway">Η βασική δουλειά του engineer μεταφέρεται στην κατασκευή και συντήρηση ενός αξιόπιστου AI pipeline, ώστε οι συνήθεις αλλαγές να απαιτούν ελάχιστο ανθρώπινο review.</p>
<h2>Δομή της ώρας</h2>
<table><tbody>
<tr><td>0-15′</td><td>Ticket, acceptance contract, context και αγγλικά prompts</td></tr>
<tr><td>15-31′</td><td>AI υλοποίηση, πραγματικά CI failures και repair</td></tr>
<tr><td>31-45′</td><td>Αξιολόγηση των ελέγχων, metrics και σύντομη εξήγηση PR</td></tr>
<tr><td>45-60′</td><td>Review, merge και περαιτέρω αυτοματοποίηση με AI reviews</td></tr>
</tbody></table>
<h2>Συμμετοχή και υλικό</h2>
<p>Τα ζεύγη δουλεύουν σε έτοιμο Java repository, ανοίγουν PR και διαβάζουν τα αποτελέσματα GitHub Actions. Δίνεται αντίστοιχο Jenkinsfile. Το παράδειγμα περνά τα υπάρχοντα tests αλλά αποτυγχάνει σε οριακές περιπτώσεις, ώστε η αξιολόγηση να γίνει συγκεκριμένη.</p>
<p>Περιλαμβάνονται παρουσίαση HTML και PDF, οδηγός φοιτητών, αγγλικά prompts, speaker notes και αναλυτικό σενάριο διδάσκοντα. Οι πρακτικές της Lauren Tan και η πρόταση του Karpathy για σαφή εξήγηση συνδέονται με πρωτογενείς πηγές.</p>
<h2>Προϋποθέσεις</h2>
<p>Εξοικείωση με Java και CI. Laptop, browser, internet και GitHub account για το lab. Η προτεινόμενη διαδρομή δεν απαιτεί paid AI subscription ή εγκατάσταση Jenkins. Το repository, τα permissions και ένα live CI run προετοιμάζονται πριν από το μάθημα.</p>
<footer>Το βασικό lab διδάσκει τα στάδια με ανθρώπινο reviewer. Το CI-connected AI review και το auto-merge παρουσιάζονται ως η επόμενη εφαρμογή ενός μετρημένου και ελεγχόμενου pipeline.</footer>
'''
p=ROOT/'build';p.mkdir(exist_ok=True)
(p/'proposal.html').write_text('<!doctype html><html lang="el"><head><meta charset="utf-8"><title>Πρόταση διάλεξης</title><style>'+fontcss+style+'</style></head><body><main class="page">'+content+'</main></body></html>',encoding='utf-8')
email='''Θέμα: Πρόταση διάλεξης για AI στην παραγωγή λογισμικού

Καλησπέρα σας,

Σας στέλνω την πρότασή μου για μια διάλεξη 60 λεπτών με θέμα τη χρήση AI από το ticket έως το merge, προσαρμοσμένη σε μεταπτυχιακούς φοιτητές με γνώση Java και Jenkins.

Περιλαμβάνει σύντομο εργαστήριο με έτοιμο repository και CI, με έμφαση στην αυτοματοποιημένη αξιολόγηση, στα AI reviews και στις τεκμηριωμένες περιγραφές PR. Το βασικό μήνυμα είναι πώς ένα αξιόπιστο AI pipeline μπορεί να μειώσει τον ανθρώπινο χρόνο review.

Επισυνάπτω τη μονοσέλιδη πρόταση και την παρουσίαση σε PDF. Θα ήθελα τη γνώμη σας για τη δομή και το επίπεδο του περιεχομένου.

Με εκτίμηση,
[Ονοματεπώνυμο]
'''
(ROOT/'outputs/email-to-professor-el.txt').write_text(email,encoding='utf-8')
print('Prepared one-page proposal and short email draft.')
