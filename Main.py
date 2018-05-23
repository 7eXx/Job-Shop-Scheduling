import sys
from Tabu import *
from Neighborhood import *
from MoveSet import *
from Block import *
from Job import *
from Task import *
from Util import *

## questo metodo implementa  la ricerca del miglior vicino
def neighborSearchProcedure(solution, tabu_list):

    fp_moves = solution.forbittenProfittableMoves(tabu_list.moves, solution.makespan)
    print("Forbitten Profittable Moves: ")
    for m in fp_moves: print(m)

    u_moves = solution.unforbittenMoves(tabu_list.moves)
    print("Unforbitten Moves: ")
    for m in u_moves: print(m)

    ## unione insiemi di fp_moves e u_moves
    union_fp_u = Move.unionMoves(fp_moves, u_moves)
    print("Union FP con U Moves: ")
    for m in union_fp_u: print(m)

    best_move = None
    if len(union_fp_u) > 0:
        best_move = union_fp_u[0]
        best_solution = solution.generateNeighbor(best_move)
        for i in  range(1,len(union_fp_u)):
            new_solution = solution.generateNeighbor(union_fp_u[i])
            if new_solution.makespan < best_solution.makespan:
                best_move = union_fp_u[i]

    elif len(solution.moves) == 1:

        best_move = solution.moves[0]

    else:

        u_moves = solution.unforbittenMoves(tabu_list.moves)
        while len(u_moves) == 0:
            tabu_list.shiftTmax()
            u_moves = solution.unforbittenMoves(tabu_list.moves)

        best_move = u_moves[0]

    ## ritorna vero se la mossa è stata aggiunta alla tabu list
    move_added = tabu_list.addMoveTabu(best_move)

    ## TODO far tornare anche il nuovo makespan se migliore del precedente
    return best_move, tabu_list


def tabuSearchAlgorithmNowicki(solution, tabu_list):

    MAX_ITER = 5
    iter = 0
    ## imposta soluzione ricevuta come ottima
    opt_solution = solution

    while len(opt_solution.moves) > 0 and iter < MAX_ITER:

        ## applicazione NSP
        best_move, tabu_list = neighborSearchProcedure(opt_solution, tabu_list)
        ## crea la nuova soluzione
        new_solution = opt_solution.generateNeighbor(best_move)
        # se il makespan della nuova soluzione è migliore di quella ottima
        if new_solution.makespan < opt_solution.makespan:
            ## aggiornamento della soluzione
            opt_solution = new_solution
            ## iteratore viene riportato a 0
            iter = 0
        else:
            ## altrimenti incremento iteratore
            iter = iter + 1

    ## ritorno soluzione ottima
    return opt_solution

## tabu search che permette anche mosse peggiorative
def tabuSearch(max_iter, solution, tabu_list):

    ## massimo iterazioni
    MAX_ITER = max_iter
    # soluzione ottima iniziale
    opt_solution = solution
    # lista soluzioni candidate per l'esplorazione
    list_solutions = []
    list_solutions.append(solution)
    ## contatore iterazioni
    iter = 0
    while len(list_solutions) > 0 and iter < MAX_ITER:

        # estrae la prima soluzione
        sol = list_solutions[0]
        ## per tutte le mosse di ogni soluzione
        for move in sol.moves:
            ## verifica se la mossa è applicabile
            if not tabu_list.searchMove(move):
                # crea la nuova soluzione
                new_solution = sol.generateNeighbor(move)
                # aggiunge la mossa alla lista tabu
                tabu_list.addMoveTabu(move)
                # aggiunge la soluzione alla lista dopo aver verificato che non ci sia
                if not solutionExists(list_solutions, new_solution):
                    list_solutions.append(new_solution)
                # aggiorna l'ottimo se migliore di quello attuale
                if new_solution.makespan < opt_solution.makespan:
                    opt_solution = new_solution
                    iter = 0
                else:
                    iter = iter + 1



        ## dopo aver provato ad applicare tutte le mosse
        ## rimuove la soluzione attuale
        list_solutions = list_solutions[1:]

    return opt_solution

## metodo per verificare se una soluzione esiste già nella lista
def solutionExists(list_solutions, solution):

    found = False
    for sol in list_solutions:
        # per tutte le macchine
        for m in range(0, len(sol.machines)):

            task_b = True
            for t in range(0, len(sol.machines[m].tasks)):

                if not sol.machines[m].tasks[t].name == solution.machines[m].tasks[t].name:
                    task_b = False
                    break

            if not task_b:
                break

        if task_b:
            found = True
            break

    return found

def printSolution(solution):

    print(str(solution))
    print("-- makespan: " + str(solution.makespan))
    print("-- ecco i percorsi critici: ")
    print(solution.strAllCriticalPaths() + "\n")
    print("-- tutti i blocchi")
    print(solution.strAllBlockSets() + "\n")
    print("-- ecco i move_sets:")
    print(solution.strAllMoveSets() + "\n")


if __name__ == "__main__":

    # Parametri di default
    n_macchine = 4
    n_jobs = 3
    jobs_times = [[10, 8, 4],
                  [8, 3, 5, 6],
                  [4, 7, 3]]
    assegnamento_macchine = [[0, 1, 2],
                             [1, 0, 3, 2],
                             [0, 1, 3]]

    '''
    ## esempio maggiore 4x3
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

    '''
    ## secondo esempio 4x3
    machines[0].tasks[0], machines[0].tasks[1], machines[0].tasks[2] = machines[0].tasks[1], machines[0].tasks[2], machines[0].tasks[0]
    machines[1].tasks[0], machines[1].tasks[1], machines[1].tasks[2] = machines[1].tasks[1], machines[1].tasks[2], machines[1].tasks[0]
    machines[2].tasks[0], machines[2].tasks[1] = machines[2].tasks[0], machines[2].tasks[1]
    machines[3].tasks[0], machines[3].tasks[1] = machines[3].tasks[1], machines[3].tasks[0]
    '''

    '''
    # Assegnamento di prova per multiple critical path
    machines[0].tasks.insert(0, machines[0].tasks[-1])
    machines[0].tasks = machines[0].tasks[:-1]
    machines[1].tasks.insert(0, machines[1].tasks[-1])
    machines[1].tasks = machines[1].tasks[:-1]
    machines[2].tasks.insert(0, machines[2].tasks[-1])
    machines[2].tasks = machines[2].tasks[:-1]
    
    # Assegnamento di prova per valutare condizione erronea
    machines[1].tasks[0], machines[1].tasks[1] = machines[1].tasks[1], machines[1].tasks[0]
    machines[1].tasks[1], machines[1].tasks[2] = machines[1].tasks[2], machines[1].tasks[1]
    '''

    # for m in machines: m.randomTasks()
    for m in machines: m.updateRefTasks()
    for m in machines: print(m)

    initial_solution = Solution(machines)

    print("-- SOLUZIONE INIZIALE: ")
    printSolution(initial_solution)

    ## visualizza i vicini al primo livello
    neighborhood = initial_solution.generateNeighborhood(initial_solution.moves)

    for i in range(0, len(neighborhood.neighbors)):
        print("-- neighbor: " + str(i+1))
        printSolution(neighborhood.neighbors[i])

    ## lista tabu iniziale
    tabu_list = Tabu_List()

    ## applicazione algoritmo NSP
    best_move, tabu_list = neighborSearchProcedure(initial_solution, tabu_list)
    ## nuova soluzione applicando la best move
    solution_new = initial_solution.generateNeighbor(best_move)

    print("-- GENERAZIONE DEL MIGLIOR VICINO: ")
    printSolution(solution_new)

    print("Tabu List: ")
    print(tabu_list)

    ## ricerca soluzione migliore con tabu search
    tabu_list = Tabu_List()
    opt_nowicki_solution = tabuSearchAlgorithmNowicki(initial_solution, tabu_list)

    print("-- SOLUZIONE OTTIMA CON TABU NOWICKI: ")
    printSolution(opt_nowicki_solution)


    ## ricerca soluzione migliore con tabu search
    tabu_list = Tabu_List()
    opt_solution = tabuSearch((len(jobs_list) * len(machines))**2, initial_solution, tabu_list)

    print("-- SOLUZIONE OTTIMA CON TABU SEARCH: ")
    printSolution(opt_solution)

    print("finito")

