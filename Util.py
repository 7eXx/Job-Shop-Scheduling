import copy
## questo metodo identifica il loop
## ritorna una lista ciclica che forma il loop
def loopDetenction(node, visited=[]):
    if node in visited:
        # trova l'indice dell'elemento gia' analizzato
        index = visited.index(node)
        # elimina tutti quelli precedenti che non stanno nel ciclo
        visited = visited[index:]
        return True, visited

    else:
        visited.append(node)
        found = False
        # verifica il task successivo del job
        if node.jcTask is not None and not found:
            found, visited =  loopDetenction(node.jcTask, visited)
        # verifica il task successivo della macchina
        if node.mcTask is not None and not found:
            found, visited =  loopDetenction(node.mcTask, visited)

        if not found:
            visited = visited[:-1]

        return found, visited

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

def analyzeDeleteLoop(machines):
    ## seguenti righe di codice cercano i loop
    ## e se ci sono cercano di eliminarli
    loop = True
    ## l'insisme degli scambi già eseguiti per non eseguire ancora gli stessi scambi
    exchanged_set = set()
    while loop:

        c_cycle = False
        ## ciclo che partendo dai task dei primi job trova eventuali cicli
        for m in machines:
            visited = []
            ## partendo dal primo task di ogni job verifica se generano loop\
            (c_cycle, visited) = loopDetenction(m.tasks[0], visited)
            if c_cycle:
                break

        if c_cycle:
            # print("ciclo trovato \n")
            deleteLoop(visited, exchanged_set)

        else:
            loop = False
            # print("nessun ciclo trovato \n")


## metodo che dai/dal task ritorna i critical path
## da una lista di tasks che hanno makespan maggiore
def allCriticalPaths(tasks):
    all_critical_paths = []
    for t in tasks:
        ## torna tutti i percorsi critici associati a un task con schema [[]]
        multiple_critical_paths = multipleCriticalPath(t, [], [])
        ## per tutti i percorsi critici del task li associa a una nuova lista
        for multi_paths in multiple_critical_paths:
            all_critical_paths.append(multi_paths)

    ## struttura del tipo [[crit_path_1],[crit_path_2]] ecc
    ## raddrizza tutti i critical path
    for crit_path in all_critical_paths:
        crit_path.reverse()

    return all_critical_paths


def multipleCriticalPath(node, multiple_paths=[], path=[]):

    if (len(path) == 0):
        multiple_paths.append(path)

    prev_task_machine = node.mpTask
    prev_task_job = node.jpTask

    if prev_task_machine is not None and prev_task_job is not None:

        if prev_task_machine.finishTime == prev_task_job.finishTime:

            path.append(node)

            path_2 = copy.copy(path)
            multiple_paths.append(path_2)

            multipleCriticalPath(prev_task_job, multiple_paths, path)
            multipleCriticalPath(prev_task_machine, multiple_paths, path_2)

        if prev_task_machine.finishTime > prev_task_job.finishTime:

            path.append(node)
            multipleCriticalPath(prev_task_machine, multiple_paths, path)

        elif prev_task_machine.finishTime < prev_task_job.finishTime:

            path.append(node)
            multipleCriticalPath(prev_task_job, multiple_paths, path)

    elif prev_task_machine is not None:
        path.append(node)
        multipleCriticalPath(prev_task_machine, multiple_paths, path)

    elif prev_task_job is not None:
        path.append(node)
        multipleCriticalPath(prev_task_job, multiple_paths, path)

    else:
        path.append(node)

    return multiple_paths


## funzione che date le macchine
## calcola i task con make span maggiore
## che sono schedulati per ultimi
def lastestTasks(machines):

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


## riesegue buona enumerazione dei nodi secondo l'espolarzione
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


## procedura aggiornamento nodi
def enumerateGraph(machines):

    for m in machines:
        if len(m.tasks) > 0:
            enumerateNode(m.tasks[0])


