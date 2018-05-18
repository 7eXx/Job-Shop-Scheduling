import sys
from Neighborhood import *
from MoveSet import *
from Block import *
from Job import *
from Task import *
from Util import *



def NeighborSearchProcedure(solution, tabu_list):

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
        for move in union_fp_u:
            new_solution = solution.generateNeighbor(move)
            if new_solution.makespan < best_solution.makespan:
                best_move = move

    elif len(solution.moves) == 1:

        best_move = solution.moves[0]

    else:
        # TODO sistemare STEP 2 del'algoritmo NSP
        # utilizzare come supporto la generazione T = T +Tmax
        None

    solution_new = solution.generateNeighbor(best_move)
    tabu_list_new = tabu_list.add(best_move)

    return solution_new, tabu_list_new





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

    initial_solution = Solution(machines)

    print("-- SOLUZIONE INIZIALE: ")
    print(str(initial_solution))
    print("-- makespan: " + str(initial_solution.makespan))
    print("-- ecco i percorsi critici: ")
    print(initial_solution.strAllCriticalPaths() + "\n")
    print("-- tutti i blocchi")
    print(initial_solution.strAllBlockSets() + "\n")
    print("-- ecco i move_sets:")
    print(initial_solution.strAllMoveSets() + "\n")


    ## applicazione algoritmo NSP




    ## per tutti i move_set genera il neighborhood
    neighborhood = initial_solution.generateNeighborhood(initial_solution.all_move_sets)

    for neighbor in neighborhood.neighbors:

        print("-- neighbor: ")
        print(str(neighbor))
        print("-- makespan: " + str(neighbor.makeSpan()))
        print("-- ecco i percorsi critici: ")
        print(neighbor.strAllCriticalPaths() + "\n")
        print("-- tutti i blocchi")
        print(neighbor.strAllBlockSets() + "\n")
        print("-- ecco i move_sets:")
        print(neighbor.strAllMoveSets() + "\n")



    print("finito")
