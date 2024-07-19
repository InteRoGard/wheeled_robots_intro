import interface, algorithms
from interface import alg_calc, map_matrix, adj_matrix, selection, rows, cols
from algorithms import Graph


print(map_matrix)
start, finish = 0, 0
for i in range(rows):
    for j in range(cols):
        num = ((i * cols) + j)
        if map_matrix[i][j] == 2:
            start = num
            print(f'start {start}')
        elif map_matrix[i][j] == 3:
            finish = num
            print(f'finish {finish}')

g = Graph(rows * cols)
g.graph = adj_matrix
src, fnsh, pred = g.Dijkstra(start, finish)
way = g.printSolution(src, fnsh, pred)
way = way[::-1]
print('\nWay:', way)

alg_calc(way)

# count = 0
# i = 0
# for btn in buttons:
#     if count == way[i]:
#         btn.config(bg = 'green')
#         count += 1
#         i += 1