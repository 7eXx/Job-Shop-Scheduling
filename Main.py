import sys
from Neighborhood import *
from MoveSet import *
from Task import *
from Util import *

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


class BlockSet:

    def __init__(self, critical_path):

        self.block_set = self.buildBlocks(critical_path)

    ## questo metodo dal critical path restituisce
    ## una lista di blocchi: dimensione massima per ogni macchina
    ## (per maggiori dettagli vedere teoria)
    def buildBlocks(self, critical_path):

        blocks = []
        prev_task = None
        for task in crit_path:

            ## verifica se il task precedente della macchina è nullo
            if task.mpTask is None or task.machine != prev_task.machine:
                blocks.append([task])

            else:
                blocks[-1].append(task)

            prev_task = task

        return blocks

    def __str__(self):
        stringa = "["
        for blocks in self.block_set:
            stringa += "[ "
            for task in blocks:
                stringa += task.name + " "
            stringa += "]"

        stringa += "]"
        return stringa

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

    all_critical_paths = []
    for t in tasks:
        ## torna tutti i percorsi critici associati a un task con schema [[]]
        multiple_critical_paths = multipleCriticalPath(t, [[]])
        ## per tutti i percorsi critici del task li associa a una nuova lista
        for multi_paths in multiple_critical_paths:
            all_critical_paths.append(multi_paths)

    ## struttura del tipo [[crit_path_1],[crit_path_2]] ecc
    ## raddrizza tutti i critical path
    for crit_path in all_critical_paths:
        crit_path.reverse()

    return all_critical_paths

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
    machines = []
    jobs_list = []
    
    for i in range(0, n_jobs):
        jobs_list.append(Job(i, jobs_times[i]))
        # print del job
        # print(jobs_list[i])

    ## creazione delle macchine
    for i in range(0, n_macchine):
        machines.append(Machine(i, []))

    ## assegnamento dei task alle macchine secondo il vettore
    for j in range(0,len(jobs_list)):
        for i in range(0,len(jobs_list[j].tasks)):
            ## assegnazionio dei job alle macchine in relazione al vettore di assegnamento
            machines[assegnamento_macchine[j][i]].addSimpleTask(jobs_list[j].tasks[i])

    for m in machines:
        print(m)

    for m in machines:
        m.shortestTaskFirst()

    print ("-- situazione attuale macchine")
    for m in machines:
        print(m)

    analyzeDeleteLoop(machines)

    print("-- situazione finale macchine sistemate")
    for j in jobs_list:
        print(j)

    ## esegue aggiornamento nodi
    enumerateGraph(machines)

    print("-- assegnamento start time task: \n")
    for m in machines:
        print(m)


    # calcola il makespan recuperandolo dagli ultimi task delle macchine
    lastes_tasks = lastestTask(machines)
    print("-- i tasks con maggiore makespan sono: \n")
    for t in lastes_tasks:
        print(t)

    ## ritorna una lista contente tutti i percorsi critici possibili
    all_critical_paths = allCriticalPaths(lastes_tasks)

    print("-- ecco tutti i percorsi critici:")
    print("[", end="")
    for crit_path in all_critical_paths:
        print("[ ", end="")
        for task in crit_path:
            print(task.name + " ", end="")
        print("]", end="")
    print("]\n")

    ## ora dai percorsi critici si puo' lavorare con l'algoritmo di Nowicki
    ## quindi costruzione dei blocchi in cui ogni task appartiene a una macchina
    ## struttura dal tipo [[[blocco_1_path_1][blocco_2_path_1]...], [[blocco_1_path_2][blocco_2_path_2]...]...]
    all_blocks_sets = []
    for crit_path in all_critical_paths:
        all_blocks_sets.append(BlockSet(crit_path))

    print("-- tutti i blocchi")
    ## print di tutti i blocchi
    for block_set in all_blocks_sets:
        print(block_set)


    ## costruzione del MoveSet per i blocchi
    move_sets = []
    for block_set in all_blocks_sets:
        move_set = MoveSet(block_set)
        move_sets.append(move_set)

    print("-- ecco i move_sets:")
    for move_set in move_sets:
        print(move_set)


    ## per tutti i move_set genera il neighborhood
    neighborhood = Neighborhood()
    for move_set in move_sets:
        for moves in move_set.move_set:
            if len(moves) > 0:
                for move in moves:
                    neighbor = Neighbor(machines, move)
                    neighborhood.addNeighbor(neighbor)

    print("finito")
