from Task import *
'''
classe per modellare il Job
'''
class Job:

    def __init__(self, n, op_times):
        self.name = "Job_" + str(n)
        self.tasks = []

        # Per ogni tempo inserito devo creare un task
        for i in range(len(op_times)):
            name = str(n) + "_" + str(i+1)

            # Crea il task e lo aggiunge alla lista delle operazioni
            t = Task(name, op_times[i])
            self.addSimpleTask(t)


    # Metodo che inserisce un task all'interno del job aggiornando tempi e riferimenti del task
    def addTask(self, t):

        # Definisce il job del task
        t.setJob(self)

        # Aggiorna il tempo di inizio del task verificando qual e' il tempo maggiore tra i task del job e della macchina
        if len(self.tasks) > 0:
            t.setJobParent(self.tasks[-1])
            if t.mpTask is not(None):
                t.startTime = max(t.jpTask.finishTime, t.mpTask.finishTime)
            else:
                t.startTime = t.jpTask.finishTime
            t.jpTask.setJobChildren(t)

        # Aggiorna il tempo di fine del task e aggiunge il task alla lista del task del job
        t.finishTime = t.startTime + t.executionTime
        self.tasks.append(t)


    # Metodo che aggiunge il task in coda alla lista dei task aggiornando i riferimenti
    def addSimpleTask(self, t):

        # Definisce il job del task
        t.setJob(self)

        # Aggiunge il task attuale nella lista dei task aggiornando i riferimenti al padre e al figlio
        if len(self.tasks) > 0:
            t.setJobParent(self.tasks[-1])
            self.tasks[-1].setJobChildren(t)
        self.tasks.append(t)


    def __str__(self):
        stringa = self.name + "\n"
        for t in self.tasks:
            stringa += str(t) + '\n'

        return stringa