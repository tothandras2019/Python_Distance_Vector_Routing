from App import MessageingApp
from node_component import node
from node_component import graph

import os


class NodeManager:
    def __init__(self) -> None:
        self.node_instances = []
        self.load_nodes()


        self.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
                    [4, 0, 8, 0, 0, 0, 0, 11, 0],
                    [0, 8, 0, 7, 0, 4, 0, 0, 2],
                    [0, 0, 7, 0, 9, 14, 0, 0, 0],
                    [0, 0, 0, 9, 0, 10, 0, 0, 0],
                    [0, 0, 4, 14, 10, 0, 2, 0, 0],
                    [0, 0, 0, 0, 0, 2, 0, 1, 6],
                    [8, 11, 0, 0, 0, 0, 1, 0, 7],
                    [0, 0, 2, 0, 0, 0, 6, 7, 0]
                ]
        d_graph = graph.Graph(9)
        d_graph.graph = self.graph
        d_graph.dijkstra(0)
    

    def load_nodes(self):
        path = os.getcwd()
        directory = "network"
        file = "distance_vector.json"

        full_path = os.path.join(path, directory, file)

        node_list = MessageingApp.read_json(full_path)
        self.upload_node_instance_list(node_list)

    def upload_node_instance_list(self, nodes):
        if not nodes:
            return

        node_list = [node["node"] for node in nodes]

        for node_obj in nodes:
            name = node_obj["node"]
            neighb = node_obj["neighbours"]

            node_inst = node.Node(name, neighb)
            self.node_instances.append(node_inst)

        for n_instance in self.node_instances:
            node_name = n_instance.get_name()

            for node_net in n_instance.get_neigbh():
                for other_instance in self.node_instances:
                    if node_net["node"] == other_instance.get_name():
                        n_instance.add_neghb_node_instance(other_instance)
                        # print("Other", other_instance)

    def find_shortest_distance(self, from_node, to_node):
        summa = 0
        for node_instance in self.node_instances:
            if from_node == node_instance.get_name():
               summa += node_instance.get_distance_to_destination(node_instance, to_node)
               break
        
        print("summa...:", summa)
                
