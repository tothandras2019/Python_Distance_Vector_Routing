# Az eredeti prezentacio alapjan (Egy pontbol kiindulva) es sajat elkepzeles alapjan is megcsinalhatom 2.-ra.
class Node:

    def __init__(self, name:str, connections:set, distances:dict, first_step:dict) -> None:
        self.name = name
        self.connections = connections
        self.distances = distances
        self.first_step = first_step

    def get_obj_name_from_dist(self, edge_name:str):
        name = self.name
        return edge_name.replace(name, '')

    def update_distances_connections(self, edge_dict:dict):
        for key,value in edge_dict.items():
            if key[0] == self.name or key[1] == self.name:
                self.distances[key] = value
                if self.name == key[0]:
                    self.connections.add(key[1])
                    self.first_step[key[1]] = key[1]
                else:    
                    self.connections.add(key[0])
                    self.first_step[key[0]] = key[0]

    def get_distance(self, other):
        name1 = self.name
        name2 = other.name
        dist_name = create_dist_name(name1, name2)
        dist = self.distances[dist_name]
        return dist
    
    def closest_new_node(self, spaning_tree) -> str:
        dist = float("inf")
        obj = None
        for edge, value in self.distances.items():
            test_obj = self.get_obj_name_from_dist(edge)
            if test_obj not in spaning_tree:
                if value <= dist:
                    dist = value
                    obj = self.get_obj_name_from_dist(edge)
        return obj
    
    def modify_distances(self, other):
        name1 = self.name
        name2 = other.name
        s_o_dist = self.get_distance(other)
        for con2 in other.connections:
            if name1 != con2:
                for con1 in self.connections:
                    if name2 != con1:
                        dist_name = create_dist_name(con1, name1)
                        dist_name2 = create_dist_name(con2, name2)
                        s_dist = self.distances[dist_name]
                        o_dist = other.distances[dist_name2]
                        if con2 == con1:
                            if s_dist > o_dist + s_o_dist:
                                self.distances[dist_name] = o_dist + s_o_dist
                                self.first_step[con2] = name2
                        elif con2 not in self.connections:
                            dist_name = create_dist_name(con2, name1)
                            self.distances[dist_name] = o_dist + s_o_dist
                            self.first_step[con2] = name2
    
    def route_calculation(self, other, object_list) -> str:
        route = self.name
        name2 = other.name
        first_step = self.first_step[name2]
        if first_step != name2:
            for next_step in object_list:
                if next_step.name == first_step:
                    route1 = other.route_calculation(next_step,object_list)
                    route = route + route1
                    return route
        else:
            route = route + first_step
            return route


def create_dist_name(name1:str, name2:str) -> str:
    if name1 > name2:
        dist_name = name2 + name1
    else:
        dist_name = name1 + name2
    return dist_name
        
def create_objects(routing_dict:dict):
    object_set = set()
    object_list = []
    for route in routing_dict.keys():
        name1 = route[0]
        name2 = route[1]
        object_set.add(name1)
        object_set.add(name2)
    for obj in object_set:
        obj = Node(obj,set(),{},{})
        obj.update_distances_connections(routing_dict)
        object_list.append(obj)
        object_list.sort(key=lambda x: x.name)
    return object_list

edge_dict = {"AC":2, "AD":1, "AE":4, "BF":2, "CD":2, "CF":3, "DF":7, "DG":10, "EF":6, "FG":5 }

def main():
    spanning_tree = []
    edges = []
    object_list = create_objects(edge_dict)
    start_point = object_list[0]
    print(start_point.name)
    spanning_tree.append(start_point.name)
    for i in range(len(object_list)-1):
        y = 0
        obj_name = start_point.closest_new_node(spanning_tree)
        spanning_tree.append(obj_name)
        for obj in object_list:
            if obj_name == obj.name:
                start_point.modify_distances(obj)
                edge = start_point.route_calculation(obj,object_list)
                edge = edge[-2:]
                edges.append(edge)
        print(f"{spanning_tree}  {edges}")
    return

main()
