# Εργαστήριο αξιολόγησης κώδικα AI με Java και CI

## Στόχος

Θα αναθέσετε στο AI ένα ticket, θα αξιολογήσετε την αλλαγή στο CI και θα αποφασίσετε αν ένα PR μπορεί να γίνει merge. Δουλεύετε σε ζεύγη. Ο ένας χειρίζεται το εργαλείο και ο άλλος ελέγχει τις απαιτήσεις. Στο review αλλάζετε ρόλους. Το AI γράφει τον κώδικα· εσείς ορίζετε και ελέγχετε τα κριτήρια αποδοχής.

Το repository δίνεται από τον διδάσκοντα. Χρειάζεστε GitHub account και browser. Μπορείτε να χρησιμοποιήσετε Copilot Free ή άλλο δωρεάν AI chat που ήδη διαθέτετε, εντός των ορίων του. Δεν χρειάζεται paid agent ή τοπικός Jenkins. Αν το AI δεν είναι διαθέσιμο, δουλέψτε πάνω στο αρχικό ενδεικτικό candidate και συγκρίνετε τα αποθηκευμένα reports. Συμμετέχετε κανονικά στην αξιολόγηση και το review. [Copilot plans](https://docs.github.com/en/copilot/get-started/plans).

## Η γλώσσα των prompts

Όλα τα copy-paste prompts δίνονται στα αγγλικά. Οι διαφάνειες και η διδασκαλία παραμένουν στα ελληνικά, και τα prompts μπορούν να ζητούν ελληνική εξήγηση ή περιγραφή PR. Τα αγγλικά είναι πρακτική προεπιλογή για technical instructions και μπορούν να μειώσουν τα input tokens και να βοηθήσουν την απόδοση σε ορισμένα μοντέλα και tasks. Το όφελος στην ποιότητα επιβεβαιώνεται με evals στο πραγματικό workflow.

Δεν υπάρχει καθολικός κανόνας ότι τα αγγλικά δίνουν καλύτερη απάντηση ή χαμηλότερη συνολική χρέωση. Η tokenization εξαρτάται από την κωδικοποίηση και η ποιότητα από το task, το μοντέλο και το context. Το output μπορεί να παραμείνει ελληνικό. [OpenAI token counting](https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens), [Multilingual prompting research](https://aclanthology.org/2023.findings-emnlp.826/), [Παράδειγμα όπου άλλο prompt language αποδίδει καλύτερα](https://aclanthology.org/2024.findings-emnlp.916/).

Στο σύντομο prompt της διαφάνειας 7, μετρήσαμε **37 tokens στα αγγλικά και 64 στα ελληνικά** με `o200k_base`. Με `cl100k_base` οι αντίστοιχοι αριθμοί είναι 37 και 119. Πρόκειται για τα δύο συγκεκριμένα instruction strings, χωρίς ticket, κώδικα, message formatting ή output. Δεν είναι benchmark μοντέλου.

## Το ticket PRICING-142

Υλοποιήστε το κουπόνι `STUDENT10` στη μέθοδο:

```java
public static BigDecimal calculate(BigDecimal subtotal, String coupon)
```

| Κριτήριο | Συμβόλαιο |
| --- | --- |
| AC1 Input | Subtotal από 0 έως 10000, με το πολύ δύο ουσιαστικά δεκαδικά. Τα `50.00` και `50.000` είναι έγκυρα. Null, αρνητικό, πάνω από 10000 ή τρίτο μη μηδενικό δεκαδικό προκαλούν `IllegalArgumentException`. |
| AC2 Κουπόνι | `strip()` στα άκρα και αναγνώριση χωρίς διάκριση πεζών/κεφαλαίων. Null, κενό και άγνωστο κουπόνι σημαίνουν καμία έκπτωση. Η locale δεν αλλάζει τη συμπεριφορά. |
| AC3 Επιλεξιμότητα | Το STUDENT10 εφαρμόζεται όταν subtotal >= 50.00. |
| AC4 Υπολογισμός | Έκπτωση 10%, με cap 20.00. Στρογγυλοποίηση της έκπτωσης με HALF_UP σε δύο δεκαδικά, και μετά αφαίρεση. |
| AC5 Αποτέλεσμα και API | Output scale 2, ίδια API, με τις υποστηρικτικές αλλαγές που επιλέγει ο agent. Οι υπάρχουσες συμπεριφορές χωρίς έκπτωση διατηρούνται. |

Πριν εκτελέσετε κώδικα, συμπληρώστε τις προβλέψεις σας:

| Subtotal και κουπόνι | Αναμενόμενη τιμή |
| --- | --- |
| 49.99 και STUDENT10 | … |
| 50.00 και STUDENT10 | … |
| 50.05 και STUDENT10 | … |
| 500.00 και STUDENT10 | … |
| 100.00 και άγνωστο κουπόνι | … |

## Βήμα 1 Κατανοήστε το συμβόλαιο

Διαβάστε `ticket.md`, `AGENTS.md`, `docs/feature-map.md` και `src/main/java/edu/ai/PriceCalculator.java`. Σε browser chat, δώστε το περιεχόμενό τους ως context. Μην στείλετε κώδικα ή δεδομένα από ιδιωτικό πραγματικό project.

Αυτά είναι σημεία εκκίνησης. Δώστε στο AI πρόσβαση σε όλο το εκπαιδευτικό repository, όπου το εργαλείο το υποστηρίζει. Σε browser chat επισυνάψτε το lab ZIP ή δώστε επιπλέον αρχεία που χρειάζεται, όπως `pom.xml` και tests. Ο agent επιλέγει ποια αρχεία θα εξερευνήσει και θα αλλάξει.

```text
Read the provided ticket, AGENTS.md, feature map, and PriceCalculator.java.
Restate the acceptance contract in six short sentences.
Give the expected outputs for subtotals 49.99, 50.00, 50.05, and 500.00 with STUDENT10.
Flag any ambiguity before changing code. Do not edit files yet.
```

Συγκρίνετε την απάντηση με το ticket και τις δικές σας προβλέψεις. Διορθώστε οποιαδήποτε παρανόηση πριν ζητήσετε υλοποίηση.

## Βήμα 2 Ζητήστε υλοποίηση και ανοίξτε PR

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

Στη browser διαδρομή, δημιουργήστε δημόσιο fork του εκπαιδευτικού repo, ενεργοποιήστε Actions στο fork και δημιουργήστε branch `pricing-142`. Χρησιμοποιήστε Edit ή το github.dev editor για να εφαρμόσετε όλα τα αρχεία της προτεινόμενης λύσης, προσθέτοντας νέα όπου χρειάζεται. Κάντε commit στο branch και ανοίξτε PR **προς το main του δικού σας fork**. Ελέγξτε το base repository πριν πατήσετε Create pull request. Έτσι κάθε ομάδα έχει ξεχωριστό κύκλο CI και merge.

Αν χρησιμοποιείτε το κοινό repo του διδάσκοντα, ακολουθήστε το branch naming που σας έδωσε και ζητήστε review από τον εξουσιοδοτημένο reviewer. Μην κάνετε merge ή push απευθείας στο main.

## Βήμα 3 Διαβάστε τον evaluator

Στο PR επιλέξτε το check `ticket-evaluation`. Διαβάστε το step «Evaluate the complete candidate project» και το summary. Από το Actions run μπορείτε να κατεβάσετε το artifact με `result.json`, `build.log` και JUnit XML.

Το report περιλαμβάνει PASS ή FAIL, αριθμό tests, failures, errors, skipped tests, required cases που εκτελέστηκαν, διάρκεια, SHA της αξιολογημένης κατάστασης και hashes του πλήρους candidate project. Η διάρκεια αφορά build και tests, όχι τον χρόνο παραγωγής κώδικα από το AI. Ένα fail μπορεί να είναι λανθασμένο αποτέλεσμα, compiler error ή timeout. Αναζητήστε την πραγματική αιτία στο `build.log`.

Ο evaluator εξετάζει το πλήρες project και τρέχει τα agreed acceptance cases ανεξάρτητα από τις επιλογές υλοποίησης. Ο agent μπορεί να αναδιοργανώσει αρχεία και να αλλάξει tests ή build configuration. Αξιολογούμε αν η συνολική αλλαγή επιτυγχάνει τον στόχο, μαζί με τα πραγματικά αποτελέσματα και την εξήγησή της.

**Αρχικό παράδειγμα:** Ο κώδικας του starter περνά 3/3 legacy tests. Ο πλήρης evaluator εντοπίζει 5 failures σε 27 tests. Αν το δικό σας candidate περάσει, διαβάστε το baseline report που δίνει ο διδάσκων και εξηγήστε τις διαφορές.

Για να δείτε μόνο τα legacy tests από browser: Actions → Legacy demo → Run workflow → επιλέξτε το branch σας. Το ξεχωριστό check `legacy-demo` είναι demonstration run και δεν αντικαθιστά το required `ticket-evaluation` του PR.

## Βήμα 4 Διορθώστε με βάση ένα counterexample

Αν υπάρχει failure, δώστε στο AI το πλήρες συμβόλαιο και το συγκεκριμένο report:

```text
The independent evaluator reports 45.05 for subtotal 50.05 with STUDENT10.
The acceptance contract requires 45.04 because the discount must be rounded before subtraction.
Use the provided repository and report to diagnose the mismatch.
Choose the changes, files, and tools needed to restore the agreed behavior.
Explain the fix using this example and verify the complete updated project.
Report actual results and remaining uncertainty. If you cannot run a check, write NOT RUN.
```

Κάντε νέο commit στο ίδιο branch. Περιμένετε το νέο run. Μια προηγούμενη πράσινη ένδειξη δεν τεκμηριώνει νέο commit. Αν το αποτέλεσμα παραμένει FAIL, καταγράψτε το· μην αλλάξετε το κριτήριο για να περάσει.

## Βήμα 5 Εξηγήστε την αλλαγή

Συμπληρώστε την περιγραφή PR από το template. Για κάθε AC γράψτε ποιος έλεγχος το εξετάζει και ποιο πραγματικό αποτέλεσμα υπάρχει. Προσθέστε run URL και το SHA που ελέγχθηκε. Αν το μοντέλο δεν γνωρίζει το run, δώστε του το πραγματικό report.

```text
Explain the change in Greek using clarity principles inspired by ASD-STE100.
Use one idea per sentence, active voice, and consistent technical terms.
Preserve numbers, conditions, and uncertainty. Do not claim certified ASD-STE100 compliance.
For AC1-AC5, connect the requirement to the code, check name, and actual CI result.
Use only the supplied diff and reports. Write NOT VERIFIED for unsupported claims.
Do not invent executed checks or results. Summarize decisions and evidence, without private reasoning traces.
```

Το ASD-STE100 αφορά αγγλικά. Εδώ εφαρμόζουμε αρχές σαφήνειας στα ελληνικά. Η ιδέα προέρχεται από το [post του Karpathy](https://x.com/karpathy/status/2105819303471976479). Η σαφήνεια δεν αποτελεί απόδειξη ότι ο κώδικας είναι σωστός.

## Βήμα 6 Κάντε ανεξάρτητο review

Εξετάστε το diff και το report άλλης ομάδας. Επιλέξτε APPROVE, REQUEST CHANGES ή WAIT. Κρατήστε την αιτιολόγηση συγκεκριμένη:

- Εφαρμόζονται τα κριτήρια, ειδικά 50.00, 50.05 και cap 20.00;
- Πέρασε το πλήρες check για την τρέχουσα κατάσταση;
- Πώς συμβάλλει η συνολική αλλαγή στον συμφωνημένο στόχο;
- Είναι αληθείς οι ισχυρισμοί της εξήγησης;
- Μπορείτε να εξηγήσετε ένα worked example χωρίς νέα βοήθεια από AI;

Βαθμολογήστε την εξήγηση από 0 έως 2 σε τέσσερα κριτήρια: ορθότητα, τεκμηρίωση, κάλυψη αποφάσεων και ορίων, σαφήνεια. Ένα ψευδές «tests passed» χρειάζεται διόρθωση ανεξάρτητα από το άθροισμα. Το lab αξιολογεί την εξήγηση με ανθρώπινο rubric, όχι με αυτοματοποιημένο model judge.

Με πράσινο CI και εξουσιοδοτημένο ανεξάρτητο approval, κάντε merge στο εκπαιδευτικό fork σας. Αν δεν ολοκληρώσετε εντός του μαθήματος, παραδώστε το PR και την τεκμηριωμένη απόφαση review. Ο διδάσκων θα δείξει ένα ολοκληρωμένο merge.

## Τι παραδίδετε

Ένα PR με την αλλαγή, σύνδεσμο στο acceptance run, αντιστοίχιση AC1–AC5 και έναν περιορισμό της αξιολόγησης. Προσθέστε εργαλείο και διαθέσιμο model identifier, αριθμό υποβολών, ενεργό ανθρώπινο χρόνο κατανόησης και review, χρόνο CI και merge ή review outcome. Τα token counts που δεν εκθέτει το εργαλείο καταγράφονται ως άγνωστα. Μην παρουσιάσετε το ένα ticket ως benchmark ενός μοντέλου.

Απαντήστε στο exit ticket: ποιο failure mode θα γίνει μόνιμο check, ποιο μέρος του review μπορεί να αναλάβει το pipeline και ποια μέτρηση θα δικαιολογούσε μεγαλύτερη αυτονομία.

## Προαιρετική τοπική διαδρομή

Με Java 17+ και Python 3, χωρίς εγκατεστημένο Maven:

```powershell
.\mvnw.cmd -B -ntp test
python ci/evaluate.py --candidate . --trusted . --mode acceptance --out reports
```

Σε Linux ή macOS:

```bash
chmod +x mvnw
./mvnw -B -ntp test
python3 ci/evaluate.py --candidate . --trusted . --mode acceptance --out reports
```

Η πρώτη εκτέλεση του wrapper κατεβάζει Maven και dependencies. Το `mvnw test` τρέχει τα local tests. Το acceptance run χτίζει ολόκληρο το candidate project και προσθέτει τα agreed contract cases. Για ανεξάρτητη σύγκριση δώστε στο `--trusted` το reviewed contract checkout. Στο GitHub γίνεται αυτόματα ξεχωριστό base checkout.

## Η συνέχεια μετά το βασικό εργαστήριο

Μάθατε τα στάδια με ορατή ανθρώπινη συμμετοχή. Σε μια ώριμη εφαρμογή, το pipeline μπορεί να αναλάβει περισσότερο έργο: παραγωγή κώδικα, trusted tests, AI review, διόρθωση επαληθευμένων ευρημάτων και νέα αξιολόγηση. Το AI μπορεί να συντάσσει σύντομη περιγραφή PR με πραγματικά evidence από το τελευταίο run, ώστε ο άνθρωπος να εξετάζει κυρίως εξαιρέσεις και σημαντικές αποφάσεις.

Η βασική εργασία του engineer μεταφέρεται στην κατασκευή και συντήρηση αυτού του αξιόπιστου pipeline. Η ομάδα μπορεί να αυξάνει την αυτονομία για συγκεκριμένες κατηγορίες αλλαγών, όταν μετρά μικρότερο ανθρώπινο χρόνο review μαζί με διατήρηση ή βελτίωση της ποιότητας. Το παρόν lab διδάσκει τα θεμέλια· το instructor demo δείχνει αυτόματο PR review και CI με χειροκίνητο repair handoff. Η πλήρης σύνδεση repair και το auto-merge αποτελούν επόμενα βήματα. Η Tan περιγράφει [agentic review και αυτόματες διορθώσεις](https://x.com/poteto/status/2085885450468909083) και [agents που κάνουν merge](https://x.com/poteto/status/2087244771849089270) στο δικό της περιβάλλον.


## Το δωρεάν instructor demo που θα παρακολουθήσετε

Στα λεπτά 48–52 ο διδάσκων δείχνει ξεχωριστό public PR με CodeRabbit review. Παρατηρήστε αν το finding περιέχει location, απαίτηση, counterexample και evidence. Η διόρθωση και το νέο CI run αφορούν το ίδιο PR. Στο παράδειγμα το constants refactor διατηρείται, ενώ αποκαθίσταται η σειρά rounding. Η μεταφορά του finding στο implementation AI και το push γίνονται από άνθρωπο. Δεν χρειάζεται δική σας εγκατάσταση CodeRabbit για να ακολουθήσετε το lab.

Γράψτε μία πρόταση: τι πληροφορία πρόσθεσε το review πέρα από το CI failure; Αν δεν βρέθηκε πραγματικό finding, πώς θα καταγράφατε αυτό το αποτέλεσμα στην αξιολόγηση του reviewer;
