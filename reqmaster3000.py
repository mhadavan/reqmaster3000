import os
"""
ReqMaster3000 is a requirement management tool that allows users to create projects, objects, and links between objects. 
It also provides functionality to validate the links between objects.
Attributes:
    config_dir (str): Directory where configuration files are stored.
    projects_dir (str): Directory where projects are stored.
    configs (dict): Dictionary to store configurations loaded from config_dir.
Methods:
    __init__(self, config_dir="config", projects_dir="projects"):
        Initializes the ReqMaster3000 instance with the given configuration and projects directories.
    load_configs(self):
        Loads configuration files from the config_dir and returns a dictionary of configurations.
    create_project(self, project_name):
        Creates a new project with the given project name.
    create_object(self, project_name, object_type, object_id, **attributes):
        Creates a new object in the specified project with the given object type, object ID, and attributes.
    edit_object(self, project_name, object_id, **attributes):
        Edits an existing object in the specified project with the given object ID and updates its attributes.
    create_link(self, project_name, object_id_1, object_id_2):
        Creates a link between two objects in the specified project.
    validate_links(self, project_name):
        Validates the links between objects in the specified project and identifies any broken links.
"""


import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ReqMaster3000:
    def __init__(self, config_dir="config", projects_dir="projects"):
        self.config_dir = config_dir
        self.projects_dir = projects_dir
        self.configs = self.load_configs()

    def load_configs(self):
        configs = {}
        try:
            for file_name in os.listdir(self.config_dir):
                with open(os.path.join(self.config_dir, file_name), 'r') as f:
                    config = json.load(f)
                    object_type = file_name.split('_config')[0]
                    configs[object_type] = config
        except Exception as e:
            logging.error(f"Failed to load configs: {e}")
        return configs

    def create_project(self, project_name):
        project_path = os.path.join(self.projects_dir, project_name, 'objects')
        if os.path.exists(project_path):
            logging.error(f"Error: Project '{project_name}' already exists.")
            return
        try:
            os.makedirs(project_path, exist_ok=True)
            logging.info(f"Project '{project_name}' created.")
        except Exception as e:
            logging.error(f"Failed to create project '{project_name}': {e}")

    def create_object(self, project_name, object_type, object_id, **attributes):
        if object_type not in self.configs:
            logging.error(f"Error: Object type '{object_type}' does not exist.")
            return

        project_path = os.path.join(self.projects_dir, project_name, 'objects')
        if not os.path.isdir(project_path):
            logging.error(f"Error: Project '{project_name}' does not exist.")
            return

        config = self.configs[object_type]
        
        # Check if object with given ID already exists
        if os.path.exists(os.path.join(project_path, f"{object_id}.json")):
            logging.error(f"Error: Object ID '{object_id}' already exists in the project.")
            return

        object_data = {field: attributes.get(field, "") for field in config['fields']}
        object_data['Unique Requirement ID'] = object_id

        try:
            with open(os.path.join(project_path, f"{object_id}.json"), 'w') as f:
                json.dump(object_data, f, indent=4)
            logging.info(f"{object_type.capitalize()} '{object_id}' created in project '{project_name}'.")
        except Exception as e:
            logging.error(f"Failed to create object '{object_id}' in project '{project_name}': {e}")

    def edit_object(self, project_name, object_id, **attributes):
        project_path = os.path.join(self.projects_dir, project_name, 'objects')
        object_path = os.path.join(project_path, f"{object_id}.json")

        if not os.path.isfile(object_path):
            logging.error(f"Error: Object ID '{object_id}' does not exist in project '{project_name}'.")
            return

        try:
            with open(object_path, 'r+') as f:
                object_data = json.load(f)
                object_data.update(attributes)
                f.seek(0)
                json.dump(object_data, f, indent=4)
                f.truncate()
            logging.info(f"Object '{object_id}' updated in project '{project_name}'.")
        except Exception as e:
            logging.error(f"Failed to edit object '{object_id}' in project '{project_name}': {e}")

    def create_link(self, project_name, object_id_1, object_id_2):
        project_path = os.path.join(self.projects_dir, project_name, 'objects')
        object_path_1 = os.path.join(project_path, f"{object_id_1}.json")
        object_path_2 = os.path.join(project_path, f"{object_id_2}.json")

        if not os.path.isfile(object_path_1) or not os.path.isfile(object_path_2):
            logging.error("Error: One or both object IDs do not exist.")
            return

        try:
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

            logging.info(f"Link created between '{object_id_1}' and '{object_id_2}' in project '{project_name}'.")
        except Exception as e:
            logging.error(f"Failed to create link between '{object_id_1}' and '{object_id_2}' in project '{project_name}': {e}")

    def list_projects(self):
        try:
            projects = [d for d in os.listdir(self.projects_dir) if os.path.isdir(os.path.join(self.projects_dir, d))]
            if projects:
                logging.info("Projects found:")
                for project in projects:
                    logging.info(f"  - {project}")
            else:
                logging.info("No projects found.")
        except Exception as e:
            logging.error(f"Failed to list projects: {e}")
    def validate_links(self, project_name):
        project_path = os.path.join(self.projects_dir, project_name, 'objects')
        try:
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
                logging.warning("Broken links found:")
                for object_id, broken_link in broken_links:
                    logging.warning(f"Object '{object_id}' has a broken link to '{broken_link}'.")
            else:
                logging.info("All links are valid.")
        except Exception as e:
            logging.error(f"Failed to validate links in project '{project_name}': {e}")

    def list_links(self, project_name, object_id):
        project_path = os.path.join(self.projects_dir, project_name, 'objects')
        object_path = os.path.join(project_path, f"{object_id}.json")

        if not os.path.isfile(object_path):
            logging.error(f"Error: Object ID '{object_id}' does not exist in project '{project_name}'.")
            return

        try:
            with open(object_path, 'r') as f:
                object_data = json.load(f)
                links = object_data.get("links", [])
                title = object_data.get("Title", "No title")
                logging.info(f"Object '{object_id}' (Title: '{title}') in project '{project_name}' has links to:")
                if links:
                    for link in links:
                        link_path = os.path.join(project_path, f"{link}.json")
                        if os.path.isfile(link_path):
                            with open(link_path, 'r') as lf:
                                link_data = json.load(lf)
                                link_title = link_data.get("Title", "No title")
                                logging.info(f"  - {link_title}")
                        else:
                            logging.info(f"  - No title")
                else:
                    logging.info(f"Object '{object_id}' (Title: '{title}') in project '{project_name}' has no links.")
        except Exception as e:
            logging.error(f"Failed to list links for object '{object_id}' in project '{project_name}': {e}")

    def help(self):
        print("ReqMaster 3000 - Requirement Management Tool")
        print("Commands:")
        print("  create-project --project-name <project_name>")
        print("  create-object --project-name <project_name> --object-type <object_type> --object-id <object_id> [--attributes key1=value1 key2=value2 ...]")
        print("  edit-object --project-name <project_name> --object-id <object_id> [--attributes key1=value1 key2=value2 ...]")
        print("  create-link --project-name <project_name> --object-id <object_id> --object-id-2 <object_id_2>")
        print("  validate-links --project-name <project_name>")
        print("  list-projects")
        print("  list-links --project-name <project_name> --object-id <object_id>")
        print("  help")

# Command-line interface
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ReqMaster 3000 - Requirement Management Tool")
    parser.add_argument("command", help="Command to run", choices=["create-project", "create-object", "edit-object", "create-link", "validate-links", "help", "list-projects", \
    "list-links"])
    parser.add_argument("--project-name", help="Name of the project", required=False)
    parser.add_argument("--object-type", help="Type of object to create", required=False)
    parser.add_argument("--object-id", help="ID of the object to create or edit", required=False)
    parser.add_argument("--object-id-2", help="Second object ID to link", required=False)
    parser.add_argument("--attributes", nargs='*', help="Attributes for the object in key=value format", required=False)

    args = parser.parse_args()
    reqmaster = ReqMaster3000()
    print(args.command)
    if args.command == "create-project":
        print(args.project_name)
        if args.project_name:
            reqmaster.create_project(args.project_name)
        else:
            print("Error: --project_name is required for creating a project.")
    elif args.command == "create-object":
        if args.project_name and args.object_type and args.object_id:
            attributes = {kv.split('=')[0]: kv.split('=')[1] for kv in args.attributes or []}
            reqmaster.create_object(args.project_name, args.object_type, args.object_id, **attributes)
        else:
            print("Error: --project-name, --object-type, and --object-id are required for creating an object.")
    elif args.command == "edit-object":
        if args.project_name and args.object_id:
            attributes = {kv.split('=')[0]: kv.split('=')[1] for kv in args.attributes or []}
            reqmaster.edit_object(args.project_name, args.object_id, **attributes)
        else:
            print("Error: --project-name and --object-id are required for editing an object.")
    elif args.command == "create-link":
        if args.project_name and args.object_id and args.object_id_2:
            reqmaster.create_link(args.project_name, args.object_id, args.object_id_2)
        else:
            print("Error: --project-name, --object-id, and --object-id-2 are required for creating a link.")
    elif args.command == "validate-links":
        if args.project_name:
            reqmaster.validate_links(args.project_name)
        else:
            print("Error: --project-name is required for validating links.")
    elif args.command == "help":
        reqmaster.help()
    elif args.command == "list-projects":
        reqmaster.list_projects()
    elif args.command == "list-links":
        if args.project_name and args.object_id:
            reqmaster.list_links(args.project_name, args.object_id)
        else:
            print("Error: --project-name and --object-id are required for listing links.")
