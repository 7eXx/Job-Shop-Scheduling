from Machine import *
from MoveSet import *
from Util import *
import copy

class Neighborhood:

    def __init__(self):
        self.neighbors = []

    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)

class Neighbor:

    def __init__(self, machines, move):

        self.machines = copy.deepcopy(machines)

        ## pulizia degli start time
        for m in self.machines:
            m.clearStartTime()

        self.move = move
        self.executeMove()
        # analizza ed elimina eventuali loop
        analyzeDeleteLoop(self.machines)

        ## aggiorno le etichette
        enumerateGraph(self.machines)


    def executeMove(self):

        task_1 = None
        task_2 = None

        for machine in self.machines:

            for task in machine.tasks:

                if task.name == self.move.task_1.name:
                    task_1 = task

                if task.name == self.move.task_2.name:
                    task_2 = task

        machine = task_1.machine
        machine.exchangeOrder(task_1, task_2)



