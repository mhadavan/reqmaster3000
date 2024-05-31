import os
import json
import uuid

class ReqMaster3000:
    def __init__(self, config_dir="config", projects_dir="projects"):
        self.config_dir = config_dir
        self.projects_dir = projects_dir
        self.configs = self.load_configs()

    def load_configs(self):
        configs = {}
        for file_name in os.listdir(self.config_dir):
            with open(os.path.join(self.config_dir, file_name), 'r') as f:
                config = json.load(f)
                object_type = file_name.split('_config')[0]
                configs[object_type] = config
        return configs

    def create_project(self, project_name):
        project_path = os.path.join(self.projects_dir, project_name, 'objects')
        os.makedirs(project_path, exist_ok=True)
        print(f"Project '{project_name}' created.")

    def create_object(self, project_name, object_type, object_id, **attributes):
        if object_type not in self.configs:
            print(f"Error: Object type '{object_type}' does not exist.")
            return

        project_path = os.path.join(self.projects_dir, project_name, 'objects')
        if not os.path.isdir(project_path):
            print(f"Error: Project '{project_name}' does not exist.")
            return

        config = self.configs[object_type]
        
        # Check if object with given ID already exists
        if os.path.exists(os.path.join(project_path, f"{object_id}.json")):
            print(f"Error: Object ID '{object_id}' already exists.")
            return

        object_data = {field: attributes.get(field, "") for field in config['fields']}
        object_data['Unique Requirement ID'] = object_id

        with open(os.path.join(project_path, f"{object_id}.json"), 'w') as f:
            json.dump(object_data, f, indent=4)

        print(f"{object_type.capitalize()} '{object_id}' created in project '{project_name}'.")

    def edit_object(self, project_name, object_id, **attributes):
        project_path = os.path.join(self.projects_dir, project_name, 'objects')
        object_path = os.path.join(project_path, f"{object_id}.json")

        if not os.path.isfile(object_path):
            print(f"Error: Object ID '{object_id}' does not exist in project '{project_name}'.")
            return

        with open(object_path, 'r+') as f:
            object_data = json.load(f)
            object_data.update(attributes)
            f.seek(0)
            json.dump(object_data, f, indent=4)
            f.truncate()

        print(f"Object '{object_id}' updated in project '{project_name}'.")

    def create_link(self, project_name, object_id_1, object_id_2):
        project_path = os.path.join(self.projects_dir, project_name, 'objects')
        object_path_1 = os.path.join(project_path, f"{object_id_1}.json")
        object_path_2 = os.path.join(project_path, f"{object_id_2}.json")

        if not os.path.isfile(object_path_1) or not os.path.isfile(object_path_2):
            print("Error: One or both object IDs do not exist.")
            return

        with open(object_path_1, 'r+') as f1, open(object_path_2, 'r+') as f2:
            object_data_1 = json.load(f1)
            object_data_2 = json.load(f2)

            if "links" not in object_data_1:
                object_data_1["links"] = []
            if "links" not in object_data_2:
                object_data_2["links"] = []

            if object_id_2 not in object_data_1["links"]:
                object_data_1["links"].append(object_id_2)
            if object_id_1 not in object_data_2["links"]:
                object_data_2["links"].append(object_id_1)

            f1.seek(0)
            json.dump(object_data_1, f1, indent=4)
            f1.truncate()

            f2.seek(0)
            json.dump(object_data_2, f2, indent=4)
            f2.truncate()

        print(f"Link created between '{object_id_1}' and '{object_id_2}' in project '{project_name}'.")

    def validate_links(self, project_name):
        project_path = os.path.join(self.projects_dir, project_name, 'objects')
        object_files = os.listdir(project_path)
        object_ids = {os.path.splitext(obj)[0] for obj in object_files}
        broken_links = []

        for object_file in object_files:
            object_path = os.path.join(project_path, object_file)
            with open(object_path, 'r') as f:
                object_data = json.load(f)
                object_id = os.path.splitext(object_file)[0]
                if "links" in object_data:
                    for linked_id in object_data["links"]:
                        if linked_id not in object_ids:
                            broken_links.append((object_id, linked_id))

        if broken_links:
            print("Broken links found:")
            for object_id, broken_link in broken_links:
                print(f"Object '{object_id}' has a broken link to '{broken_link}'.")
        else:
            print("All links are valid.")

# Command-line interface
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ReqMaster 3000 - Requirement Management Tool")
    parser.add_argument("command", help="Command to run", choices=["create_project", "create_object", "edit_object", "create_link", "validate_links"])
    parser.add_argument("--project_name", help="Name of the project")
    parser.add_argument("--object_type", help="Type of object to create")
    parser.add_argument("--object_id", help="ID of the object to create or edit")
    parser.add_argument("--object_id_2", help="Second object ID to link")
    parser.add_argument("--attributes", nargs='*', help="Attributes for the object in key=value format")

    args = parser.parseArgs()
    reqmaster = ReqMaster3000()

    if args.command == "create_project":
        if args.project_name:
            reqmaster.create_project(args.project_name)
        else:
            print("Error: --project_name is required for creating a project.")
    elif args.command == "create_object":
        if args.project_name and args.object_type and args.object_id:
            attributes = {kv.split('=')[0]: kv.split('=')[1] for kv in args.attributes or []}
            reqmaster.create_object(args.project_name, args.object_type, args.object_id, **attributes)
        else:
            print("Error: --project_name, --object_type, and --object_id are required for creating an object.")
    elif args.command == "edit_object":
        if args.project_name and args.object_id:
            attributes = {kv.split('=')[0]: kv.split('=')[1] for kv in args.attributes or []}
            reqmaster.edit_object(args.project_name, args.object_id, **attributes)
        else:
            print("Error: --project_name and --object_id are required for editing an object.")
    elif args.command == "create_link":
        if args.project_name and args.object_id and args.object_id_2:
            reqmaster.create_link(args.project_name, args.object_id, args.object_id_2)
        else:
            print("Error: --project_name, --object_id, and --object_id_2 are required for creating a link.")
    elif args.command == "validate_links":
        if args.project_name:
            reqmaster.validate_links(args.project_name)
        else:
            print("Error: --project_name is required for validating links.")