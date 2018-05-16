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

    def exchangeOrder(self, t_1, t_2):

        t_1_index = self.tasks.index(t_1)
        t_2_index = self.tasks.index(t_2)

        self.tasks[t_1_index], self.tasks[t_2_index] = self.tasks[t_2_index], self.tasks[t_1_index]
        self.updateRefTasks()


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

    def shortestTaskFirst(self):

        self.tasks.sort(key=lambda task: task.executionTime,reverse=True)

        ## aggiornamento riferimenti task
        self.updateRefTasks()

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


## questo metodo identifica il loop
## ritorna una lista ciclica che forma il loop
def loopDetenction(node, visited=[]):
    if node in visited:
        # trova l'indice dell'elemento gia' analizzato
        index = visited.index(node)
        # elimina tutti quelli precedenti che non stanno nel ciclo
        visited = visited[index:]
        return (True, visited)
    else:
        visited.append(node)
        # verifica il task successivo del job
        if node.jcTask is not None:
            return loopDetenction(node.jcTask, visited)
        # verifica il task successivo della macchina
        if node.mcTask is not None:
            return loopDetenction(node.mcTask, visited)

        return (False, visited)

## questo metodo elimina il loop dal percorso
## attraverso l'inversione di un arco che collega
## due task nella stessa macchina
def deleteLoop(loop_path, exchanged_set):

    for i in range(0, len(loop_path)):
        ## verifica che i due task appartengano alla stessa macchina
        ## allora si possono invertire
        node_1 = loop_path[i]
        node_2 = loop_path[(i+1)%len(loop_path)]

        if node_1.machine == node_2.machine and (node_1, node_2) not in exchanged_set and (node_2, node_1) not in exchanged_set:

            node_1.machine.exchangeOrder(node_1, node_2)
            ## aggiunge i nodi all'insieme di quelli già scambiati per non riscambiarli
            exchanged_set.add((node_1, node_2))
            exchanged_set.add((node_2, node_1))
            break

def enumerateNode(node):

    prev_task_machine = node.mpTask
    prev_task_job = node.jpTask

    if prev_task_machine is not None and prev_task_job is not None:
        node.startTime = max(prev_task_machine.finishTime, prev_task_job.finishTime)

    elif prev_task_machine is not None:
        node.startTime = prev_task_machine.finishTime

    elif prev_task_job is not None:
        node.startTime = prev_task_job.finishTime

    node.finishTime = node.startTime + node.executionTime

    if node.mcTask is not None:
        enumerateNode(node.mcTask)

    if node.jcTask is not None:
        enumerateNode(node.jcTask)

## funzione che date le macchine
## calcola i task con make span maggiore
## che sono schedulati per ultimi
def lastestTask(machines):

    last_task_machines = []
    for m in machines:
        last_task_machines.append(m.tasks[-1])

    max_task = max(last_task_machines, key=lambda m: m.finishTime)

    ## verifica se ci sono piu' task che hanno durata uguale al max
    max_tasks = []
    for t in last_task_machines:
        if t.finishTime == max_task.finishTime:
            max_tasks.append(t)

    return max_tasks


## metodo che dai/dal task ritorna i critical path
## da una lista di tasks che hanno makespan maggiore
def allCriticalPaths(tasks):

    all_critical_path = []
    for t in tasks:
        ## torna tutti i percorsi critici associati a un task con schema [[]]
        multiple_critical_paths = multipleCriticalPath(t, [[]])
        ## per tutti i percorsi critici del task li associa a una nuova lista
        for multi_paths in multiple_critical_paths:
            all_critical_path.append(multi_paths)

    ## struttura del tipo [[crit_path_1],[crit_path_2]] ecc
    return all_critical_path

def multipleCriticalPath(node, multiple_paths=[[]]):

    prev_task_machine = node.mpTask
    prev_task_job = node.jpTask

    if prev_task_machine is not None and prev_task_job is not None:

        if prev_task_machine.finishTime == prev_task_job.finishTime:

            multiple_paths.append([node])
            return multipleCriticalPath(prev_task_machine, multiple_paths)

            multiple_paths.append([node])
            return multipleCriticalPath(prev_task_job, multiple_paths)

        if prev_task_machine.finishTime > prev_task_job.finishTime:

            multiple_paths[0].append(node)
            return multipleCriticalPath(prev_task_machine, multiple_paths)

        elif prev_task_machine.finishTime < prev_task_job.finishTime:

            multiple_paths[0].append(node)
            return multipleCriticalPath(prev_task_job, multiple_paths)

    elif prev_task_machine is not None:
        multiple_paths[0].append(node)
        return multipleCriticalPath(prev_task_machine, multiple_paths)

    elif prev_task_job is not None:
        multiple_paths[0].append(node)
        return multipleCriticalPath(prev_task_job, multiple_paths)

    else:
        multiple_paths[0].append(node)
        return multiple_paths





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

    ## creazione dei JOB
    for i in range(0, n_jobs):
        jobs_list.append(Job(i, jobs_times[i]))
        # print del job
        # print(jobs_list[i])

    ## creazione delle macchine
    for i in range(0, n_macchine):
        macchine.append(Machine(i,[]))

    ## assegnamento dei task alle macchine secondo il vettore
    for j in range(0,len(jobs_list)):
        for i in range(0,len(jobs_list[j].tasks)):
            ## assegnazionio dei job alle macchine in relazione al vettore di assegnamento
            macchine[assegnamento_macchine[j][i]].addSimpleTask(jobs_list[j].tasks[i])

    for m in macchine:
        print(m)

    for m in macchine:
        m.shortestTaskFirst()

    print ("situazione attuale macchine")
    for m in macchine:
        print(m)

    ## seguenti righe di codice cercano i loop
    ## e se ci sono cercano di eliminarli
    loop = True
    ## l'insisme degli scambi già eseguiti per non eseguire ancora gli stessi scambi
    exchanged_set = set()
    while loop:

        c_cycle = False
        ## ciclo che partendo dai task dei primi job trova eventuali cicli
        for j in jobs_list:
            visited = []
            ## partendo dal primo task di ogni job verifica se generano loop\
            (c_cycle, visited) = loopDetenction(j.tasks[0], visited)
            if c_cycle:
                break

        if c_cycle:
            print("ciclo trovato \n")
            deleteLoop(visited, exchanged_set)

        else:
            loop = False
            print("nessun ciclo trovato \n")


    print("situazione finale macchine sistemate")
    for j in jobs_list:
        print(j)


    ## aggiornamento etichette nodi, starting time e finishtime
    for m in macchine:
        enumerateNode(m.tasks[0])

    print("assegnamento start time task: \n")
    for m in macchine:
        print(m)


    # calcola il makespan recuperandolo dagli ultimi task delle macchine
    lastes_tasks = lastestTask(macchine)
    print("i tasks con maggiore makespan sono: \n")
    for t in lastes_tasks:
        print(t)

    ## ritorna una lista contente tutti i percorsi critici possibili
    all_critical_paths = allCriticalPaths(lastes_tasks)

    print("ecco tutti i percorsi critici: \n")
    for crit_path in all_critical_paths:
        for task in crit_path:
            print(task)

    ## ora dai percorsi critici si puo' lavorare con l'algoritmo di Nowicki

    print("finito")

