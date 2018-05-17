
class MoveSet:

    def __init__(self, block_set):

        self.block_set = block_set
        self.move_set = self.buildMoves()

    ## questo metodo crea l'insieme delle operazioni scambiabili
    def buildMoves(self):
        moves = []
        ## per ogni blocco
        if len(self.block_set.block_set) > 1:

            ## verifica che almeno un blocco abbia dimensione maggiore di 1
            verified = False
            for block in self.block_set.block_set:
                if len(block) > 1:
                    verified = True

            if verified:

                for i in range(0, len(self.block_set.block_set)):
                    # recupero il blocco che sto analizzando
                    block = self.block_set.block_set[i]
                    if i == 0:
                        if len(block) > 1:
                            move = [Move(block[-2], block[-1])]
                        else:
                            move = []
                        moves.append(move)

                    elif i == (len(self.block_set.block_set)-1):
                        if len(block) > 1:
                            move = [Move(block[0], block[1])]
                        else:
                            move = []
                        moves.append(move)

                    else:
                        if len(block) > 2:
                            move_1 = Move(block[0], block[1])
                            move_2 = Move(block[-2], block[-1])
                            moves.append([move_1, move_2])

                        elif len(block) > 1:
                            move = Move(block[0], block[1])
                            moves.append([move])
                        else:
                            move = []
                            moves.append(move)
        return moves

    def __str__(self):

        stringa = "["
        for moves in self.move_set:
            stringa += "["
            for move in moves:
                stringa += str(move)
            stringa += "]"
        stringa += "]"

        return stringa

class Move:

    def __init__(self, task_1, task_2):
        self.task_1 = task_1
        self.task_2 = task_2

    def __str__(self):
        return "(" + self.task_1.name + ", " + self.task_2.name + ")"