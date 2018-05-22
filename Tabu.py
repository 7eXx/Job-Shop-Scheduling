from MoveSet import *
from queue import *
class Tabu_List:

    MAX_T = 5

    def __init__(self):

        self.moves = []

    ## metodo per eseguire la procedura T=T+Tmax
    def shiftTmax(self):

        if len(self.moves) > 0:
            self.moves.append(self.moves[-1])

        if len(self.moves) > Tabu_List.MAX_T:
            self.moves = self.moves[1:]


    ## ricerca se una mossa e' gia' presente nella lista
    def searchMove(self, move_search):

        found = False
        for move in self.moves:
            if Move.equalsMove(move, move_search):
                found = True
                break

        return found

    ## aggiunge una mossa tabu alla lista
    def addMoveTabu(self, move):

        if not self.searchMove(move):

            move_inver = move.generateInverse()
            if len(self.moves) == Tabu_List.MAX_T:

                self.moves = self.moves[1:] + [move_inver]
            else:
                self.moves.append(move_inver)

            return True

        return False

    def __str__(self):
        stringa = "["
        for m in self.moves:
            stringa += str(m)
        stringa += "]"

        return stringa