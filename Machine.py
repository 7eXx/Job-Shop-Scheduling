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

    def addSimpleTask(self,t):

        t.setMachine(self)

        if len(self.tasks) > 0:
            t.setMachineParent(self.tasks[-1])
            self.tasks[-1].setMachineChildren(t)

        self.tasks.append(t)

    ## scambia l'ordine di due task sulla macchina
    def exchangeOrder(self, t_1, t_2):

        t_1_index = self.tasks.index(t_1)
        t_2_index = self.tasks.index(t_2)

        self.tasks[t_1_index], self.tasks[t_2_index] = self.tasks[t_2_index], self.tasks[t_1_index]
        self.updateRefTasks()

    ## riaggiorna
    def updateRefTasks(self):
        # aggiornamento dei riferimenti ai nodi
        for i in range(0, len(self.tasks)):
            ## imposta il genitore
            if i > 0:
                self.tasks[i].setMachineParent(self.tasks[i - 1])
            else:
                self.tasks[i].setMachineParent(None)
            ## imposta il figlio
            if i + 1 < len(self.tasks):
                self.tasks[i].setMachineChildren(self.tasks[i + 1])
            else:
                self.tasks[i].setMachineChildren(None)

    ## ordina i task del piu' corto al piu' lungo
    def shortestTaskFirst(self):

        self.tasks.sort(key=lambda task: task.executionTime,reverse=True)

        ## aggiornamento riferimenti task
        self.updateRefTasks()

    ## pulizia degli start time
    def clearStartTime(self):
        for t in self.tasks:
            t.startTime = 0
            t.finishTime = 0

    def __str__(self):
        stringa = self.name + "\n"
        for t in self.tasks:
            stringa += str(t) + "\n"

        return stringa
