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

            # crea il task e lo aggiunge alla lista delle operazioni
            t = Task(name, op_times[i])

            self.addSimpleTask(t)

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

    def addSimpleTask(self, t):

        t.setJob(self)

        if len(self.tasks) > 0:
            t.setJobParent(self.tasks[-1])
            self.tasks[-1].setJobChildren(t)

        self.tasks.append(t)


    def __str__(self):
        stringa = self.name + "\n"
        for t in self.tasks:
            stringa += str(t) + '\n'

        return stringa