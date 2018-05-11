
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
        stringa = ""
        stringa = "nome: " + self.name + "\n"
        stringa += "macchina: " + (self.machine.name if self.machine is not(None) else "(nessuna)") + "\n"
        stringa += "inizio: " + str(self.startTime) + "\n"
        stringa += "fine: " + str(self.finishTime) + "\n"
        stringa += "tempo esecuzione: " + str(self.executionTime) + "\n"
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
    def addTask (self, t):

        t.setMachine(self)

        # aggiornamento dei tempi
        # verifica quale è il maggiore tra
        # l'operazione sul job e sulla macchina

        if t.pTask is not(None) and len(self.tasks) > 0:
            if t.pTask.finishTime < self.tasks[-1].finishTime:
                t.startTime = self.tasks[-1].finishTime
            else:
                t.startTime = t.pTask.finishTime

        ## TODO implementare gli altri casi

        t.finishTime = t.startTime + t.executionTime

        self.tasks.append(t)


    def __str__(self):
        stringa = ""
        for t in self.tasks:
            stringa += str(t) + "\n"

        return stringa


class Job:

    def __init__(self, n, op_times):
        self.name = "Job_" + str(n)
        self.tasks = []

        for i in range(len(op_times)):

            name = str(n) + "_" + str(i)

            # crea il task e lo aggiunge alla lista delle operazioni
            t = Task(name, op_times[i])

            if i == 0:
                t.startTime = 0
                t.finishTime = t.startTime + t.executionTime

            else:
                t.setParent(self.tasks[-1])
                t.startTime = self.tasks[-1].finishTime
                t.finishTime = t.startTime + t.executionTime

            if i > 0:
                self.tasks[-1].setChildren(t)

            self.tasks.append(t)

    def __str__(self):
        stringa = self.name + "\n"
        for t in self.tasks:
            stringa += str(t) + '\n'

        return stringa


if __name__ == "__main__":

    n_macchine = 3
    n_jobs = 3

    jobs_times =   [[3,2,2],
                    [2,1,4],
                    [1,2]]

    '''
    # test macchina con task
    t_1 = Task(1, 10, None, None)
    t_2 = Task(2, 20, None, None)
    t_3 = Task(3, 30, None, None)

    tasks = []
    tasks.append(t_1)
    tasks.append(t_2)
    tasks.append(t_3)

    machine_1 = Machine(1, tasks)
    print(machine_1)
    '''

    ## aggiunta dei tempi ai jobs
    for i in range(len(jobs_times)):
        job = Job(str(i),jobs_times[i])
        print(job)

    # TODO assegnare alle macchine i task dei job e controllare il ricalcolo dei tempi

