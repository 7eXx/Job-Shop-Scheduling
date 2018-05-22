import sys
from Tabu import *
from Neighborhood import *
from MoveSet import *
from Block import *
from Job import *
from Task import *
from Util import *

# Questo metodo implementa  la ricerca del miglior vicino
def neighborSearchProcedure(solution, tabu_list):

    # Trova le mosse proibite dalla soluzione attuale
    fp_moves = solution.forbittenProfittableMoves(tabu_list.moves, solution.makespan)
    print("Forbitten Profittable Moves: ")
    for m in fp_moves: print(m)

    # Trova le mosse non proibite dalle mosse nella tabu list
    u_moves = solution.unforbittenMoves(tabu_list.moves)
    print("Unforbitten Moves: ")
    for m in u_moves: print(m)

    # Unione degli insiemi delle mosse proibite e non proibite e azzera la miglior mossa
    union_fp_u = Move.unionMoves(fp_moves, u_moves)
    print("Union FP con U Moves: ")
    for m in union_fp_u: print(m)
    best_move = None

    # Se esiste almeno una mossa tra quelle non proibite scelgo la prima delle mosse e la uso per trovare una soluzione
    if len(union_fp_u) > 0:
        best_move = union_fp_u[0]
        best_solution = solution.generateNeighbor(best_move)

        # Per ciascuna mossa non proibita genera un nuovo vicino controllando che abbia un makespan migliore
        for i in  range(1,len(union_fp_u)):
            new_solution = solution.generateNeighbor(union_fp_u[i])
            if new_solution.makespan < best_solution.makespan:
                best_move = union_fp_u[i]

    # Altrimenti se la soluzione ha solo una mossa, la mossa migliore e' l'unica possibile
    elif len(solution.moves) == 1:
        best_move = solution.moves[0]

    # In caso contrario trova le mosse non proibite da tabu list
    else:
        u_moves = solution.unforbittenMoves(tabu_list.moves)

        # Finche' esiste almeno una mossa non proibita prova a trovare altre mosse non proibite
        while len(u_moves) == 0:
            tabu_list.shiftTmax()
            u_moves = solution.unforbittenMoves(tabu_list.moves)

        # La miglior mossa e' quindi la prima delle mosse rimanenti
        best_move = u_moves[0]

    # ritorna vero se la mossa è stata aggiunta alla tabu list
    move_added = tabu_list.addMoveTabu(best_move)

    # Restituisce la miglior mossa e la lista tabu
    return best_move, tabu_list


# Metodo che implementa la tabu search senza peggiorare la soluzione attuale, quindi trova un ottimo locale
def tabuSearchAlgorithmNowicki(solution, tabu_list):

    # Definisce il massimo di iterazioni e usa la soluzione parametro come ottima iniziale
    MAX_ITER = 5
    iter = 0
    opt_solution = solution

    # Finche' nella soluzione attuale esistono mosse e non sono state effettuate le iterazioni massime
    while len(opt_solution.moves) > 0 and iter < MAX_ITER:

        # Applica NSP creando la soluzione migliore tramite la mossa migliore risultante dalla NSP
        best_move, tabu_list = neighborSearchProcedure(opt_solution, tabu_list)
        new_solution = opt_solution.generateNeighbor(best_move)

        # Se il makespan della nuova soluzione e' migliore di quella ottima
        if new_solution.makespan < opt_solution.makespan:

            # Aggiornamento la soluzione considerata ottima e riporta il contatore delle iterazioni a 0
            opt_solution = new_solution
            iter = 0

        # In caso contrario aumento il contatore delle iterazioni
        else:
            iter = iter + 1

    # Restituisce la soluzione ottima (potrebbe essere un ottimo locale)
    return opt_solution


# Funzione di tabu search che permette anche mosse peggiorative
def tabuSearch(max_iter, solution, tabu_list):

    # Definisce il massimo di iterazioni e usa la soluzione parametro come ottima iniziale
    MAX_ITER = max_iter
    opt_solution = solution


    # Prepara la lista delle soluzioni candidate per l'esplorazione aggiungendo quella iniziale
    list_solutions = []
    list_solutions.append(solution)

    # Finche' ci sono soluzioni e non si raggiunge il massimo delle iterazioni
    iter = 0
    while len(list_solutions) > 0 and iter < MAX_ITER:

        # Estrae la prima soluzione e per ogni mossa in quella soluzione verifica se la mossa e' applicabile
        sol = list_solutions[0]
        for move in sol.moves:
            if not tabu_list.searchMove(move):

                # Crea la nuova soluzione e aggiunge la mossa alla lista tabu
                new_solution = sol.generateNeighbor(move)
                tabu_list.addMoveTabu(move)

                # Aggiunge la soluzione alla lista dopo aver verificato che non ci sia
                if not solutionExists(list_solutions, new_solution):
                    list_solutions.append(new_solution)

                # Aggiorna l'ottimo se migliore di quello attuale
                if new_solution.makespan < opt_solution.makespan:
                    opt_solution = new_solution
                    iter = 0
                else:
                    iter = iter + 1

        # Dopo aver provato ad applicare tutte le mosse rimuove la soluzione attuale
        list_solutions = list_solutions[1:]

    # Restituisce la soluzione ottimale
    return opt_solution


# Funzione che verifica se una soluzione esiste già nella lista
def solutionExists(list_solutions, solution):

    # Per tutte le soluzioni, in ogni macchina
    found = False
    for sol in list_solutions:
        for m in range(0, len(sol.machines)):

            # Per ogni task nella macchina
            task_b = True
            for t in range(0, len(sol.machines[m].tasks)):

                # Se il nome del task corrente fa parte della soluzione
                if not sol.machines[m].tasks[t].name == solution.machines[m].tasks[t].name:
                    task_b = False
                    break

            # Se il nome del task corrente fa parte della soluzione esci dal ciclo
            if not task_b:
                break

        # Se non ci sono task che fanno parte della soluzione imposta found a True
        if task_b:
            found = True
            break

    # Restituisce il ruolo
    return found


# Procedura che stampa la soluzione secondo una formattazione preimpostata
def printSolution(solution):
    print(str(solution))
    print("-- makespan: " + str(solution.makespan))
    print("-- ecco i percorsi critici: ")
    print(solution.strAllCriticalPaths() + "\n")
    print("-- tutti i blocchi")
    print(solution.strAllBlockSets() + "\n")
    print("-- ecco i move_sets:")
    print(solution.strAllMoveSets() + "\n")


# Procedura main
if __name__ == "__main__":

    # Esempio maggiore 4x3
    n_macchine = 4
    n_jobs = 3
    jobs_times = [[10, 8, 4],
                  [8, 3, 5, 6],
                  [4, 7, 3]]
    assegnamento_macchine = [[0, 1, 2],
                             [1, 0, 3, 2],
                             [0, 1, 3]]

    # Parametri di default
    '''
    n_macchine = 3
    n_jobs = 3
    jobs_times = [[3, 2, 2],
                  [2, 1, 4],
                  [4, 3]]
    assegnamento_macchine = [[0, 1, 2],
                             [0, 2, 1],
                             [1, 2]]
    '''

    # Inizializzazione delle strutture dati
    machines = []
    jobs_list = []

    # Inserisce i task all'interno dei job
    for i in range(0, n_jobs):
        jobs_list.append(Job(i, jobs_times[i]))

    # Creazione delle macchine
    for i in range(0, n_macchine):
        machines.append(Machine(i, []))

    # Assegnamento dei task alle macchine secondo l'assegnamento preimpostato
    for j in range(0,len(jobs_list)):
        for i in range(0,len(jobs_list[j].tasks)):
            machines[assegnamento_macchine[j][i]].addSimpleTask(jobs_list[j].tasks[i])

    # Esegue una permutazione casuale dell'ordine dei task su tutte le macchine e stampa lo stato
    for m in machines: m.randomTasks()
    for m in machines: print(m)

    # Prepara la soluzione iniziale e la stampa
    initial_solution = Solution(machines)
    print("-- SOLUZIONE INIZIALE: ")
    printSolution(initial_solution)

    # Crea il vicinato della soluzione iniziale e visualizza i vicini al primo livello
    neighborhood = initial_solution.generateNeighborhood(initial_solution.moves)
    for i in range(0, len(neighborhood.neighbors)):
        print("-- neighbor: " + str(i + 1))
        printSolution(neighborhood.neighbors[i])

    # Inizializza la tabu list, applica l'algoritmo NSP e trova una nuova soluzione applicando la mossa migliore
    tabu_list = Tabu_List()
    best_move, tabu_list = neighborSearchProcedure(initial_solution, tabu_list)
    solution_new = initial_solution.generateNeighbor(best_move)

    # Mostra il miglior vicino della soluzione iniziale assieme alla tabu list
    print("-- GENERAZIONE DEL MIGLIOR VICINO: ")
    printSolution(solution_new)
    print("Tabu List: ")
    print(tabu_list)

    # Azzera la tabu list e cerca la soluzione ottima con la tabu search senza peggioramenti mostrando la soluzione
    tabu_list = Tabu_List()
    opt_nowicki_solution = tabuSearchAlgorithmNowicki(initial_solution, tabu_list)
    print("-- SOLUZIONE OTTIMA CON TABU NOWICKI: ")
    printSolution(opt_nowicki_solution)

    # Azzera la tabu list e cerca la soluzione ottima con la tabu search con peggioramenti mostrando la soluzione
    tabu_list = Tabu_List()
    opt_solution = tabuSearch((len(jobs_list) * len(machines)) ** 2, initial_solution, tabu_list)
    print("-- SOLUZIONE OTTIMA CON TABU SEARCH: ")
    printSolution(opt_solution)

    # Print di termine esecuzione
    print("finito")