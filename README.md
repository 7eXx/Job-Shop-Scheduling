Ricerca Operativa
1)	formalizzare il problema tramite un modello matematico,
2)	scegliere almeno un approccio risolutivo tra quelli esaminati nel corso
3)	applicarlo alla soluzione del problema selezionato,
4)	sperimentandolo su almeno un’istanza.

Job-Shop Scheduling
un sistema di produzione è organizzato con un pool di macchine M={i1,..,im}, ciascuna dedicata esclusivamente a una data operazione, e un insieme di job J={j1,..,jn}. Ogni job j è definito da una sequenza di nj operazioni (o1m(1,j),..,oim(i,j), ..onjm(nj,j)), dove m(k,j) è la macchina preposta ad eseguire la k-esima operazione del job j. Ogni operazione ha durata djm da svolgersi sulla macchina dedicata m secondo l’ordine stabilito dalla sequenza, detto il routing del job, e che varia per ogni singolo job. Si vuole minimizzare il makespan, soggetto ai seguenti vincoli tecnici:
1)	ogni job viene processato dalle macchine richieste per le operazioni che lo compongono nell’ordine previsto dal suo routing
2)	la singola operazione una volta iniziata non può essere interrotta e poi ripresa (senza preemption),
3)	ogni macchina ad ogni istante non può svolgere più di una operazione,
4)	l’operazione i del job j può avere inizio solo quando l’operazione i-1 è stata terminata.
Si risolva il problema attraverso un algoritmo GRASP, che utilizza come intorno per la fase di ricerca locale, l’intorno proposto in “Nowicki Smutnicki, MANAGEMENT SCIENCE/VOL 40. No. 6, June 1996” (rivolgersi al docente per il file).

https://developers.google.com/optimization/scheduling/job_shop

https://github.com/gaulight42/jobshop
