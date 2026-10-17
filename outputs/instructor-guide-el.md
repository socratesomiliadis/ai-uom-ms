# Παραγωγή κώδικα με AI από το ticket έως το merge

## Σκοπός και μαθησιακά αποτελέσματα

Διάλεξη 60 λεπτών για μεταπτυχιακούς φοιτητές Software Engineering με γνώση Java και Jenkins. Το AI αναλαμβάνει την υλοποίηση και τη διόρθωση του κώδικα. Ο μηχανικός αναλαμβάνει το συμβόλαιο συμπεριφοράς, το περιβάλλον εκτέλεσης, την αξιολόγηση και την απόφαση για merge. Η αυτονομία αυξάνεται όταν υπάρχουν αποδείξεις ότι οι έλεγχοι εντοπίζουν τις αποτυχίες που μας ενδιαφέρουν.

Στο τέλος, κάθε φοιτητής πρέπει να μπορεί να μετατρέψει ένα ticket σε ελέγξιμες απαιτήσεις, να διακρίνει το self-check του agent από ανεξάρτητη αξιολόγηση, να ερμηνεύσει τα αποτελέσματα ενός CI run, να μετρήσει την απόδοση ενός workflow και να αιτιολογήσει την έγκριση ή την απόρριψη ενός PR.

Το lab κάνει ορατά τα βασικά στάδια ώστε οι φοιτητές να καταλάβουν πώς ελέγχεται μία αλλαγή. Το τελικό takeaway είναι: **η βασική δουλειά του engineer μεταφέρεται στην κατασκευή και συντήρηση ενός αξιόπιστου AI pipeline, ώστε πολλές συνήθεις αλλαγές να φτάνουν σε merge με ελάχιστο ανθρώπινο review.** Το pipeline συνδυάζει tests, AI reviews, κύκλους διόρθωσης και σύντομες περιγραφές PR από πραγματικά αποτελέσματα. Η πρόοδος μετριέται με χρόνο ανθρώπινου review, rework, defects που ξεφεύγουν και συνολικό κόστος.

## Η γλώσσα των prompts

Όλα τα copy-paste prompts δίνονται στα αγγλικά. Οι διαφάνειες και η διδασκαλία παραμένουν στα ελληνικά, και τα prompts μπορούν να ζητούν ελληνική εξήγηση ή περιγραφή PR. Τα αγγλικά είναι πρακτική προεπιλογή για technical instructions και μπορούν να μειώσουν τα input tokens και να βοηθήσουν την απόδοση σε ορισμένα μοντέλα και tasks. Το όφελος στην ποιότητα επιβεβαιώνεται με evals στο πραγματικό workflow.

Δεν υπάρχει καθολικός κανόνας ότι τα αγγλικά δίνουν καλύτερη απάντηση ή χαμηλότερη συνολική χρέωση. Η tokenization εξαρτάται από την κωδικοποίηση και η ποιότητα από το task, το μοντέλο και το context. Το output μπορεί να παραμείνει ελληνικό. [OpenAI token counting](https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens), [Multilingual prompting research](https://aclanthology.org/2023.findings-emnlp.826/), [Παράδειγμα όπου άλλο prompt language αποδίδει καλύτερα](https://aclanthology.org/2024.findings-emnlp.916/).

Στο σύντομο prompt της διαφάνειας 7, μετρήσαμε **37 tokens στα αγγλικά και 64 στα ελληνικά** με `o200k_base`. Με `cl100k_base` οι αντίστοιχοι αριθμοί είναι 37 και 119. Πρόκειται για τα δύο συγκεκριμένα instruction strings, χωρίς ticket, κώδικα, message formatting ή output. Δεν είναι benchmark μοντέλου.

## Προετοιμασία διδάσκοντα

Δώστε το `student-lab-el.md` και δημοσιεύστε το περιεχόμενο του `ai-production-lab.zip` σε ένα δικό σας δημόσιο εκπαιδευτικό repository πριν από το μάθημα. Το ZIP περιέχει τον σκόπιμα ελαττωματικό αρχικό κώδικα, Maven Wrapper, JUnit tests, evaluator, GitHub Actions και Jenkinsfile. Το `instructor-assets.zip` περιέχει λύση αναφοράς, πέντε παραλλαγές με γνωστά σφάλματα και αποτελέσματα επαλήθευσης. Κρατήστε τη λύση αναφοράς εκτός του student repository.

Στο GitHub, ενεργοποιήστε Actions και δημιουργήστε branch protection για `main`: απαίτηση PR, τουλάχιστον μία ανεξάρτητη έγκριση, dismissal παλιών approvals όταν αλλάζει το diff, επίλυση συζητήσεων και required check `ticket-evaluation`. Επιλέξτε GitHub Actions ως expected source του check. Ζητήστε ενημερωμένο branch πριν από merge και εφαρμόστε τους κανόνες και στους administrators, όπου επιτρέπεται. Ορίστε το required check αφού έχει εμφανιστεί από ένα πρώτο δοκιμαστικό PR. Αυτές οι δυνατότητες είναι διαθέσιμες και για δημόσια repositories στο GitHub Free. [GitHub branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

Χωρίστε τους φοιτητές σε ζεύγη. Ένας χειρίζεται το AI και το PR, ο άλλος ελέγχει τις απαιτήσεις και τα στοιχεία. Αλλάζουν ρόλους στο review. Για πραγματική έγκριση PR, χρειάζεται reviewer με write permission στο αντίστοιχο repo. Οι φοιτητές μπορούν να δουλέψουν σε δικά τους δημόσια forks και να προσθέσουν τον συνεργάτη τους ως collaborator. Ο διδάσκων κρατά ένα ανεξάρτητο demo repo ώστε να δείξει το merge χωρίς να περιμένει όλη την τάξη.

Κάντε μία πρόβα με browser-only διαδικασία. Ετοιμάστε ένα αρχικό PR και τα screenshots ή logs των δύο runs: `Legacy demo` PASS και `Ticket evaluation` FAIL. Μόνο το `ticket-evaluation` είναι required acceptance check. Αν το CI καθυστερήσει στο μάθημα, προβάλετε τα αποθηκευμένα αποτελέσματα ενώ το πραγματικό run συνεχίζεται. Ελέγξτε ότι το AI εργαλείο των ομάδων έχει διαθέσιμο δωρεάν όριο χρήσης πριν από τη διάλεξη.

Η δωρεάν διαδρομή χρησιμοποιεί δημόσιο GitHub repo, standard Ubuntu runner και Copilot Free ή άλλο ήδη διαθέσιμο δωρεάν chat. Το Copilot Free έχει περιορισμούς· μην υποσχεθείτε συγκεκριμένο μοντέλο ή απεριόριστα requests. Δεν απαιτείται cloud coding agent ή paid code review. Οι standard runners είναι δωρεάν για δημόσια repositories, ενώ artifact storage έχει όρια. Το workflow κρατά μικρά reports για μία ημέρα. [Copilot plans](https://docs.github.com/en/copilot/get-started/plans), [Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions).

## Πρόγραμμα 60 λεπτών

| Λεπτά | Περιεχόμενο | Συμμετοχή φοιτητών |
| --- | --- | --- |
| 0–4 | Ρόλοι και αρχικό ερώτημα | Ψηφοφορία για το τι αρκεί ως απόδειξη |
| 4–10 | Ticket και κριτήρια αποδοχής | 2 λεπτά για να εντοπίσουν ασάφειες |
| 10–15 | Repository context και δικαιώματα | Επανεξήγηση του ticket από το AI |
| 15–23 | Παραγωγή αλλαγής και πρώτοι έλεγχοι | 5 λεπτά για prompt και Java patch |
| 23–31 | Ανεξάρτητη αξιολόγηση στο CI | 3 λεπτά για ανάγνωση αποτυχιών |
| 31–39 | Αξιολόγηση των ελέγχων και metrics | 2 λεπτά για υπολογισμό detection rate |
| 39–45 | Εξήγηση με αρχές ASD-STE100 | 2 λεπτά για rewrite και έλεγχο ισχυρισμών |
| 45–48 | Peer review και τεκμηριωμένη απόφαση | 3 λεπτά για review άλλης ομάδας |
| 48–52 | Δωρεάν instructor demo AI review → repair → CI → PR | Πραγματικό rehearsal run, με χειροκίνητο handoff |
| 52–54 | Απόφαση για merge | Required checks, τρέχον evidence και ανεξάρτητο approval |
| 54–58 | Πρακτικές της Tan και περαιτέρω αυτοματοποίηση | Το αξιόπιστο pipeline μειώνει το ανθρώπινο review |
| 58–60 | Exit ticket | 3 σύντομες απαντήσεις |

Οι δραστηριότητες περιλαμβάνονται στον χρόνο κάθε ενότητας. Το setup έχει ολοκληρωθεί πριν από το μάθημα. Αν χαθεί χρόνος, περιορίστε το live generation και δώστε το έτοιμο αρχικό candidate· κρατήστε το CI, το explanation exercise και το review.

Οι παρακάτω ενότητες οργανώνουν την ύλη. Για ακριβή αντιστοίχιση με τις 28 διαφάνειες και τη χρονική ροή, χρησιμοποίησε τα speaker notes και το rehearsal script.

## Ενότητα 1 Οι ευθύνες όταν το AI γράφει κώδικα

**Στην οθόνη:** Engineer: intent, constraints, evaluation, approval. Agent: implementation, self-check, repair, PR draft. CI: επαναλήψιμοι έλεγχοι και πραγματικά αποτελέσματα.

**Λόγια διδάσκοντα:** «Σήμερα θα ζητήσουμε από το AI να υλοποιήσει μία αλλαγή. Η δουλειά μας είναι να ορίσουμε τι σημαίνει σωστή αλλαγή και πώς θα το αποδείξουμε. Η ευθύνη για το merge ανήκει στον εξουσιοδοτημένο reviewer. Η βεβαιότητα του agent δεν αντικαθιστά την απόδειξη.»

**Αρχική ψηφοφορία:** «Ποιο από τα παρακάτω αρκεί για merge: μεταγλώττιση, πράσινα υπάρχοντα tests, δεύτερο AI που λέει “looks good”, ή αξιολόγηση βάσει ticket μαζί με ανεξάρτητο review;» Εξηγήστε ότι ακόμη και η τελευταία επιλογή εξαρτάται από την ποιότητα των απαιτήσεων και των ελέγχων.

## Ενότητα 2 Το ticket είναι συμβόλαιο συμπεριφοράς

**Στην οθόνη:** Ticket `PRICING-142`: υποστήριξη του κουπονιού `STUDENT10` στον υπάρχοντα υπολογισμό τελικής τιμής.

Το API παραμένει `PriceCalculator.calculate(BigDecimal subtotal, String coupon)`. Το subtotal είναι από 0 έως 10000 ευρώ, με ακρίβεια το πολύ δύο δεκαδικών. Επιπλέον μηδενικά, όπως `50.000`, επιτρέπονται επειδή δεν αλλάζουν την αριθμητική ακρίβεια. Null subtotal, αρνητικό ποσό, υπέρβαση ορίου και πραγματικό τρίτο δεκαδικό προκαλούν `IllegalArgumentException`.

Το κουπόνι αναγνωρίζεται χωρίς διάκριση πεζών/κεφαλαίων και με αφαίρεση whitespace στα άκρα μέσω `strip()`. Null, κενό και άγνωστο κουπόνι σημαίνουν καμία έκπτωση. Για `STUDENT10` και subtotal **τουλάχιστον 50.00**, η έκπτωση είναι 10%, με ανώτατο όριο 20.00. Η έκπτωση στρογγυλοποιείται πρώτα σε δύο δεκαδικά με `HALF_UP`, και κατόπιν αφαιρείται. Το αποτέλεσμα έχει πάντα scale 2.

| Παράδειγμα | Αναμενόμενο τελικό ποσό | Τι εξετάζει |
| --- | --- | --- |
| 49.99 και STUDENT10 | 49.99 | Κάτω από το όριο |
| 50.00 και STUDENT10 | 45.00 | Συμπερίληψη ορίου |
| 50.05 και STUDENT10 | 45.04 | Στρογγυλοποίηση της έκπτωσης |
| 500.00 και STUDENT10 | 480.00 | Ανώτατο όριο έκπτωσης |
| 100.00 και OTHER | 100.00 | Διατήρηση συμπεριφοράς χωρίς έκπτωση |

**Άσκηση 2 λεπτών:** Πρώτα δείξτε μόνο τη φράση «10% έκπτωση για παραγγελίες πάνω από 50 ευρώ». Ζητήστε δύο ασάφειες. Αναμενόμενες απαντήσεις: `>` ή `>=`, σειρά στρογγυλοποίησης, cap, invalid input, normalization. Μετά αποκαλύψτε το πλήρες ticket. Οι σημαντικές αποφάσεις γίνονται πριν από την παραγωγή κώδικα.

Το `BigDecimal` υποστηρίζει ρητό rounding mode. Στο παράδειγμα δημιουργείται από δεκαδικά strings ώστε η τιμή του ticket να μην περάσει πρώτα από αναπαράσταση `double`. [Java BigDecimal](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/math/BigDecimal.html).

## Ενότητα 3 Ο agent χρειάζεται συγκεκριμένο context

**Στην οθόνη:** ticket, API, σχετικό αρχείο, `AGENTS.md`, commands, feature map, εργαλεία αξιολόγησης, σαφές finish condition.

Η Lauren Tan προτείνει verification skill που επιτρέπει στον agent να τρέχει, να ελέγχει και να κάνει debug την εφαρμογή. Το feature map καταγράφει τι κάνουν οι λειτουργίες και πώς τις ασκεί κάποιος. Η συντήρησή του είναι μέρος της υποδομής αξιολόγησης. Στο εργαστήριο μεταφέρουμε αυτή την ιδέα σε `docs/feature-map.md` και μία επαναλήψιμη εντολή evaluator. [Το post που δόθηκε ως παράδειγμα, 30 Ιουλίου 2026](https://x.com/poteto/status/2082874054483255805), [Verification is all you need, 31 Αυγούστου 2026](https://x.com/poteto/status/2094457600259842065).

Η ίδια προτείνει να ζητάμε από τον agent να επαναδιατυπώνει το πρόβλημα πριν ξεκινήσει. Αυτό δίνει στον engineer μια ευκαιρία να εντοπίσει παρερμηνείες. [The art of supervising someone smarter than you, 9 Σεπτεμβρίου 2026](https://x.com/poteto/status/2097732320606507506).

**Prompt κατανόησης:**

```text
Read the provided ticket, AGENTS.md, feature map, and PriceCalculator.java.
Restate the acceptance contract in six short sentences.
Give the expected outputs for subtotals 49.99, 50.00, 50.05, and 500.00 with STUDENT10.
Flag any ambiguity before changing code. Do not edit files yet.
```

**Context για τον agent:** Δώστε ολόκληρο το repository, τον στόχο, παραδείγματα και τα εργαλεία αξιολόγησης. Ο agent εξερευνά, επιλέγει αρχεία και υλοποίηση, δοκιμάζει και βελτιώνει τη λύση από το feedback. Η αξιολόγηση της τελικής συμπεριφοράς και του evidence είναι το κέντρο της διαδικασίας.

## Ενότητα 4 Παραγωγή και μικρός κύκλος διόρθωσης

**Στην οθόνη:** understand → implement → run → inspect failure → repair. Ο agent επιλέγει τα αρχεία και τη στρατηγική υλοποίησης με βάση τον στόχο και το feedback.

**Prompt υλοποίησης:**

```text
Implement PRICING-142 using the provided acceptance contract.
Explore the repository and choose the implementation and files needed to meet the objective.
You may add or refactor classes, supporting tests, resources, documentation, and build configuration.
Preserve the agreed public behavior and API. Explain how your decisions serve the objective.
Use the available tools to run your own checks and the independent acceptance evaluator.
Report the exact commands and actual results. If you cannot run a check, write NOT RUN.
If you are working in browser chat, return every changed file with its path and complete content.
Summarize the change and evidence for the PR. Do not merge the PR.
```

**Άσκηση 5 λεπτών:** Κάθε ζεύγος στέλνει το prompt στο δωρεάν εργαλείο του, μεταφέρει την αλλαγή στο αρχείο και ανοίγει PR. Επιτρέπεται copy/paste από chat. Δεν απαιτείται agent με πρόσβαση στο repository. Ζητήστε μία νέα προσπάθεια όταν υπάρχει συγκεκριμένο failure· μην επαναλαμβάνετε ένα αόριστο «try harder».

Όταν ένας πραγματικός coding agent μπορεί να τρέξει την εφαρμογή, τα self-checks μειώνουν τις αποτυχημένες υποβολές. Ο evaluator που αποφασίζει την αποδοχή έχει ξεχωριστό έλεγχο και version. Ένα δεύτερο μοντέλο μπορεί να εντοπίσει κάτι χρήσιμο, αλλά μπορεί επίσης να μοιράζεται τις ίδιες υποθέσεις με το πρώτο.

## Ενότητα 5 Ένα πράσινο legacy run με λάθος αποτέλεσμα

**Στην οθόνη:** Ο αρχικός κώδικας περνά 3/3 legacy tests. Ο acceptance evaluator αναφέρει 5 failures σε 27 tests.

Το ZIP ξεκινά με μία ενδεικτική λανθασμένη υλοποίηση για τη διδασκαλία. Τα legacy tests εξετάζουν μόνο 40.00, 100.00 με έγκυρο κουπόνι και 100.00 με άγνωστο κουπόνι. Η υλοποίηση χρησιμοποιεί `> 50` και στρογγυλοποιεί το τελικό ποσό. Επομένως δίνει 50.00 αντί 45.00 στο όριο και 45.05 αντί 45.04 για subtotal 50.05.

**Λόγια διδάσκοντα:** «Το CI απάντησε σωστά στην ερώτηση που του θέσαμε. Η ερώτηση ήταν ανεπαρκής. Πρέπει να ελέγξουμε αν οι δοκιμές μας θα απέρριπταν τις αλλαγές που φοβόμαστε.»

**Άσκηση 3 λεπτών:** Οι φοιτητές διαβάζουν `result.json` και εντοπίζουν δύο πραγματικές αποκλίσεις από το ticket. Αν η δική τους αλλαγή πέρασε με την πρώτη, συγκρίνουν με το baseline report. Ένα test failure είναι counterexample. Ζητούν από το AI μια διόρθωση με αναφορά στον αντίστοιχο όρο του ticket.

## Ενότητα 6 Τρεις διαφορετικές αξιολογήσεις

**Στην οθόνη:** correctness της αλλαγής, quality του evaluator, usefulness του workflow.

| Ερώτημα | Κατάλληλο μέσο | Περιορισμός |
| --- | --- | --- |
| Δίνει η αλλαγή τα σωστά αποτελέσματα; | Acceptance tests, regression tests, ιδιότητες, integration checks όπου απαιτούνται | Οι δοκιμές καλύπτουν συγκεκριμένη συμπεριφορά |
| Εντοπίζουν οι έλεγχοι γνωστά σφάλματα; | Seeded faults ή mutation testing, έλεγχος test oracle | Το διαθέσιμο σύνολο σφαλμάτων μπορεί να είναι εύκολο |
| Είναι χρήσιμο το συνολικό AI workflow; | Ιστορικά tickets, επαναλήψεις, baseline, review/rework και cost metrics | Ένα ticket ή ένα demo δεν αποδεικνύει παραγωγικότητα |

Μια eval για coding agent περιλαμβάνει task, αρχική κατάσταση repository, εργαλεία και permissions, budget και grader. Ο grader εξετάζει το τελικό artifact και, όταν χρειάζεται, καταγεγραμμένες ενέργειες. Code-based checks, μοντέλα ως κριτές και ανθρώπινο review εξυπηρετούν διαφορετικές ανάγκες. Στη συγκεκριμένη άσκηση η αριθμητική ορθότητα κρίνεται με εκτελέσιμο κώδικα, ενώ η επάρκεια της εξήγησης αξιολογείται με rubric. [Anthropic, Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

**Κρίσιμο σημείο:** Tests που παράγονται από τον ίδιο agent μπορούν να κωδικοποιήσουν το ίδιο λάθος με την υλοποίηση. Ο άνθρωπος ελέγχει τα αναμενόμενα αποτελέσματα από το ticket. Στο lab υπάρχει και δεύτερος oracle σε ακέραια cents: για επιλέξιμο subtotal `c`, η έκπτωση σε cents είναι `min((c + 5) / 10, 2000)` με ακέραια διαίρεση. Είναι διαφορετική αναπαράσταση του ίδιου συμβολαίου, χρήσιμη για 500 καθορισμένα inputs.

## Ενότητα 7 Αξιολόγηση των ελέγχων

**Στην οθόνη:** πέντε γνωστά σφάλματα: όριο, rounding, cap, normalization, validation.

Το instructor package περιέχει πέντε παραλλαγές που εισάγουν ένα σφάλμα η καθεμία στη σωστή λύση. Ο evaluator απορρίπτει και τις πέντε. Η λύση αναφοράς περνά 27/27 tests. Το property test εξετάζει 500 inputs μέσα σε ένα από τα 27 tests· αυτά δεν είναι 500 ανεξάρτητα tickets ή agent trials.

**Άσκηση 2 λεπτών:** «Απορρίφθηκαν 5 από 5 γνωστές λανθασμένες παραλλαγές. Ποιο είναι το detection rate; Τι δεν μας λέει;» Απάντηση: 100% στο συγκεκριμένο σύνολο. Δεν εκτιμά το ποσοστό άγνωστων bugs ούτε τη συνολική ασφάλεια της εφαρμογής. Οι παραλλαγές επιλέχθηκαν για να εξετάσουν τις απαιτήσεις του ticket, όχι ως τυχαίο δείγμα όλων των πιθανών failures.

Σε μεγαλύτερο Java project, το PIT δημιουργεί μεταλλάξεις και ελέγχει αν οι δοκιμές τις ανιχνεύουν. Χρειάζεται ερμηνεία για ισοδύναμες μεταλλάξεις και για το πραγματικό πεδίο των tests. Το lab χρησιμοποιεί πέντε χειροποίητα seeded faults· το αποτέλεσμα **δεν ονομάζεται PIT mutation score**. [PIT Maven quickstart](https://pitest.org/quickstart/maven/).

Το coverage δείχνει ποιος κώδικας εκτελέστηκε. Δεν αποδεικνύει ότι το expected result είναι σωστό ή ότι υπάρχουν χρήσιμα assertions. Σε παραγωγή μπορείτε να ορίσετε ένα συμφωνημένο κατώφλι για σημαντικό κώδικα, μαζί με συμπεριφορικούς ελέγχους. Η JaCoCo παρέχει μηχανισμό ελέγχου ορίων coverage. [JaCoCo check](https://www.jacoco.org/jacoco/trunk/doc/check-mojo.html).

Η Tan προτείνει να μετατρέπουμε επαναλαμβανόμενες διορθώσεις πρώτα σε δομική λύση, κατόπιν σε lint ή test και ύστερα σε οδηγίες για agents. Στο παράδειγμά μας καταγράφουμε μόνιμα το boundary και το rounding counterexample στην ανεξάρτητη σουίτα. [Post για την εξάλειψη επαναλαμβανόμενων διορθώσεων, 16 Αυγούστου 2026](https://x.com/poteto/status/2089067865098113024).

## Ενότητα 8 Μέτρηση ενός AI workflow

**Στην οθόνη:** Μετράμε αποδεκτές αλλαγές, χρόνο ανθρώπου, rework, αποτυχίες που ξέφυγαν και κόστος.

| Metric | Ορισμός | Χρήση |
| --- | --- | --- |
| First-attempt acceptance | Tickets που πέρασαν στην πρώτη υποβολή / όλα τα ξεκινημένα tickets | Ποιότητα αρχικής υποβολής χωρίς κρυφές επαναλήψεις |
| Acceptance within budget | Tickets που έγιναν αποδεκτά εντός συμφωνημένων limits / όλα τα ξεκινημένα tickets | Αποτελεσματικότητα με retries |
| Human effort per accepted change | Specification + review + ενεργός χρόνος διορθώσεων, με αναφορά και των εγκαταλειμμένων tasks | Αν μειώνεται η δουλειά του engineer |
| Lead time | Χρόνος από έτοιμο ticket έως αποδεκτό merge | Περιλαμβάνει ουρές και CI |
| Cost per accepted change | Συνολικό AI και CI κόστος όλων των attempts / αποδεκτές αλλαγές | Περιλαμβάνει αποτυχημένες και εγκαταλειμμένες προσπάθειες |
| Escape rate | Αποδεκτές αλλαγές με confirmed defect εντός σταθερού χρονικού παραθύρου / αλλαγές που παρακολουθήθηκαν για όλο το παράθυρο | Ποιότητα μετά την αποδοχή |
| Evaluator false accept rate | Γνωστά λανθασμένα candidates που έγιναν δεκτά / όλα τα γνωστά λανθασμένα candidates | Έλεγχος του grader σε gold set |

**Αριθμητικό παράδειγμα για την τάξη:** Σε 20 tickets, 12 έγιναν δεκτά με την πρώτη και 16 εντός budget. First-attempt acceptance = 60%, acceptance within budget = 80%. Συνολικό AI και CI κόστος 24 ευρώ δίνει 1.50 ευρώ ανά αποδεκτή αλλαγή. Αν το free εργαλείο δεν εκθέτει token counts, τα καταγράφουμε ως άγνωστα· δεν τα εκτιμούμε από το μήκος της απάντησης. Αυτοί οι αριθμοί είναι υποθετικοί για την άσκηση.

Για πραγματικό pilot επιλέξτε, ενδεικτικά, 20–30 αντιπροσωπευτικά παλιά tickets διαφορετικής δυσκολίας και κινδύνου, με καθαρό αρχικό commit. Κρατήστε σταθερά runtime, tools, budget και grader. Κάντε περισσότερα από ένα runs ανά ticket σε ανεξάρτητα workspaces. Συγκρίνετε με συμφωνημένο baseline, όπως το ίδιο εργαλείο χωρίς το νέο verification playbook ή μια human-only διαδικασία. Εναλλάξτε τη σειρά για να μειώσετε learning effects.

Ορίστε πρώτα ένα development set για βελτίωση prompts και ένα held-out set για σύγκριση. Μην προσαρμόζετε συνέχεια τον grader για να περάσει η τρέχουσα υλοποίηση. Μην αλλάζετε ταυτόχρονα μοντέλο, prompts και permissions και αποδίδετε όλο το αποτέλεσμα σε έναν παράγοντα. Αναφέρετε αριθμό tasks και trials, median και διασπορά χρόνων, αβεβαιότητα και ποια κατηγορία tickets εκπροσωπείται. Μικρό δείγμα δίνει ενδείξεις για pilot, όχι γενική εγγύηση.

Η Tan προτείνει να προσθέτουμε skills όταν έχουμε παρατηρήσει πρόβλημα και να συγκρίνουμε αν πράγματι βοηθούν. Η εφαρμογή εδώ είναι μια σύγκριση workflow με και χωρίς feature map, με ίδιο task set και grader. [Post για επιλεκτική χρήση skills και evals, 28 Αυγούστου 2026](https://x.com/poteto/status/2093182292915298366).

## Ενότητα 9 Εξήγηση που μπορεί να ελεγχθεί

**Στην οθόνη:** απαίτηση → αλλαγή → αποτέλεσμα ελέγχου → περιορισμός. Η εξήγηση διευκολύνει την επιθεώρηση των στοιχείων.

Ο Karpathy προτείνει να ζητάμε εξηγήσεις κοντά στο ASD-STE100, ακόμη και «80%» όταν η αυστηρή μορφή γίνεται δύσκαμπτη. Προτείνει επίσης διαγράμματα και διαδραστικές σελίδες όταν βοηθούν την κατανόηση. Το ASD-STE100 είναι ελεγχόμενη **αγγλική** γλώσσα. Για το ελληνικό υλικό υιοθετούμε αρχές σαφήνειας, χωρίς ισχυρισμό συμμόρφωσης ή πιστοποίησης. [Karpathy, 2 Οκτωβρίου 2026](https://x.com/karpathy/status/2105819303471976479), [ASD-STE100](https://www.asd-ste100.org/).

**Πριν:** «Η υλοποίηση διασφαλίζει robust και seamless handling όλων των pricing scenarios, βελτιστοποιώντας την ακρίβεια και διατηρώντας backward compatibility.»

**Μετά:** «Το κουπόνι εφαρμόζεται όταν το subtotal είναι τουλάχιστον 50.00. Ο κώδικας περιορίζει την έκπτωση σε 20.00. Στρογγυλοποιεί την έκπτωση πριν την αφαιρέσει. Για subtotal 50.05, η έκπτωση είναι 5.01 και η τελική τιμή 45.04. Το acceptance test για 50.05 πέρασε στο αναφερόμενο CI run. Οι έλεγχοι καλύπτουν τη Java μέθοδο. Δεν εξετάζουν checkout API ή πληρωμές.»

**Prompt εξήγησης:**

```text
Explain the change in Greek using clarity principles inspired by ASD-STE100.
Use one idea per sentence, active voice, and consistent technical terms.
Preserve numbers, conditions, and uncertainty. Do not claim certified ASD-STE100 compliance.
For AC1-AC5, connect the requirement to the code, check name, and actual CI result.
Use only the supplied diff and reports. Write NOT VERIFIED for unsupported claims.
Do not invent executed checks or results. Summarize decisions and evidence, without private reasoning traces.
```

**Άσκηση 2 λεπτών:** Οι ομάδες διορθώνουν το «Πριν», με ένα αριθμητικό παράδειγμα και έναν περιορισμό. Ο reviewer πρέπει να μπορεί να εξηγήσει γιατί το 50.05 δίνει 45.04 χωρίς να ξαναρωτήσει το AI.

**Rubric εξήγησης, 0–2 ανά κριτήριο:** Ορθότητα αριθμών και conditions, αντιστοίχιση σε πραγματικά evidence, κάλυψη βασικών αποφάσεων και ορίων, σαφήνεια όρων. Ένα unsupported claim για εκτελεσμένο test απαιτεί διόρθωση ακόμη και αν η συνολική βαθμολογία είναι υψηλή. Στο lab το rubric εφαρμόζεται από ανθρώπους. Σε παραγωγή, ένα script μπορεί να ελέγχει ότι υπάρχουν απαίτηση, report link και SHA· model judge μπορεί να προτείνει βαθμολογία για πληρότητα και σαφήνεια. Βαθμονομήστε τον judge σε ανθρώπινα παραδείγματα, μετρήστε false accepts και ελέγξτε disagreements. Ο judge δεν αντικαθιστά τις αριθμητικές δοκιμές.

## Ενότητα 10 Η αξιολόγηση μέσα στο pipeline

**Στην οθόνη:**

```text
Ticket και acceptance contract
        ↓
Απομονωμένος agent → Java patch → self-check και repair
        ↓
PR με diff, απαιτήσεις και στοιχεία
        ↓
Στόχος → ελεύθερη υλοποίηση → πλήρες build → acceptance evals → reports
        ↓
Ανεξάρτητο review → νέα αλλαγή σημαίνει νέο run και επανέγκριση
        ↓
Merge της αξιολογημένης κατάστασης
```

| Στάδιο | Τι αυτοματοποιούμε | Τι εξηγούμε |
| --- | --- | --- |
| Ticket | Έλεγχος υποχρεωτικών πεδίων και παραδειγμάτων | Υποθέσεις και κριτήρια αποδοχής |
| Implementation | Build, στοχευμένα self-checks | Αλλαγή API ή συμπεριφοράς και αιτία |
| CI evaluation | Ανεξάρτητα acceptance cases, πρόσθετα candidate tests και build checks | Απαίτηση που απέτυχε και counterexample |
| PR review | Συγκέντρωση reports και αντιστοίχιση σε commit | Αποδεικτικά στοιχεία, κίνδυνοι και NOT VERIFIED |
| Merge | Required checks, approvals και έλεγχος τρέχουσας κατάστασης | Ποιος ενέκρινε, ποιο artifact αξιολογήθηκε και πώς γίνεται revert |

Το workflow αξιολογεί όλο το candidate project. Ο agent μπορεί να αλλάξει δομή, helper classes, tests, resources και build configuration. Τα ανεξάρτητα acceptance cases εκφράζουν τον συμφωνημένο στόχο, ενώ τα δικά του tests προσθέτουν επιπλέον evidence. Το report περιλαμβάνει και ποια required cases εκτελέστηκαν. Η επιλογή αρχείων δεν αποτελεί κριτήριο αποδοχής.

Το report καταγράφει το SHA του checkout που ελέγχθηκε, το SHA της policy, το PR head όταν υπάρχει και το SHA-256 του αρχείου. Στα PRs του GitHub ελέγχεται το συνθετικό merge checkout. Η εξήγηση πρέπει να αναφέρεται σε αυτό το run. Αν αλλάξει το PR ή το base, απαιτείται επανέλεγχος της κατάστασης που θα συγχωνευθεί.

**Αρχή του μαθήματος:** Δίνουμε στον agent σαφή στόχο, πλήρες repository και εργαλεία για πειραματισμό και αξιολόγηση. Εκείνος επιλέγει πώς θα φτάσει στον στόχο. Η ανεξάρτητη αξιολόγηση κρίνει τη συμπεριφορά του τελικού αποτελέσματος. Το εκπαιδευτικό run δεν παρουσιάζεται ως πλήρες production sandbox.

Το lab χρησιμοποιεί `pull_request`, read-only permissions και checkout χωρίς persistent credentials. Αποφεύγει secrets και privileged `pull_request_target` εκτέλεση candidate κώδικα. Τα third-party actions έχουν συγκεκριμένα commit SHAs. [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use), [pull_request_target risks](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target).

Το `Jenkinsfile` καλεί τον ίδιο evaluator σε disposable Linux worker. Ο διδάσκων ή η PR integration δίνει το reviewed `TRUSTED_BASE_SHA`. Στην παραγωγή το job definition και η επιλογή της policy ελέγχονται από το CI administration, χωριστά από το PR. Το `post` δημοσιεύει JUnit και reports ακόμη και όταν αποτύχει η αξιολόγηση. Το Jenkinsfile δεν κάνει merge. [Jenkins Pipeline syntax](https://www.jenkins.io/doc/book/pipeline/syntax/).

## Ενότητα 11 Review και merge

**Άσκηση 3 λεπτών:** Κάθε ζεύγος εξετάζει PR άλλου ζεύγους και καταγράφει APPROVE ή REQUEST CHANGES με ένα συγκεκριμένο στοιχείο. Αν το CI εκκρεμεί, η απόφαση είναι WAIT. Ελέγξτε τα παρακάτω:

1. Η αλλαγή υλοποιεί AC1–AC5 και αιτιολογείται από τον συμφωνημένο στόχο.
2. Το πραγματικό CI run για την τρέχουσα κατάσταση πέρασε χωρίς skipped checks.
3. Η εξήγηση συμφωνεί με τον κώδικα και τα reports. Δεν υπόσχεται μεγαλύτερη κάλυψη.
4. Ο reviewer κατανοεί το όριο, τη στρογγυλοποίηση και ένα counterexample.
5. Τα review findings έχουν διορθωθεί ή απορριφθεί με τεκμηρίωση, και υπάρχει σαφής τρόπος revert.

Παράδειγμα χρήσιμου comment: «Το ticket περιλαμβάνει subtotal 50.00. Το `> 0` το αποκλείει. Το acceptance run δείχνει expected 45.00, actual 50.00. Χρειάζεται inclusive comparison και νέο run.»

Τα σχόλια από AI reviewer αντιμετωπίζονται ως υποθέσεις για διερεύνηση. Αναπαράγουμε την πιθανή αποτυχία ή ελέγχουμε το σχετικό συμβόλαιο. Δεν εφαρμόζουμε κάθε πρόταση αυτόματα. Η Tan δίνει έμφαση σε μικρά PRs με στοιχεία και χωριστή επαλήθευση πριν από το shipping. [pstack Verify and ship](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/06-verify-and-ship.md).

Στο demo ο διδάσκων κάνει merge ενός έτοιμου, αξιολογημένου PR. Οι ομάδες με πράσινο CI και ανεξάρτητη έγκριση μπορούν να κάνουν merge στα εκπαιδευτικά repos τους. Όσοι δεν ολοκληρώσουν παραδίδουν την τεκμηριωμένη απόφαση review. Το merge σε production δεν ισοδυναμεί με επιτυχή deployment: χρειάζεται ξεχωριστή διαδικασία rollout, παρακολούθησης και ανάκαμψης.

## Ενότητα 12 Η συνέχεια του lab και το τελικό takeaway

Αφιερώστε τα λεπτά 54–58 στη σύνθεση. Το βασικό lab παραμένει με ανθρώπινο reviewer. Το κάναμε έτσι για να μάθουν οι φοιτητές ποιες απαιτήσεις, αποτυχίες και τεκμήρια πρέπει να αναγνωρίζει ο επόμενος αυτοματοποιημένος κύκλος.

**Πρώτο λεπτό, πρακτικές της Tan:** Στο Loops You Can Trust η Tan περιγράφει verification tools, artifacts που επιθεωρούνται χωρίς replay και στάδια που σταματούν όταν λείπει η απόδειξη. Οι αναρτήσεις για organic architecture και constraints δίνουν προτεραιότητα σε κανόνες που επιβάλλει ο κώδικας, ο compiler και το CI. Ο «gardener» μετατρέπει επαναλαμβανόμενα προβλήματα σε μόνιμους κανόνες. [Loops You Can Trust](https://x.com/poteto/status/2069824386283319343), [Organic architecture](https://x.com/poteto/status/2078527882499150286), [Gardener](https://x.com/poteto/status/2090546476464451907), [Constraints και software engineering](https://x.com/poteto/status/2106916667599278365).

**Δεύτερο λεπτό, περαιτέρω αυτοματοποίηση:** Το ticket τροφοδοτεί τον implementation agent. Το trusted CI παράγει reports. Ένας reviewer agent παίρνει το τελικό diff, το ticket και τα πραγματικά evidence σε φρέσκο context. Κάθε ουσιαστικό finding έχει θέση, απαίτηση και counterexample. Ο author agent αναπαράγει και διορθώνει πραγματικά findings και επανεκτελεί τα checks. Τέλος το AI παράγει σύντομο PR από την τελική κατάσταση. Η Tan αναφέρει agentic review και αυτόματη διόρθωση πραγματικών bugs πριν από το merge. [Agentic review και repair](https://x.com/poteto/status/2085885450468909083).

**Τρίτο λεπτό, η ανθρώπινη προσοχή:** Για συγκεκριμένες κατηγορίες αλλαγών που έχουν αξιολογηθεί, ο άνθρωπος διαβάζει ένα σύντομο PR και τις εξαιρέσεις του. Η policy μπορεί αργότερα να επιτρέπει auto-merge όταν οι υποχρεωτικοί έλεγχοι, τα review findings και τα στοιχεία της τελικής κατάστασης συμφωνούν. Η Tan περιγράφει agents που κάνουν merge και δικό της review των αλλαγών στο main αργότερα. Αυτό είναι εμπειρία από το δικό της περιβάλλον. Η εφαρμογή στη δική μας ομάδα απαιτεί μετρημένο ιστορικό και συμφωνημένη policy. [Agents που κάνουν merge](https://x.com/poteto/status/2087244771849089270), [Κανόνες στον κώδικα και στο lint](https://x.com/poteto/status/2090181049754206370).

**Τέταρτο λεπτό, takeaway:** «Η βασική δουλειά του engineer μεταφέρεται στην κατασκευή και συντήρηση του συστήματος που παράγει, αξιολογεί και παραδίδει αποδεκτές αλλαγές. Στόχος μας είναι λιγότερος ανθρώπινος χρόνος ανά merge, με ποιότητα που εξακολουθούμε να μετράμε.» Αυτό μπορεί να επιτρέψει πολλά merges με ελάχιστη επιθεώρηση κώδικα. Ο engineer επενδύει σε tests, AI reviews, σαφή PRs, policy και παρακολούθηση των εξαιρέσεων. Οι νέες ή υψηλού κινδύνου κατηγορίες παίρνουν στοχευμένο review.

Σε pilot μετρήστε ενεργό review time, rework και defects που ξεφεύγουν, μαζί με χρόνο συντήρησης του pipeline. Εξετάστε false alarms και missed defects του AI reviewer σε ανθρώπινα ελεγμένο gold set. Νέο context δεν εξασφαλίζει ανεξάρτητες πιθανότητες σφάλματος. Το βασικό student lab χρησιμοποιεί άνθρωπο ως reviewer. Το instructor demo προσθέτει αυτόματο CodeRabbit PR review και CI, με χειροκίνητο handoff για repair. Η πλήρης αυτόματη σύνδεση repair και το auto-merge παραμένουν επόμενα βήματα.

**Exit ticket 2 λεπτών:**

1. Ποιο failure mode θα μετέτρεπες σε μόνιμο check;
2. Ποιο μέρος του ανθρώπινου review μπορεί να αναλάβει το pipeline;
3. Ποια μέτρηση θα δικαιολογούσε μεγαλύτερη αυτονομία;

## Απαντήσεις στις συνηθέστερες ερωτήσεις

**Μπορεί το AI να γράψει και τα tests;** Ναι. Ο άνθρωπος ελέγχει το oracle και η υποχρεωτική αξιολόγηση συντηρείται ανεξάρτητα. Ένα assertion που απλώς επαναλαμβάνει τον αλγόριθμο μπορεί να επιβεβαιώσει το ίδιο λάθος.

**Χρειάζεται πάντα δεύτερο AI;** Όχι. Για αριθμητικό αποτέλεσμα, ο εκτελέσιμος grader είναι πιο άμεσος. Δεύτερο μοντέλο μπορεί να βοηθήσει στο review, μαζί με ρητό rubric και επαλήθευση ευρημάτων.

**Μπορούμε να βάλουμε 100% coverage ως κανόνα;** Μπορούμε να το μετρήσουμε, αλλά δεν τεκμηριώνει από μόνο του ορθότητα. Το κατάλληλο κατώφλι εξαρτάται από τον κώδικα και τον κίνδυνο. Τα συγκεκριμένα counterexamples έχουν ουσιαστικότερη πληροφορία για αυτό το ticket.

**Πώς εξηγούμε τον κώδικα που δεν γράψαμε;** Διαβάζουμε τα κρίσιμα σημεία, ζητάμε σύντομη τεκμηριωμένη εξήγηση και επαληθεύουμε ένα worked example. Αν δεν μπορούμε να αιτιολογήσουμε την αλλαγή, δεν έχουμε ολοκληρώσει το review.

**Τι μετρά το εργαστήριο;** Την αξιολόγηση της συγκεκριμένης Java μεθόδου και την ποιότητα των ελέγχων σε πέντε γνωστά σφάλματα. Δεν εκτιμά model capability ούτε το production escape rate. Αυτά απαιτούν πραγματικά agent trials και παρακολούθηση αλλαγών.

## Πηγές για διανομή

Οι σχετικές αναρτήσεις της Lauren Tan και η πρόταση του Karpathy αναφέρονται στα σημεία όπου χρησιμοποιούνται. Το `lauren-tan-takeaways-el.md` περιλαμβάνει αναλυτική σύνθεση περισσότερων posts και διαχωρίζει τις πρακτικές της από τη δική μας εφαρμογή. Τα pstack commands είναι παραδείγματα από το δικό της εργαλείο· το εργαστήριο υλοποιεί τις αρχές με δωρεάν εργαλεία και δεν απαιτεί εγκατάσταση pstack ή paid Cursor.

Για συνέχεια μετά τη διάλεξη, προτείνετε την ανάγνωση του [pstack verification guide](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/06-verify-and-ship.md) για επαναλήψιμα proof artifacts και του [Anthropic agent eval guide](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) για σχεδιασμό task sets και graders. Οι δικές μας διαδικασίες lab, τα thresholds και τα metrics αποτελούν διδακτική πρόταση εφαρμογής, όχι benchmarks ή οδηγίες των δημιουργών των posts.

## Η παρουσίαση και οι σημειώσεις της

Το deck περιλαμβάνει 25 κύριες διαφάνειες για 60 λεπτά και 3 διαφάνειες παραρτήματος. Οι σημειώσεις ανά διαφάνεια βρίσκονται στο `deck-speaker-notes-el.md`. Οι διαφάνειες 21–24 αντιστοιχούν στο κλείσιμο των λεπτών 54–58. Το πρόγραμμα περιλαμβάνει τον χρόνο των δραστηριοτήτων.


## Νέο instructor demo στα λεπτά 48–52

Το peer review της διαφάνειας 17 διαρκεί πλέον 3 λεπτά (45–48). Οι διαφάνειες 18–19 καλύπτουν το δωρεάν demo review→repair→CI→PR στα 48–52. Η διαφάνεια 20 δείχνει merge στα 52–54. Το closing 54–58 και το exit ticket 58–60 διατηρούνται. Συνολικά: 25 κύριες διαφάνειες και 3 appendices, 60 λεπτά.

Χρησιμοποίησε το `github-demo-setup-el.md` για το public instructor repository και το `demo-prompts-en.md` για repair και τελικό PR. Το demo έχει σωστό main και PR που εξάγει constants, με χειρόγραφο seeded rounding fault. Η διόρθωση κρατά το refactor. Ο φοιτητικός starter διατηρεί τα δικά του γνωστά σφάλματα και δημοσιεύεται σε διαφορετικό repo.

Η CodeRabbit εφαρμογή κάνει αυτόματο review του PR. Το supplied Actions job κάνει acceptance evaluation. Δεν υποθέτουμε ότι η εφαρμογή διάβασε όλα τα artifacts του job. Ο instructor ελέγχει ένα πραγματικό finding, το μεταφέρει στο implementation AI και κάνει push. Το ολοκληρωμένο live rehearsal καταγράφεται στο `demo-run-record-el.md`. Πραγματικό CodeRabbit review, AI repair και GitHub αποτέλεσμα δεν έχουν παραχθεί από την τοπική προετοιμασία.

Αν το review χάσει το fault, δείξε το missed finding μαζί με το πραγματικό acceptance failure. Αν καθυστερεί η υπηρεσία, δείξε το αποθηκευμένο πραγματικό rehearsal run με timestamps ή τα τοπικά fixture reports με σωστή ετικέτα. Το αναμενόμενο finding δεν παρουσιάζεται ως πραγματικό AI output. Στο demo απαιτείται ανεξάρτητη ανθρώπινη έγκριση για merge· αλλιώς κράτησε το PR ανοικτό ως WAIT.
