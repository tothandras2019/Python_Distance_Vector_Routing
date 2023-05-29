from node_component import node_manager
from node_component import graph
from filemanager import fileprocessor
import sys
import os
import webbrowser

class MessageingApp:
    app_state = "INIT"

    states = {
        "init": "INIT",
        "draw": "DRAW",
        "inputs": "INPUTS",
        "modify": "MODIFY",
        "quit": "QUIT",
    }

    def __init__(self) -> None:
        self.gr = graph.Graph()
        self.help_user = None
        self._graph = None
        self.file_processor = fileprocessor.FileProcessor()

        self.apply_states()

        # BACKUP:
        # args = sys.argv
        # self.start_user_interface(args)
        # self.nodeManager = node_manager.NodeManager()

    def open_page(self):
        path = os.getcwd()
        webbrowser.open(os.path.join(path, "index", "index.html"))

    def create_base_index_page(self, data):
        script_data = f"<script> const enbeded_data = {data} </script>"

        return f'<!DOCTYPE html><html lang="en"> <head> <meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <link rel="stylesheet" href="style.css"> <script defer src="script.js"></script> <title>Hello</title>  </head> <body><span>Ha nem tetszik az alakzat vonszold a pöttyöket odébb!</span> <div id="root"> </div> {script_data}</body> </html>'

    def apply_states(self):
        while True:
            if type(self).app_state == type(self).states["init"]:
                self.load_graph()
                print("----------GRAPH LOADED-----------")

            if type(self).app_state == type(self).states["inputs"]:
                print("----------MENU-----------")
                start_node = input('(KILÉPÉS: "q", MÓDOSÍTÁS: m, FESZÍTŐFA - Böngésző nézet!!!: "f") \n Add meg betuvel a kiindulasi pontot.\n>> ') 
                start_node = start_node.upper()

                if start_node == "Q":
                    type(self).app_state = type(self).states["quit"]
                    break

                if start_node == "F":
                    type(self).app_state = type(self).states["draw"]
                    continue
                if start_node == "M":
                    type(self).app_state = type(self).states["modify"]
                    continue

                end_node = input("Add meg betuvel a cel pontot: ")
                end_node = end_node.upper()

                self.gr.print_result(self.gr.dijkstra_II(self._graph, start_node), start_node, end_node)

            if type(self).app_state == type(self).states["draw"]:
                print("----------DRAW-----------")
                tree = self.gr.draw_tree(self._graph)

                self.file_processor.create_html_file(self.create_base_index_page(tree))
                self.open_page()

                type(self).app_state = type(self).states["inputs"]

            if type(self).app_state == type(self).states["modify"]:
                print("[GRAPH]:", self._graph)
                self.modyfy_graph()

                type(self).app_state = type(self).states["inputs"]


            if type(self).app_state == type(self).states["quit"]:
                print("----------EXIT-----------")
                sys.exit()

    def modyfy_graph(self):
        while True:
            modify_state = input("Törlés: d\nMódosítás: m\nKilépés: q\n>>")
            modify_state = modify_state.upper()

            node = None

            if modify_state == "M" or  modify_state == "D":
                print("------TÖRLÉS------" if modify_state== "D" else "----MÓDOSÍTÁS----")
                node = input("Melyik csúcsot akarod törölni/módosítani?\n>>")
                node = node.upper()
                
                if modify_state == "Q":
                    type(self).app_state = type(self).states["inputs"]
                    break

            if modify_state == "M":
                try: 
                    neighb = input("Melyik élt?\n>>")
                    neighb = neighb.upper()

                    weight = input("Él új súlya:\n>>")
                    weight = int(weight)

                    if type(weight) != int:
                        raise ValueError

                    self._graph[node][neighb]=weight
                    self._graph[neighb][node]=weight

                    print("Módosítva 1:", self._graph[node])
                    print("Módosítva 2:", self._graph[neighb])

                    return
                
                except ValueError as e:
                    print("Nem számot adott meg!!")

            if modify_state == "D":
                print(f"{node}:", self._graph[node], end="")
                del self._graph[node]

                for neighbours in self._graph.items():
                    if node in neighbours[1]:
                        del neighbours[1][node]
                    
                print(" - csúcs törölve:")
                return
            
            if modify_state == "Q":
                type(self).app_state = type(self).states["inputs"]
                break

    def load_graph(self):
        path = os.getcwd()
        file = "graph.json"
        full_path = os.path.join(path, "network", file)

        #self._graph = self.read_json(full_path)
        self._graph =  self.file_processor.read_json(full_path)

        if self._graph:
            type(self).app_state = type(self).states["inputs"]
            pass


if __name__ == "__main__":
    MessageingApp()

    # region BACKUP
    # def start_user_interface(self, args):
    #     path = os.getcwd()
    #     file = "usage.json"
    #     file_access = os.path.join(path, "app_usage", file)
    #     self.help_user = type(self).read_json(file_access)

    #     cmd_list = args[1:]
    #     if "--help" in cmd_list:
    #         self.print_app_usage()
    #         sys.exit()

    #     if "-s" not in cmd_list or "-d" not in cmd_list:
    #         self.print_app_usage()
    #         print("[Commands missing!!!]")
    #         sys.exit()

    #     if len(cmd_list) < 4:
    #         self.print_app_usage()
    #         "[Message or destination were missing!!!]"
    #         sys.exit()

    #     from_node = cmd_list[1]
    #     destination_node = cmd_list[3]

    #     print("start:", from_node)
    #     print("destination:", destination_node)

    #     self.nodeManager.find_shortest_distance(from_node, destination_node)

    # def print_app_usage(self):
    #     if not self.help_user:
    #         return

    #     for _ in range(0, 100):
    #         print("_", end="")

    #     print(f"\n{self.help_user['start']}\n")
    #     for row in self.help_user["start_cmd"]:
    #         print(*row, end="\n")

    #     print(f"\n{self.help_user['modify']}\n")
    #     for row in self.help_user["modfy_cmd"]:
    #         print(*row, end="\n")

    #     for _ in range(0, 100):
    #         print("_", end="")
    #     print("\n")
    # endregion
