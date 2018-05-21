'''
classe per modellare il MoveSet
'''
class MoveSet:

    def __init__(self, block_set):

        self.block_set = block_set
        self.move_set = self.buildMoves()


    # Metodo che crea l'insieme delle operazioni scambiabili
    def buildMoves(self):

        # Verifica che almeno un blocco abbia dimensione maggiore di 1
        moves = []
        if len(self.block_set.block_set) > 1:
            verified = False
            for block in self.block_set.block_set:
                if len(block) > 1:
                    verified = True

            # Se esiste almeno un blocco di dimensione maggiore di 1
            if verified:

                # Per ogni blocco del block set
                for i in range(0, len(self.block_set.block_set)):
                    block = self.block_set.block_set[i]

                    # Se sono al primo blocco ed e' più grande di 1 ho questo spostamento
                    if i == 0:
                        if len(block) > 1:
                            move = Move(block[-2], block[-1])
                            moves.append(move)

                    # Altrimenti se sono all'ultimo blocco ed e' più grande di 1 ho questo spostamento
                    elif i == (len(self.block_set.block_set)-1):
                        if len(block) > 1:
                            move = Move(block[0], block[1])
                            moves.append(move)

                    # Altrimenti (caso in cui i sia compreso tra 1 e len(self.block_set.block_set)-2)
                    else:

                        # Se il blocco e' piu' grande di 2 ho 2 possibili spostamenti
                        if len(block) > 2:
                            move_1 = Move(block[0], block[1])
                            move_2 = Move(block[-2], block[-1])
                            moves.append(move_1)
                            moves.append(move_2)

                        # Altrimenti se il blocco e' grande di 1 ho questo spostamento
                        elif len(block) > 1:
                            move = Move(block[0], block[1])
                            moves.append(move)

        # Restituisce la lista delle mosse
        return moves


    def __str__(self):

        stringa = "["
        for move in self.move_set:
            stringa += str(move)
        stringa += "]"

        return stringa


'''
classe per modellare la mossa Move
'''
class Move:

    def __init__(self, task_1, task_2):
        self.task_1 = task_1
        self.task_2 = task_2
        self.machine = task_1.machine


    # Metodo che verifica se due mosse sono identiche tra loro
    def equalsMove(move_1, move_2):
        return (move_1.task_1.name == move_2.task_1.name) and (move_1.task_2.name == move_2.task_2.name)


    # Metodo che genera l'inverso della mossa
    def generateInverse(self):
        return Move(self.task_2, self.task_1)


    # Metodo che cerca una mossa in una lista
    def findMove(move, list):

        # Cerca la mossa nella lista finche' non la trova restituendo True o False
        found = False
        for m in list:
            if Move.equalsMove(move, m):
                found = True
                break
        return found


    # Metodo che unisce due liste di mosse
    def unionMoves(move_list_1, move_list_2):

        # Per ogni mossa in entrambe le movelist inserisce la mossa nell'unione se non e' gia' presente
        union_list = []
        for m in move_list_1:
            if not(Move.findMove(m, union_list)):
                union_list.append(m)
        for m in move_list_2:
            if not(Move.findMove(m, union_list)):
                union_list.append(m)

        # Restituisce l'unione della lista di mosse
        return union_list


    def __str__(self):
        return "(" + self.task_1.name + ", " + self.task_2.name + ")"