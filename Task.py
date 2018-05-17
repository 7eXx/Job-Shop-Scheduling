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
                  "macchina: " + (self.machine.name if self.machine is not (None) else "(nessuna)") + "\n" + \
                  "lavoro: " + (self.job.name if self.job is not (None) else "(nessuno)") + "\n" + \
                  "task job precedente: " + (self.jpTask.name if self.jpTask is not None else "(nessuno)") +  "\n" + \
                  "task job successivo: " + (self.jcTask.name if self.jcTask is not None else "(nessuno)") + "\n" + \
                  "task macchina precedente: " + (self.mpTask.name if self.mpTask is not None else "(nessuno)") + "\n" + \
                  "task macchina successivo: " + (self.mcTask.name if self.mcTask is not None else "(nessuno)") + "\n" + \
                  "inizio: " + str(self.startTime) + "\n" +\
                  "fine: " + str(self.finishTime) + "\n" +\
                  "tempo esecuzione: " + str(self.executionTime) + "\n"
        return stringa


