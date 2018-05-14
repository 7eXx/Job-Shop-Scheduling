import sys

'''
classe per modellare l'operazione
'''


class Task:

    def __init__(self, n, eTime, pTask=None, cTask=None):
        self.name = "task_" + str(n)
        self.machine = None
        self.executionTime = eTime
        self.startTime = 0
        self.finishTime = 0
        self.pTask = pTask
        self.cTask = cTask

    def setParent(self, task):
        self.pTask = task

    def setChildren(self, task):
        self.cTask = task

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

    ## metodo per aggiungere un task alla macchina
    ## viene verificato
    def addTask(self, t):

        t.setMachine(self)

        # aggiornamento dei tempi
        # verifica quale è il maggiore tra
        # l'operazione sul job e sulla macchina

        if t.pTask is not None and len(self.tasks) > 0:
            if t.pTask.finishTime < self.tasks[-1].finishTime:
                t.startTime = self.tasks[-1].finishTime
            else:
                t.startTime = t.pTask.finishTime

        ## TODO implementare gli altri casi

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

            # Se sto inserendo il primo task nel job calcolo i tempi
            if i == 0:
                t.startTime = 0
                t.finishTime = t.startTime + t.executionTime

            # Se ci sono già altri task nel Job aggiorno la parentela e calcolo i tempi
            #TODO capire se è giusto calcolare in questo momento i tempi di esecuzione o se vanno scelti quando si assegna il task alla macchina
            else:
                t.setParent(self.tasks[-1])
                self.tasks[-1].setChildren(t)
                t.startTime = self.tasks[-1].finishTime
                t.finishTime = t.startTime + t.executionTime

            # Aggiungo il task appena creato alla lista del task del Job
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
        macchine.append(Machine(i, []))
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
    # TODO Capire come aggiornare i tempi all'interno delle tramite ordinamento dei task