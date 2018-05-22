import copy
'''
File con tutte le funzioni e procedure che non appartengono a nessuna classe
'''


# Funzione ricorsiva che identifica il loop nel grafo ed eventualmente restituisce la lista ciclica che forma il loop
def loopDetenction(node, visited=[]):
    # Se il nodo e' gia' stato visitato
    if node in visited:

        # Trova la posizione del nodo, elimina i nodi che non sono nel ciclo e ritorna True assieme alla lista ciclica
        index = visited.index(node)
        visited = visited[index:]
        return True, visited

    # Se un nodo non e' gia' visitato
    else:

        # Aggiunge il nodo ai visitati e richiama questa funzione per il task successivo nel job e nella macchina
        visited.append(node)
        found = False
        if node.mcTask is not None and not found:
            found, visited = loopDetenction(node.mcTask, visited)
        if node.jcTask is not None and not found:
            found, visited = loopDetenction(node.jcTask, visited)

        # Elimino l'ultimo nodo dalla lista dei visitati
        if not found:
            visited = visited[:-1]

        # Restituisce il risultato con i nodi visitati
        return found, visited


# Procedura che elimina il loop dal percorso tramite inversione di un arco che collega due task nella stessa macchina
def deleteLoop(loop_path, exchanged_set):

    # Per ogni elemento del cammino considera il nodo iesimo e quello successivo
    for i in range(0, len(loop_path)):
        node_1 = loop_path[i]
        node_2 = loop_path[(i + 1) % len(loop_path)]

        # Verifica che i due nodi appartengano alla stessa macchina, in tal caso si possono invertire
        if node_1.machine == node_2.machine and (node_1, node_2) not in exchanged_set and (
        node_2, node_1) not in exchanged_set:
            node_1.machine.exchangeOrder(node_1, node_2)

            # Aggiunge i nodi all'insieme di quelli già scambiati per non scambiarli ancora in futuro
            exchanged_set.add((node_1, node_2))
            exchanged_set.add((node_2, node_1))
            break


# Procedura che analizza ed elimina i loop nel grafo
def analyzeDeleteLoop(machines):

    # Tengo in memoria gli scambi gia' eseguiti per evitare di eseguirli nuovamente
    exchanged_set = set()
    loop = True
    while loop:

        # Controllo per ogni macchina che non esistano cicli dal primo task
        c_cycle = False
        for m in machines:
            visited = []
            (c_cycle, visited) = loopDetenction(m.tasks[0], visited)
            if c_cycle:
                break

        # Se trovo un ciclo lo elimino tramite procedura deleteLoop
        if c_cycle:
            print("ciclo trovato \n")
            deleteLoop(visited, exchanged_set)

        # Se dopo aver cercato in ogni macchina non ci sono cicli allora termino la ricerca
        else:
            loop = False
            print("nessun ciclo trovato \n")


# Funzione restituisce tutti i critical path da una lista di tasks che hanno makespan maggiore
def allCriticalPaths(tasks):

    # Per tutti i task trova tutti i critical path e li salva uno ad uno in all_critical_path
    all_critical_paths = []
    for t in tasks:
        multiple_critical_paths = multipleCriticalPath(t, [], [])
        for multi_paths in multiple_critical_paths:
            all_critical_paths.append(multi_paths)

    # Per ogni path inverte l'ordine dei task trovati dato che la ricerca del critical path parte dall'ultimo task
    for crit_path in all_critical_paths:
        crit_path.reverse()

    # Ritorna tutti i critical path
    return all_critical_paths


# Funzione ricorsiva che trova tutti i critical path che hanno termine nel task nodo
def multipleCriticalPath(node, multiple_paths=[], path=[]):

    # Aggiungo il riferimento al path ai cammini multipli se il cammino e' vuoto
    if len(path) == 0:
        multiple_paths.append(path)

    # Salvo i task precedenti al task attuale
    prev_task_machine = node.mpTask
    prev_task_job = node.jpTask

    # Se esistono entrambi i task precedenti
    if prev_task_machine is not None and prev_task_job is not None:

        # Se il tempo di fine dei task precedenti e' lo stesso
        if prev_task_machine.finishTime == prev_task_job.finishTime:

            # Aggiunge il task attuale al path copiando il path attuale in modo aggiungerlo ai cammini multipli
            path.append(node)
            path_2 = copy.copy(path)
            multiple_paths.append(path_2)

            # Richiama la funzione sui due cammini che sono stati trovati
            multipleCriticalPath(prev_task_job, multiple_paths, path)
            multipleCriticalPath(prev_task_machine, multiple_paths, path_2)


        # Se il tempo di fine del task precedente di macchina e' maggiore del tempo di fine del task precedente di job
        if prev_task_machine.finishTime > prev_task_job.finishTime:

            # Aggiunge il task attuale al path e chiama la funzione sul task di macchina precedente
            path.append(node)
            multipleCriticalPath(prev_task_machine, multiple_paths, path)

        # Se il tempo di fine del task precedente di macchina e' minore del tempo di fine del task precedente di jo
        elif prev_task_machine.finishTime < prev_task_job.finishTime:

            # Aggiunge il task attuale al path e chiama la funzione sul task di job precedente
            path.append(node)
            multipleCriticalPath(prev_task_job, multiple_paths, path)

    # Altrimenti se esiste solo il task precedente di macchina
    elif prev_task_machine is not None:

        # Aggiunge il task attuale al path e chiama la funzione sul task di macchina precedente
        path.append(node)
        return multipleCriticalPath(prev_task_machine, multiple_paths, path)

    # Altrimenti se esiste solo il task precedente di job
    elif prev_task_job is not None:

        # Aggiunge il task attuale al path e chiama ricorsivamente la funzione sul task di job precedente
        path.append(node)
        return multipleCriticalPath(prev_task_job, multiple_paths, path)

    # In caso contrario, vuol dire che non ci sono task precedenti quindi aggiungo il task attuale al path
    else:
        path.append(node)

    # Restituisce i critical paths trovati
    return multiple_paths


# Funzione che date le macchine calcola i task con make span maggiore che sono schedulati per ultimi
def lastestTasks(machines):

    # Per ogni macchina salva il task che termina la sua esecuzione per ultimo
    last_task_machines = []
    for m in machines:
        last_task_machines.append(m.tasks[-1])

    # Tra gli ultimi task trova il task con tempo di fine piu' grande
    max_task = max(last_task_machines, key=lambda m: m.finishTime)

    # Verifica se ci sono piu' task che hanno tempo di fine uguale al task che termina per ultimo
    max_tasks = []
    for t in last_task_machines:
        if t.finishTime == max_task.finishTime:
            max_tasks.append(t)

    # Ritorna i task con tempo di fine piu' grande
    return max_tasks


# Procedura che aggiorna i tempi di tutti i task a partire dal task nodo
def enumerateNode(node):

    # Salvo i task precedenti al task attuale
    prev_task_machine = node.mpTask
    prev_task_job = node.jpTask

    # Se esistono i due task precedenti, lo start time del task e' il massimo del tempo di fine dei task precedenti
    if prev_task_machine is not None and prev_task_job is not None:
        node.startTime = max(prev_task_machine.finishTime, prev_task_job.finishTime)

    # Altrimenti se esiste solo il task precedente di macchina uso il suo tempo di fine come tempo di inizio del task
    elif prev_task_machine is not None:
        node.startTime = prev_task_machine.finishTime

    # Altrimenti se esiste solo il task precedente del job uso il suo tempo di fine come tempo di inizio del task
    elif prev_task_job is not None:
        node.startTime = prev_task_job.finishTime

    # Aggiorna il tempo di fine del task attuale usando il tempo di inizio + il tempo di esecuzione
    node.finishTime = node.startTime + node.executionTime

    # Se esistono task successivi nel job e nella macchina richiamo la procedura per i figli successivi
    if node.mcTask is not None:
        enumerateNode(node.mcTask)
    if node.jcTask is not None:
        enumerateNode(node.jcTask)


# Procedura che aggiorna i tempi di tutti i task di tutte le macchine
def enumerateGraph(machines):
    for m in machines:
        if len(m.tasks) > 0:
            enumerateNode(m.tasks[0])