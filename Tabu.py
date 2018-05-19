from MoveSet import *
from queue import *

'''
Classe per modellare la Tabu List
'''
class Tabu:

    None


class Tabu_List:

    # Variabile statica che definisce la grandezza massima della lista, quindi il numero massimo di mosse memorizzabili
    MAX_T = 5

    def __init__(self):
        self.moves = []


    # Metodo gestire le mosse sulla lista in base alla grandezza di quest'ultima
    def shiftTmax(self):

        # Se esiste una mossa nella lista inserisce l'ultima mossa nella lista
        if len(self.moves) > 0:
            self.moves.append(self.moves[-1])

        # Se la lista delle mosse e' piu' grande del consentito rimuove la mossa piu' vecchia (la prima della lista)
        if len(self.moves) > Tabu_List.MAX_T:
            self.moves = self.moves[1:]


    # Metodo che cerca se una mossa e' gia' presente nella lista
    def searchMove(self, move_search):

        # Confronta ogni la mossa parametro con quelle gia' presenti nella lista
        found = False
        for move in self.moves:
            if Move.equalsMove(move, move_search):
                found = True
                break

        # Restituisce True o False in base alla presenza o meno della mossa
        return found


    # Metodo che aggiunge una mossa tabu alla lista
    def addMoveTabu(self, move):

        # Se la mossa non e' gia' presente
        if not self.searchMove(move):

            # Genera l'inversione della mossa
            move_inver = move.generateInverse()

            # Se la grandezza della lista e' al massimo, inserisce la mossa invertita al posto della mossa piu' vecchia
            if len(self.moves) == Tabu_List.MAX_T:
                self.moves = self.moves[1:] + [move_inver]

            # Altrimenti la inserisce semplicemente in coda alla lista
            else:
                self.moves.append(move_inver)

            # Restituisce la conferma per l'avvenuto inserimento della mossa nella lista tabu
            return True

        # Ritorna False se non e' possibile inserire la mossa
        return False


    def __str__(self):
        stringa = "["
        for m in self.moves:
            stringa += str(m)
        stringa += "]"

        return stringa