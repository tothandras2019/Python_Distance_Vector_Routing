import math


class Graph:


    def __init__(self,):
        pass

    def printSolution(self, dist, end):
        print("Vertex \t Distance from Source")
        for key, val in dist.items():
            print(key, "\t\t", val)

        print("--------DESTINATION----------")
        for key, val in dist.items():
            if key == end:
                print(key, "\t\t", val)        
    
    def short_way(self, previous_nodes, start, end):
        way = []
        current_node = end

        while current_node != start:
            way.append(current_node)
            current_node = previous_nodes[current_node]

        way.append(start)
        way.reverse()

        return way

    def dijkstra_II(self, graph, start):
        distances = {node: math.inf for node in graph}
        distances[start] = 0
   
        self.priority_queue = [(0, start)]
        prev_nodes = {}

        while self.priority_queue:
            self.priority_queue.sort()
            current_distance, current_node = self.priority_queue.pop(0)

            if current_distance > distances[current_node]:
                continue
            
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    #print(distance, "<", distances[neighbor],  weight)
                 
                    prev_nodes[neighbor]=current_node
                    distances[neighbor] = distance
                    self.priority_queue.append((distance, neighbor))

        return [distances, prev_nodes]
    
    def draw_tree(self, graph):
        all_tree = {}
        for key in graph.keys():
           all_tree[key] = self.spanning_tree(key, graph)

        return all_tree
    
    def spanning_tree(self, init_node, graph):
        target_nodes = []
        all_shortest = []

        for key in graph.keys():
            if key != init_node:
                target_nodes.append(key)

        for end_node in target_nodes:
           all_shortest.append(self.print_result(self.dijkstra_II(graph, init_node), init_node, end_node))
        
        return all_shortest

    def print_result(self, dijkstra, start_node, end_node):
        distances, previous_nodes = dijkstra

        shortest_distance = distances[end_node]
        shortest_path = self.short_way(previous_nodes, start_node, end_node)

        print(f"A legrovidebb utvonal: {' -> '.join(shortest_path)} , a tavolsag: {shortest_distance}")
        return shortest_path


# _graph = {
#         "S": {"B": 4, "C": 2, "G": 5, "S": 3},
#         "B": {"S": 4, "C": 1, "H": 1},
#         "C": {"S": 2, "B": 1, "H": 5, "D": 6, "I": 5},
#         "D": {"H": 9, "C": 6, "I": 8, "E": 9},
#         "E": {"F": 8, "I": 3, "D": 9},
#         "F": {"G": 9, "I": 2, "E": 8},
#         "G": {"S": 5, "I": 3, "F": 9},
#         "H": {"B": 1, "C": 5, "D": 9},
#         "I": {"S": 3, "C": 5, "D": 8, "E": 3, "F": 2, "G": 3},
#     }

# gr = Graph()
#result = gr.forwarding(_graph)
# gr.draw_tree(_graph)


