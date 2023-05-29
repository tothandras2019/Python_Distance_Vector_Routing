import os
import json

class FileProcessor():
        
    def create_html_file(self, file_content):
        path_current = os.getcwd()
        full_path = os.path.join(path_current, "index")

        try:
            if not os.path.exists(full_path):
                os.mkdir(full_path)

            with open(os.path.join(full_path, "index.html"), "wt", encoding="utf-8") as dest_file:
                dest_file.write(file_content)

        except Exception as e:
            print("Create file went wrong", e)

    def create_json(self, target_folder, file):
        path_current = os.getcwd()
        full_path = os.path.join(path_current, target_folder)
        try:
            if not os.path.exists(full_path):
                os.mkdir(full_path)

            with open(os.path.join(full_path, "spanning_tree.json"), "w", encoding="utf-8") as dest_file:
                dest_file.write(json.dumps(file))

        except Exception as e:
            print("Create file went wrong", e)

    def read_json(self, file_path):
        if not file_path:
            print("File missing!")
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.loads(file.read())

        except Exception as e:
            print("Something went wrong!!", e)
    