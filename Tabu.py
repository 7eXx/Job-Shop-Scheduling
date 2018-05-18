from MoveSet import *
from queue import *

'''
classe per modellare la tabu search
'''
class Tabu:

    None


class Tabu_List:

    MAX_T = 5

    def __init__(self):

        self.moves = []

    ## TODO implmentare T=T+Tmax (vedere appunti)
    #def shift


    ## ricerca se una mossa e' gia' presente nella lista
    def searchMove(self, move_search):

        found = False
        for move in self.tabu_list:
            if Move.equalsMove(move, move_search):
                found = True
                break

        return found


    def addMove(self, move):

        if not self.searchMove(move):

            move_inver = move.generateInverse()
            if len(self.tabu_list) == Tabu_List.MAX_T:

                self.tabu_list = self.tabu_list[1:] + [move_inver]
            else:
                self.tabu_list.append(move_inver)

            return True

        return False