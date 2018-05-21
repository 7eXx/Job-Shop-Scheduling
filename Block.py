'''
classe per la gestione del BlockSet

'''
class BlockSet:

    def __init__(self, critical_path):

        self.block_set = self.buildBlocks(critical_path)


    # Metodo che dal critical path restituisce una lista di blocchi di dimensione massima per ogni macchina
    def buildBlocks(self, critical_path):

        # Per ogni task nel critical_path
        blocks = []
        prev_task = None
        for task in critical_path:

            # Verifica se il task precedente della macchina è nullo aggiungendo un blocco composto dal solo task
            if task.mpTask is None or prev_task is not None and task.machine != prev_task.machine:
                blocks.append([task])

            # In caso contrario inserisce il task nell'ultimo blocco
            elif len(blocks) > 0:
                blocks[-1].append(task)

            # Aggiornamento il task precedente
            prev_task = task

        # Ritorna la lista dei blocchi
        return blocks



    def __str__(self):
        stringa = "["
        for blocks in self.block_set:
            stringa += "[ "
            for task in blocks:
                stringa += task.name + " "
            stringa += "]"

        stringa += "]"
        return stringa