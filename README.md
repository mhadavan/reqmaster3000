# ReqMaster 3000

ReqMaster 3000 is a lightweight and configurable requirement management tool. It uses JSON files for backend storage and provides a command-line interface for managing projects, objects, and links between objects. The tool ensures bi-traceable links and easy object configuration.

## Features

- Easily configurable object types using JSON configuration files.
- Create and manage projects.
- Create and edit various types of objects within projects.
- Bi-traceable links between objects.
- Validate links to ensure integrity.

## Project Structure

```plaintext
ReqMaster3000/
├── config/
│   └── requirement_config.json
├── projects/
│   ├── Project_A/
│   │   └── objects/
│   │       └── requirement_id_001.json
│   ├── Project_B/
│       └── objects/
│           └── requirement_id_001.json 
└── reqmaster3000.py
```

## Configuration Files
Customize your object types by modifying JSON configuration files in the config/ directory. Each object type should have its configuration file.

Example for requirement_config.json:
```
{
    "fields": [
        "Unique Requirement ID",
        "Requirement Description",
        "Status",
        "Verification Method"
    ]
}
```

## Usage
To use ReqMaster 3000, you need to have Python installed. You can then interact with the tool via the command line.

### Commands
#### Create a New Project
Creates a new project with the specified project name.
```
python reqmaster3000.py create_project --project_name <PROJECT_NAME>
```
#### Create a New Object
Creates a new object of the specified type within a project. You must specify a unique requirement ID.
```
python reqmaster3000.py create_object --project_name <PROJECT_NAME> --object_type <OBJECT_TYPE> --object_id <OBJECT_ID> --attributes <KEY=VALUE> ...
```
Example:

```
python reqmaster3000.py create_object --project_name Project_A --object_type requirement --object_id req_001 --attributes "Requirement Description=New requirement" "Status=Open" "Verification Method=Inspection"
```
####Edit an Existing Object
Edits an existing object within a project.

```
python reqmaster3000.py edit_object --project_name <PROJECT_NAME> --object_id <OBJECT_ID> --attributes <KEY=VALUE> ...
```
Example:

```
python reqmaster3000.py edit_object --project_name Project_A --object_id req_001 --attributes "Status=Closed"
```
#### Create a Link Between Objects
Creates a bi-traceable link between two objects within a project.

```
python reqmaster3000.py create_link --project_name <PROJECT_NAME> --object_id <OBJECT_ID_1> --object_id_2 <OBJECT_ID_2>
```
Example:

```
python reqmaster3000.py create_link --project_name Project_A --object_id req_001 --object_id_2 req_002
```
#### Validate Links
Validates all links within a project to ensure there are no broken links.

```
python reqmaster3000.py validate_links --project_name <PROJECT_NAME>
```
Example:

```
python reqmaster3000.py validate_links --project_name Project_A
```
#### Example Workflow
Here's a step-by-step example of creating a project, adding objects, linking them, and validating the links:

###Create a Project

```
python reqmaster3000.py create_project --project_name Project_A
```
#### Create a Requirement Object
```
python reqmaster3000.py create_object --project_name Project_A --object_type requirement --object_id req_001 --attributes "Requirement Description=Implement login feature" "Status=Open" "Verification Method=Review"
```
###List Objects and Get Object IDs

Review the objects in projects/Project_A/objects directory to get object IDs.

Create Another Requirement Object

```
python reqmaster3000.py create_object --project_name Project_A --object_type requirement --object_id req_002 --attributes "Requirement Description=Implement logout feature" "Status=Open" "Verification Method=Review"
```
#### Link the Requirement Objects
```
python reqmaster3000.py create_link --project_name Project_A --object_id req_001 --object_id_2 req_002
```
#### Validate Links

```
python reqmaster3000.py validate_links --project_name Project_A
```
## Requirements
Python 3.6 or higher
## License
MIT License

Happy managing your requirements with ReqMaster 3000!
