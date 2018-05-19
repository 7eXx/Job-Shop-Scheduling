'''
classe per modellare la macchina
'''
class Machine:

    def __init__(self, n, tasks=[]):
        self.name = "Machine_" + str(n)
        self.tasks = tasks

        # Imposta la macchina per tutti i task nella lista dei task
        for t in tasks:
            t.setMachine(self)


    # Metodo che aggiunge un task alla macchina aggiornando i tempi di inizio e fine dei task della macchina
    def addTask(self, t):

        # Imposta la macchina del task
        t.setMachine(self)

        # Aggiorna il tempo di inizio del task verificando qual e' il tempo maggiore tra i task del job e della macchina
        if len(self.tasks) > 0:
            t.setMachineParent(self.tasks[-1])
            if t.jpTask is not(None):
                t.startTime = max(t.jpTask.finishTime, t.mpTask.finishTime)
            else:
                t.startTime = t.mpTask.finishTime
            t.mpTask.setMachineChildren(t)

        # Aggiorna il tempo di fine del task e aggiunge il task alla lista del task della macchina
        t.finishTime = t.startTime + t.executionTime
        self.tasks.append(t)


    # Metodo che aggiunge un task in fondo alla lista dei task
    def addSimpleTask(self,t):

        # Imposta la macchina del task
        t.setMachine(self)

        # Aggiunge il task attuale nella lista dei task aggiornando i riferimenti al padre e al figlio
        if len(self.tasks) > 0:
            t.setMachineParent(self.tasks[-1])
            self.tasks[-1].setMachineChildren(t)
        self.tasks.append(t)


    # Metodo che scambia l'ordine di due task sulla macchina
    def exchangeOrder(self, t_1, t_2):

        # Trova la posizione dei due task all'interno della lista dei task
        t_1_index = self.tasks.index(t_1)
        t_2_index = self.tasks.index(t_2)

        # Scambia i due task all'interno della lista e richiama l'aggiornamento dei riferimenti
        self.tasks[t_1_index], self.tasks[t_2_index] = self.tasks[t_2_index], self.tasks[t_1_index]
        self.updateRefTasks()


    # Metodo che aggiorna i riferimenti dei task in base all'ordine con cui compaiono nella lista dei task
    def updateRefTasks(self):

        # Scorre la lista dei task e per ogni task
        for i in range(0, len(self.tasks)):

            # Imposta il genitore
            if i > 0:
                self.tasks[i].setMachineParent(self.tasks[i - 1])
            else:
                self.tasks[i].setMachineParent(None)

            # Imposta il figlio
            if i + 1 < len(self.tasks):
                self.tasks[i].setMachineChildren(self.tasks[i + 1])
            else:
                self.tasks[i].setMachineChildren(None)


    # Metodo che ordina i task dal piu' corto al piu' lungo
    def shortestTaskFirst(self):

        # Ordina i task all'interno della lista posizionando prima i task piu' corti e aggiorna i riferimenti
        self.tasks.sort(key=lambda task: task.executionTime,reverse=True)
        self.updateRefTasks()


    # Metodo che azzera gli start time di tutti i task della macchina
    def clearStartTime(self):
        for t in self.tasks:
            t.startTime = 0
            t.finishTime = 0


    def __str__(self):
        stringa = self.name + "\n"
        for t in self.tasks:
            stringa += str(t) + "\n"

        return stringa