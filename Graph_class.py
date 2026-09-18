from collections import defaultdict

class Graph:
    def __init__(self):
        self.adj = defaultdict(list)
        self.edges = set()
        self.original_edges = []  # Сохраняем оригинальные ребра для визуализации

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)
        edge = tuple(sorted((u, v)))
        self.edges.add(edge)
        self.original_edges.append(edge)

    def remove_edge(self, u, v):
        edge = tuple(sorted((u, v)))
        if edge in self.edges:
            self.edges.remove(edge)
            self.adj[u].remove(v)
            self.adj[v].remove(u)

    def get_degree(self, v):
        return len(self.adj[v])

    def is_bridge(self, u, v):
        if self.get_degree(u) <= 1:
            return True
        
        self.remove_edge(u, v)
        visited = set()
        stack = [u]
        
        while stack:
            curr = stack.pop()
            if curr == v:
                self.add_edge(u, v)
                return False
            if curr not in visited:
                visited.add(curr)
                stack.extend(self.adj[curr])
        
        self.add_edge(u, v)
        return True

    def fleury_algorithm(self, start_vertex):
        odd_degree_vertices = [v for v in self.adj if self.get_degree(v) % 2 != 0]
        if len(odd_degree_vertices) not in (0, 2):
            raise ValueError("Граф не содержит эйлерова пути или цикла")
        
        if len(odd_degree_vertices) == 2 and start_vertex not in odd_degree_vertices:
            start_vertex = odd_degree_vertices[0]

        path = []
        curr = start_vertex
        
        while self.edges:
            next_vertex = None
            bridge_edge = None
            
            for neighbor in list(self.adj[curr]):
                if tuple(sorted((curr, neighbor))) in self.edges:
                    if not self.is_bridge(curr, neighbor):
                        next_vertex = neighbor
                        break
                    else:
                        bridge_edge = neighbor
            
            if next_vertex is None:
                next_vertex = bridge_edge
            
            path.append(curr)
            self.remove_edge(curr, next_vertex)
            curr = next_vertex
        
        path.append(curr)
        return path

    def export_to_dot(self, filename, euler_path=None):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("graph G {\n  rankdir=LR;\n  node [shape=circle, style=filled, fillcolor=lightblue];\n")
            
            # Рисуем ОРИГИНАЛЬНЫЕ ребра (не те, что остались после алгоритма)
            drawn_edges = set()
            for edge in self.original_edges:
                u, v = edge
                if edge not in drawn_edges:
                    is_euler = False
                    if euler_path:
                        for i in range(len(euler_path) - 1):
                            if tuple(sorted((euler_path[i], euler_path[i+1]))) == edge:
                                is_euler = True
                                break
                    
                    style = 'color=red, penwidth=2.0' if is_euler else 'color=black'
                    f.write(f'  "{u}" -- "{v}" [{style}];\n')
                    drawn_edges.add(edge)
            
            # Определяем роли вершин (начало/конец/середина) БЕЗ дублирования
            if euler_path:
                vertex_roles = {}
                for i, v in enumerate(euler_path):
                    if i == 0 or i == len(euler_path) - 1:
                        vertex_roles[v] = "red"  # Начало или конец
                    elif v not in vertex_roles:
                        vertex_roles[v] = "yellow"  # Середина
                
                # Записываем каждую вершину только один раз
                for v, color in vertex_roles.items():
                    f.write(f'  "{v}" [fillcolor={color}];\n')
            
            f.write("}\n")
        print(f"Граф сохранен в {filename}")
