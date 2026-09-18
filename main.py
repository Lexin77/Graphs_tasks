from Graph_class import Graph

g = Graph()
for u, v in [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]:
    g.add_edge(u, v)
    
path = g.fleury_algorithm(start_vertex=1)
print("Эйлеров путь:", " -> ".join(map(str, path)))
g.export_to_dot("task3_graph.dot", euler_path=path)