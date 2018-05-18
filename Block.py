
'''
classe per la gestione del

'''
class BlockSet:

    def __init__(self, critical_path):

        self.block_set = self.buildBlocks(critical_path)

    ## questo metodo dal critical path restituisce
    ## una lista di blocchi: dimensione massima per ogni macchina
    ## (per maggiori dettagli vedere teoria)
    def buildBlocks(self, critical_path):

        blocks = []
        prev_task = None
        for task in critical_path:

            ## verifica se il task precedente della macchina è nullo
            if task.mpTask is None or task.machine != prev_task.machine:
                blocks.append([task])

            else:
                blocks[-1].append(task)

            prev_task = task

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

