import math


class Node():

    _prev_dest_pair = []
    _min_dist = math.inf
    _origin_direction_pair = {}

    _is_first = False

    index = 0

    def __init__(self, name, neighbs) -> None:
        self.name = name
        self.neighbours = neighbs
        
        self.neighbour_instances = []

    def get_name(self):
        return self.name

    def add_neghb_node_instance(self, node_intance)->None:
        self.neighbour_instances.append(node_intance)       

    def add_visited(self, current_pair):
            if current_pair not in type(self)._prev_dest_pair:
                type(self)._prev_dest_pair.append(current_pair)

    def get_distance_to_destination(self, from_node, dest_node_name)-> int:
        current_pair = f"{self.get_name()}{dest_node_name}"
        # RETURN condition:
        if from_node.get_name() == dest_node_name or current_pair in type(self)._prev_dest_pair:
            return 0
        
        #print("curr - to:", current_pair)
        self.add_visited(current_pair)

        # if type(self).index == 0:
        #     self.origin_direction_pair[f"{from_node.get_name()}"] = None
        #     type(self).index += 1
        
        #print("PAIR:", type(self)._prev_dest_pair)

        instance = None
        ret = 0
        dest_distance_in_neighbours = None
        for neigbour_dict in from_node.neighbours:
            if not type(self)._is_first:
              type(self)._origin_direction_pair[neigbour_dict["node"]] = math.inf

            if neigbour_dict["node"] == dest_node_name:
                dest_distance_in_neighbours = neigbour_dict["distance"]
                break
        type(self)._is_first = True
      
        #print(type(self)._origin_direction_pair)

        # if dest_distance_in_neighbours:
        #     return dest_distance_in_neighbours

        for instance_node in from_node.neighbour_instances:
            instance = instance_node
            ret += instance_node.get_distance_to_destination(instance_node, dest_node_name)         
        
        ac_dist = 0
        for actual in self.get_neigbh():
            if actual["node"] == instance.get_name():
                ac_dist += actual["distance"]
                break        
       
        #print("direction_pair: ", type(self)._direction_pair)
        #print("RET:", ac_dist, ret)
        return ac_dist + ret  
    
    def get_neigbh(self) -> list:
        return self.neighbours
    
    def __str__(self) -> str:
        return f"Node: {self.name}, Neighbours: {self.neighbours}"
       

    


