import heapq
import random

'''
Classe per modellare il Nodo
'''
class Node:

    def __init__(self, value):
        self.value = value
        self.h_score = None


    # Metodo che genera i figli del nodo
    def generate_children(self):
        children = [Node(self.value + random.randint(-5, 5)) for _ in xrange(3)]
        return children


    def __repr__(self):
        return str(self.value)


    def __hash__(self):
        return str(self.value)


# Funzione che calcola la distanza del nodo dall'obiettivo
def heuristic(node, goal=100):
    node.h_score = abs(node.value - goal)
    return node.h_score, node


# Funzione che implementa la beam search
def beam_search(origin, tabu_size=5, max_iterations=1000, max_children=4):

    # Inizializzo le strutture da usare
    node_list = [(-1, origin)]
    current_node = Node(None)
    tabu_set = []

    # Finche' il risultato euristico del nodo e' diverso da 0 scegli il miglior nodo dalla lista tramite heappop
    while current_node.h_score != 0:
        _, current_node = heapq.heappop(node_list)

        # Finche' il valore del nodo appena estratto e' nel tabu_set scegli nuovamente il miglior nodo dalla lista
        while current_node.value in tabu_set:
            _, current_node = heapq.heappop(node_list)

        # Aggiungo il valore del nodo attuale nella lista rimuovendo l'ultimo valore se il tabu_set supera il massimo
        tabu_set = [current_node.value] + tabu_set[:tabu_size - 1]
        print
        current_node.value, tabu_set

        # Genero i figli del nodo e per ciascun figlio, se ha un valore che non e' in tabu_set, inserisco nell'heap
        for node in current_node.generate_children():
            if node.value not in tabu_set:
                heapq.heappush(node_list, heuristic(node))

        # Riduco la dimensione della lista di nodi eliminando i nodi con valore piu' alto e quindi peggiore
        node_list = node_list[:max_children]

    # Restituisce il nodo corrente, cioe' il nodo che ha come risultato euristico 0
    return current_node

print
beam_search(Node(1))