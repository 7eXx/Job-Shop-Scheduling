from Machine import *
from MoveSet import *
from Block import *
from Util import *
import copy

class Neighborhood:

    def __init__(self):
        self.neighbors = []

    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)

class Solution:

    def __init__(self, machines, move=None):

        ## crea una copia delle macchine da modificare
        self.machines = machines
        ## pulizia degli start time
        for m in self.machines:
            m.clearStartTime()

        self.move = move
        ## se la mossa non è nulla la esegue
        if self.move is not None:
            self.executeMove(self.move)

        # analizza ed elimina eventuali loop
        analyzeDeleteLoop(self.machines)

        ## aggiorno le etichette
        enumerateGraph(self.machines)

        ## recupera tutti i tasks schedulati come ultimi
        self.lastest_tasks = lastestTasks(self.machines)

        if len(self.lastest_tasks) > 0:
            self.makespan = self.lastest_tasks[0].finishTime

        ## recupera tutti i critical paths dati gli ultimi task
        self.all_critical_paths = allCriticalPaths(self.lastest_tasks)

        ## genera tutti i blockset dal
        self.all_blocks_sets = self.generateBlockSets(self.all_critical_paths)

        ## genera tutti i move_sets dai blocchi
        self.all_move_sets = self.generateMoveSets(self.all_blocks_sets)

        self.moves = self.generateMoves(self.all_move_sets)

    ## metodo per generare il vicino da una mossa
    def generateNeighbor(self, move):

        machines = copy.deepcopy(self.machines)
        return Solution(machines, move)

    ## evolve la soluzione applicando la mossa
    def evolveSolution(self, move):

        return Solution(self.machines, move)

    ## esegue
    def executeMove(self, move):

        task_1 = None
        task_2 = None

        for machine in self.machines:

            for task in machine.tasks:

                if task.name == move.task_1.name:
                    task_1 = task

                if task.name == move.task_2.name:
                    task_2 = task

        self.move = Move(task_1, task_2)

        machine = self.move.machine
        machine.exchangeOrder(task_1, task_2)

    ## generazione delle mosse proibite ma potenzialmente buone
    def forbittenProfittableMoves(self, tabu_list, makespan):

        best_fp_moves = []
        for move in self.moves:
            new_solution = self.generateNeighbor(move)
            if new_solution.makespan < makespan and Move.findMove(move, tabu_list):
                best_fp_moves.append(move)

        return best_fp_moves

    # generazione delle mosse non proibite
    def unforbittenMoves(self, tabu_list):

        u_moves = []
        for move in self.moves:
            if not(Move.findMove(move, tabu_list)):
                u_moves.append(move)

        return u_moves

    ##


    def makeSpan(self):
        return self.makespan

    ## genera tutti i blocksets
    def generateBlockSets(self, all_critical_paths):
        all_blocks_sets = []
        for crit_path in all_critical_paths:
            block_set = BlockSet(crit_path)
            all_blocks_sets.append(block_set)

        return all_blocks_sets

    ## genera tutti gli insiemi delle mosse dai
    def generateMoveSets(self, all_blocks_sets):

        all_move_sets = []
        for block_set in all_blocks_sets:
            move_set = MoveSet(block_set)
            all_move_sets.append(move_set)

        return all_move_sets

    ## dalla lista di liste delle mosse
    ## genera una lista complessiva con tutte le mosse
    ## quindi unica per tutti i critical path
    def generateMoves(self, all_move_sets):

        moves = []
        for move_set in all_move_sets:
            for move in move_set.move_set:
                if not(Move.findMove(move, moves)):
                    moves.append(move)
        return moves

    ## da usare con parsimonia
    ## dal vicino attuale prova a generare tutti i sottovicini
    def generateNeighborhood(self, move_set):

        neighborhood = Neighborhood()
        for move in move_set:
            neighbor = self.generateNeighbor(move)
            neighborhood.addNeighbor(neighbor)

        return neighborhood


    ## metodo per ritornare la rappresentazione dei percorsi critici
    def strAllCriticalPaths(self):
        stringa = "["
        for crit_path in self.all_critical_paths:
            stringa += "[ "
            for task in crit_path:
                stringa += task.name + " "
            stringa += "]"
        stringa += "]"

        return  stringa

    ## metodo per ritornare la rappresentazione dei blocchi
    def strAllBlockSets(self):

        stringa = ""
        ## print di tutti i blocchi
        for block_set in self.all_blocks_sets:
            stringa += str(block_set)

        return stringa

    ## stringa con tutt
    def strAllMoveSets(self):

        stringa = ""
        for move_set in self.all_move_sets:
            stringa += str(move_set)

        return stringa

    def strMoves(self):
        stringa = "["
        for m in self.moves:
            stringa += str(m)
        stringa += "]"

        return stringa

    def __str__(self):
        stringa = ""
        for m in self.machines:
            stringa += str(m) + "\n"

        return stringa


