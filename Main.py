import sys

'''
classe per modellare l'operazione
'''


class Task:

    def __init__(self, n, eTime, jpTask=None, jcTask=None, mpTask=None, mcTask=None):
        self.name = "task_" + str(n)

        self.executionTime = eTime
        self.startTime = 0
        self.finishTime = 0


        ## imposta l'ordine padre e figlio sul lavoro
        self.jpTask = jpTask
        self.jcTask = jcTask
        self.job = None

        ## imposta l'ordine padre figlio sulla macchina
        self.mpTask = mpTask
        self.mcTask = mcTask
        self.machine = None

    def setJobParent(self, task):
        self.jpTask = task

    def setJobChildren(self, task):
        self.jcTask = task

    def setJob(self, job):
        self.job = job

    def setMachineParent(self, task):
        self.mpTask = task

    def setMachineChildren(self,task):
        self.mcTask = task

    def setMachine(self, machine):
        self.machine = machine


    def __str__(self):
        stringa = "nome: " + self.name + "\n" +\
                  "macchina: " + (self.machine.name if self.machine is not (None) else "(nessuna)") + "\n" +\
                  "inizio: " + str(self.startTime) + "\n" +\
                  "fine: " + str(self.finishTime) + "\n" +\
                  "tempo esecuzione: " + str(self.executionTime) + "\n"
        return stringa


'''
classe per modellare la macchina
'''


class Machine:

    def __init__(self, n, tasks=[]):
        self.name = "Machine_" + str(n)
        self.tasks = tasks

        for t in tasks:
            t.setMachine(self)

        ## TODO calcolare i tempi finali

    ## metodo per aggiungere un task alla macchina
    ## in questo modo si assegna un ordinamento alle operazioni sulla macchina
    def addTask(self, t):

        t.setMachine(self)

        # aggiornamento dei tempi
        # verifica quale è il maggiore tra
        # l'operazione sul job e sulla macchina
        if len(self.tasks) > 0:
            t.setMachineParent(self.tasks[-1])
            if t.jpTask is not(None):
                t.startTime = max(t.jpTask.finishTime, t.mpTask.finishTime)
            else:
                t.startTime = t.mpTask.finishTime
            t.mpTask.setMachineChildren(t)

        t.finishTime = t.startTime + t.executionTime

        self.tasks.append(t)

    def __str__(self):
        stringa = self.name + "\n"
        for t in self.tasks:
            stringa += str(t) + "\n"

        return stringa


'''
classe per modellare il Job
'''
class Job:

    def __init__(self, n, op_times):
        self.name = "Job_" + str(n)
        self.tasks = []

        # Per ogni tempo inserito devo creare un task
        for i in range(len(op_times)):
            name = str(n) + "_" + str(i)

            # crea il task e lo aggiunge alla lista delle operazioni
            t = Task(name, op_times[i])

            self.addTask(t)

    def addTask(self, t):

        t.setJob(self)

        # aggiornamento dei tempi
        # verifica quale è il maggiore tra
        # l'operazione sul job e sulla macchina
        if len(self.tasks) > 0:
            t.setJobParent(self.tasks[-1])
            if t.mpTask is not(None):
                t.startTime = max(t.jpTask.finishTime, t.mpTask.finishTime)
            else:
                t.startTime = t.jpTask.finishTime
            t.jpTask.setJobChildren(t)

        t.finishTime = t.startTime + t.executionTime

        self.tasks.append(t)


    def __str__(self):
        stringa = self.name + "\n"
        for t in self.tasks:
            stringa += str(t) + '\n'

        return stringa


if __name__ == "__main__":

    # Parametri di default
    n_macchine = 3
    n_jobs = 3
    jobs_times = [[3, 2, 2],
                  [2, 1, 4],
                  [4, 3]]
    assegnamento_macchine = [[0, 1, 2],
                             [0, 2, 1],
                             [1, 2]]

    # Inizializzazione delle strutture dati
    macchine = []
    jobs_list = []
    for i in range(0, n_macchine):
        macchine.append(Machine(i,[]))
    for i in range(0, n_jobs):
        jobs_list.append(Job(i, jobs_times[i]))

    ''''# Stampa di prova
    for job in jobs_list:
        print(job)'''

    # Inserimento dei task dei Job nelle varie macchine secondo l'assegnamento impostato
    for i in range(0, n_jobs):
        for j in range(0, len(assegnamento_macchine[i])):
            macchine[assegnamento_macchine[i][j]].addTask(jobs_list[i].tasks[j])
            print("Selezionata macchina = " + macchine[assegnamento_macchine[i][j]].name + " " +
                  "selezionato task = " + jobs_list[i].tasks[j].name + " " +
                  "task nella macchina al momento = " + str(len(macchine[assegnamento_macchine[i][j]].tasks)))

    # Controllo se ogni oggetto nella lista macchine è diverso dagli altri (se non si referenzia lo stesso oggetto)
    if macchine[0] is macchine[1] or macchine[0] is macchine[2] or macchine[1] is macchine[2]:
        print("Errore! gli oggetti nella lista macchine sono gli sessi")
    else:
        print("Gli oggetti sono diversi, OK!")

    # Controllo se la lista dei task è diversa per ogni macchina (devono essere diverse)
    if set(macchine[0].tasks) == set(macchine[1].tasks) == set(macchine[2].tasks):
        print("Errore! tutte le macchine hanno gli stessi task")
    else:
        print("Tutto ok")
    # TODO capire perchè se le macchine sono oggetti diversi hanno la stessa identica lista di tasks come dimostrato da print precedenti