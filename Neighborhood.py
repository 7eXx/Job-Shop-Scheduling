from Machine import *
from MoveSet import *
from Block import *
from Util import *
import copy

'''
Classe per modellare il vicinato 
'''
class Neighborhood:

    def __init__(self):
        self.neighbors = []


    # Metodo che aggiunge un vicino alla lista dei vicini
    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)


'''
Classe per modellare la soluzione 
'''
class Solution:

    def __init__(self, machines, move=None):

        # Copia il riferimento delle macchine da modificare azzerando gli start time di tutti i task
        self.machines = machines
        for m in self.machines:
            m.clearStartTime()

        # Salva la mossa e se non e' nulla la esegue
        self.move = move
        if self.move is not None:
            self.executeMove(self.move)

        # Analizza ed elimina eventuali loop aggiornando le etichette (i tempi di tutti i task)
        analyzeDeleteLoop(self.machines)
        enumerateGraph(self.machines)

        # Recupera tutti i tasks schedulati come ultimi trovando il makespan maggiore
        self.lastest_tasks = lastestTasks(self.machines)
        if len(self.lastest_tasks) > 0:
            self.makespan = self.lastest_tasks[0].finishTime

        # Recupera tutti i critical paths dati gli ultimi task e li usa per generare tutti i blockset
        self.all_critical_paths = allCriticalPaths(self.lastest_tasks)
        self.all_blocks_sets = self.generateBlockSets(self.all_critical_paths)

        # Genera tutti i movesets da tutti i blocchi e genera tutte le mosse dai movesets
        self.all_move_sets = self.generateMoveSets(self.all_blocks_sets)
        self.moves = self.generateMoves(self.all_move_sets)


    # Metodo restituisce un vicino della mossa
    def generateNeighbor(self, move):

        # Crea una copia completa delle macchine e crea il nuovo vicino
        machines = copy.deepcopy(self.machines)
        return Solution(machines, move)


    # Metodo restituisce una evoluzione della soluzione applicando la mossa
    def evolveSolution(self, move):
        return Solution(self.machines, move)


    # Metodo che esegue la mossa
    def executeMove(self, move):

        # Variabili temporanee utilizzate come riferimento ai task task da spostare
        task_1 = None
        task_2 = None

        # Per ogni task di ogni macchina
        for machine in self.machines:
            for task in machine.tasks:

                # Cerca i task in base al nome e ne salva i riferimenti
                if task.name == move.task_1.name:
                    task_1 = task
                if task.name == move.task_2.name:
                    task_2 = task

        # Salva i task da muovere e li scambia
        self.move = Move(task_1, task_2)
        machine = self.move.machine
        machine.exchangeOrder(task_1, task_2)


    # Metodo che genera le mosse proibite ma potenzialmente buone
    def forbittenProfittableMoves(self, tabu_list, makespan):

        # Per ciascuna mossa genera un vicino
        best_fp_moves = []
        for move in self.moves:
            new_solution = self.generateNeighbor(move)

            # Se il makespan della nuova soluzione e' minore del makespan e se la mossa non e' nella tabu_list
            if new_solution.makespan < makespan and Move.findMove(move, tabu_list):

                # Aggiunge la mossa tra le migliori mosse proibite
                best_fp_moves.append(move)

        # Restituisce le migliori mosse proibite
        return best_fp_moves


    # Metodo che genera le mosse non proibite
    def unforbittenMoves(self, tabu_list):

        # Per tutte le mosse della soluzione trova le mosse che non fanno parte della tabu_list e le restituisce
        u_moves = []
        for move in self.moves:
            if not(Move.findMove(move, tabu_list)):
                u_moves.append(move)
        return u_moves


    # Metodo che genera tutti i blocksets da tutti i critical path
    def generateBlockSets(self, all_critical_paths):

        # Per tutti i critical path trova tutti i blockset e li restituisce
        all_blocks_sets = []
        for crit_path in all_critical_paths:
            block_set = BlockSet(crit_path)
            all_blocks_sets.append(block_set)
        return all_blocks_sets


    # Metodo genera tutti gli insiemi delle mosse da tutti i blockset
    def generateMoveSets(self, all_blocks_sets):

        # Per tutti i blockset trova tutti i moveset e li restituisce
        all_move_sets = []
        for block_set in all_blocks_sets:
            move_set = MoveSet(block_set)
            all_move_sets.append(move_set)
        return all_move_sets


    # Metodo che genera tutte le mosse a partire da tutti i moveset, questa lista e' unica per ogni critical path
    def generateMoves(self, all_move_sets):

        # Per tutti i moveset trova tutte le mosse e le restituisce
        moves = []
        for move_set in all_move_sets:
            for move in move_set.move_set:
                if not(Move.findMove(move, moves)):
                    moves.append(move)
        return moves


    # Metodo che dalla soluzione attuale prova a generare il vicinato
    def generateNeighborhood(self, move_set):

        # Da ogni mossa nel moveset genera le soluzioni, le aggiunge al vicinato e lo restituisce
        neighborhood = Neighborhood()
        for move in move_set:
            neighbor = self.generateNeighbor(move)
            neighborhood.addNeighbor(neighbor)
        return neighborhood


    # Metodo che crea la rappresentazione di tutti i percorsi critici e la inserisce in una stringa che restituisce
    def strAllCriticalPaths(self):
        stringa = "["
        for crit_path in self.all_critical_paths:
            stringa += "[ "
            for task in crit_path:
                stringa += task.name + " "
            stringa += "]"
        stringa += "]"
        return  stringa


    # Metodo che crea la rappresentazione di tutti i blocchi e la inserisce in una stringa che restituisce
    def strAllBlockSets(self):
        stringa = ""
        ## print di tutti i blocchi
        for block_set in self.all_blocks_sets:
            stringa += str(block_set)
        return stringa


    # Metodo che crea la rappresentazione di tutti i moveset e la inserisce in una stringa che restituisce
    def strAllMoveSets(self):
        stringa = ""
        for move_set in self.all_move_sets:
            stringa += str(move_set)
        return stringa


    # Metodo che crea la rappresentazione di tutte le mosse e la inserisce in una stringa che restituisce
    def strMoves(self):
        stringa = "["
        for m in self.moves:
            stringa += str(m)
        stringa += "]"
        return stringa


    # Metodo che restituisce il valore di makespan della soluzione
    def makeSpan(self):
        return self.makespan


    def __str__(self):
        stringa = ""
        for m in self.machines:
            stringa += str(m) + "\n"

        return stringa