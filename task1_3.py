from collections import deque

import networkx as nx
import matplotlib.pyplot as plt
import pylab

####### TASK_1 ########
G = nx.Graph()

G.add_nodes_from(["R1", "R2","R3","R4","R5","R6","R7","R8","R9","R10",
                  "R11","R12","R13","R14","R15","R16","R17","R18","R19","R20"])

G.add_edge('R1','R2', weight= 4)
G.add_edge('R1','R3', weight= 3)
G.add_edge('R1','R4', weight= 6)
G.add_edge('R2','R3', weight= 4)
G.add_edge('R2','R8', weight= 4)
G.add_edge('R3','R6', weight= 3)
G.add_edge('R3','R7', weight= 3)
G.add_edge('R4','R5', weight= 6)
G.add_edge('R4','R6', weight= 3)
G.add_edge('R5','R11', weight= 3)
G.add_edge('R5','R12', weight= 6)
G.add_edge('R6','R7', weight= 5)
G.add_edge('R6','R11', weight= 3)
G.add_edge('R7','R10', weight= 3)
G.add_edge('R8','R7', weight= 5)
G.add_edge('R8','R9', weight= 3)
G.add_edge('R9','R10', weight= 5)
G.add_edge('R9','R16', weight= 3)
G.add_edge('R10','R14', weight= 3)
G.add_edge('R10','R15', weight= 3)
G.add_edge('R11','R12', weight= 3)
G.add_edge('R11','R14', weight= 3)
G.add_edge('R12','R13', weight= 5)
G.add_edge('R13','R19', weight= 5)
G.add_edge('R14','R13', weight= 6)
G.add_edge('R14','R18', weight= 3)
G.add_edge('R15','R17', weight= 4)
G.add_edge('R15','R18', weight= 3)
G.add_edge('R16','R15', weight= 6)
G.add_edge('R16','R17', weight= 3)
G.add_edge('R18','R19', weight= 4)
G.add_edge('R20','R17', weight= 2)
G.add_edge('R20','R18', weight= 3)
G.add_edge('R20','R19', weight= 4)

edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])

pylab.figure(figsize=(8,8))
pos=nx.spring_layout(G)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
nx.draw_networkx(G,pos, node_size=900, arrows=True, edge_cmap=plt.cm.Reds)

####### TASK_2 ########

def dfs_recursive(graph, vertex, visited=None):
    if visited is None:
        visited = set()
    visited.add(vertex)
    print(vertex, end=' ')  # Відвідуємо вершину
    for neighbor in graph[vertex]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)


def bfs_recursive(graph, queue, visited=None):
    # Перевіряємо, чи існує множина відвіданих вершин, якщо ні, то ініціалізуємо нову
    if visited is None:
        visited = set()
    # Якщо черга порожня, завершуємо рекурсію
    if not queue:
        return
    # Вилучаємо вершину з початку черги
    vertex = queue.popleft()
    # Перевіряємо, чи відвідували раніше дану вершину
    if vertex not in visited:
        # Якщо не відвідували, друкуємо вершину
        print(vertex, end=" ")
        # Додаємо вершину до множини відвіданих вершин.
        visited.add(vertex)
        # Додаємо невідвіданих сусідів даної вершини в кінець черги.
        queue.extend(set(graph[vertex]) - visited)
    # Рекурсивний виклик функції з тією ж чергою та множиною відвіданих вершин
    bfs_recursive(graph, queue, visited)

dfs_tree = nx.dfs_tree(G, "R1")
print('Пошук у глибину (DFS)')
dfs_recursive(G, 'R1')

bfs_tree = nx.bfs_tree(G, "R1")
print()
print('пошук у ширину (BFS)')
bfs_recursive(G, deque(["R1"]))
print()

pylab.show()

####### TASK_3 ########

def print_table(distances, visited):
    # Верхній рядок таблиці
    print("{:<10} {:<10} {:<10}".format("Вершина", "Відстань", "Перевірено"))
    print("-" * 30)

    # Вивід даних для кожної вершини
    for vertex in distances:
        distance = distances[vertex]
        if distance == float('infinity'):
            distance = "∞"
        else:
            distance = str(distance)

        status = "Так" if vertex in visited else "Ні"
        print("{:<10} {:<10} {:<10}".format(vertex, distance, status))
    print("\n")


def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    unvisited = list(graph.keys())
    visited = []

    while unvisited:
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])

        if distances[current_vertex] == float('infinity'):
            break

        for neighbor, weight in graph[current_vertex].items():
            distance = distances[current_vertex] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance

        visited.append(current_vertex)
        unvisited.remove(current_vertex)

        # Вивід таблиці після кожного кроку
        print_table(distances, visited)

    return distances


# Приклад графа у вигляді словника
graph = {
    'R1': {'R2': 4, 'R3': 3, 'R4': 6},
    'R2': {'R1': 4, 'R3': 4, 'R8': 4},
    'R3': {'R1': 3, 'R2': 4, 'R6': 3, 'R7': 3},
    'R4': {'R1': 6,'R5': 6, 'R6': 3},
    'R5': {'R4': 6, 'R11': 3, 'R12': 6},
    'R6': {'R3': 3, 'R4': 3, 'R7': 5, 'R11': 3},
    'R7': {'R3': 3, 'R6': 5, 'R8': 5, 'R10': 3},
    'R8': {'R2': 4, 'R7': 5, 'R9': 3},
    'R9': {'R8': 3, 'R10': 5, 'R16': 3},
    'R10': {'R7': 3, 'R9': 5, 'R14': 3, 'R15': 3},
    'R11': {'R5': 3, 'R6': 3, 'R12': 3, 'R14': 3},
    'R12': {'R5': 6, 'R11': 3, 'R13': 5},
    'R13': {'R12': 5, 'R14': 6, 'R19': 5},
    'R14': {'R10': 3, 'R11': 3, 'R13': 6, 'R18': 3},
    'R15': {'R10': 3, 'R16': 6, 'R17': 4, 'R18': 3},
    'R16': {'R9': 3, 'R15': 6, 'R17': 3},
    'R17': {'R15': 4, 'R16': 3, 'R20': 2},
    'R18': {'R14': 3, 'R15': 3, 'R19': 4, 'R20': 3},
    'R19': {'R13': 5, 'R18': 4, 'R20': 4},
    'R20': {'R17': 2, 'R18': 3, 'R19': 4}
}

# Виклик функції для вершини 'R1'
dijkstra(graph, 'R1')

# Застосування алгоритму Дейкстри
shortest_paths = nx.single_source_dijkstra_path(G, source='R1')
shortest_path_lengths = nx.single_source_dijkstra_path_length(G, source='R1')

print('найкоротший шляхи від початкового вузла до всіх інших вузлів')
print(shortest_paths) 

print('довжина найкоротшого шляху від початкового вузла до всіх інших вузлів')
print(shortest_path_lengths)  # виведе довжини найкоротших шляхів від вузла 'A' до всіх інших вузлів