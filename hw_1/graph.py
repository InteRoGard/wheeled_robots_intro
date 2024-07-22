# реализует граф, включает алгоритмы поиска и их вывод
# 

class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def printSolution(self, src, fnsh, pred):
        way = []        # сохраняет номера вершин кратчайшего пути
        node = fnsh
        print(node, end=' ')
        while node != src:
            if node != src and node != fnsh:
                way.append(node)
            print(pred[node], end=' ')
            node = pred[node]
        return way

    def minstance(self, shortest, sptSet):
        min = 1e7
        min_index = 0
        for v in range(self.V):
            if shortest[v] < min and sptSet[v] == False:
                min = shortest[v]
                min_index = v
        return min_index

    def Dijkstra(self, src, fnsh):
        shortest = [1e7] * self.V
        shortest[src] = 0
        pred = [0] * self.V
        sptSet = [False] * self.V
        for cout in range(self.V):
            u = self.minstance(shortest, sptSet)
            sptSet[u] = True
            for v in range(self.V):
                if (self.graph[u][v] > 0 and sptSet[v] == False and
                        shortest[v] > shortest[u] + self.graph[u][v]):
                    shortest[v] = shortest[u] + self.graph[u][v]
                    pred[v] = u
                if v == fnsh:
                    break
        return src, fnsh, pred
        # self.printSolution(src, fnsh, pred)
        # return shortest


