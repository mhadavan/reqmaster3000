# ReqMaster 3000

ReqMaster 3000 is a lightweight and configurable requirement management tool. It uses JSON files for backend storage and provides a command-line interface for managing projects, objects, and links between objects. The tool supports bi-traceable links and easy object configuration.

The goals with this project is:
 - I as a developer shall learn how to create a open-source project
 - I as a developer shall learn how to benefit from using different AI tools
 - Help other developers by creating a requirement management tool that are up to date

 This project is inspired by the Doorstop project and many other requirement tools I have used during my professional work as a Embedded Software Engineer

## Features

- Easily configurable object types using JSON configuration files.
- Create and manage projects.
- Create and edit various types of objects within projects.
- Bi-traceable links between objects.
- Validate links to ensure integrity.
- List links between objects

## Project Structure

```plaintext
ReqMaster3000/
├── config/
│   └── requirement-config.json
├── projects/
│   ├── Project-A/
│   │   └── objects/
│   │       └── requirement-id-001.json
│   ├── Project-B/
│       └── objects/
│           └── requirement-id-001.json 
└── reqmaster3000.py
```

## Configuration Files
Customize your object types by modifying JSON configuration files in the config/ directory. Each object type should have its configuration file.

Example for requirement-config.json:
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

### Note
I have used Python version 3.10 during development of this tool.

## Why 3000 ? ...

Why not? Sounds cool :)

### Commands
#### Create a New Project
Creates a new project with the specified project name.
```
python3 reqmaster3000.py create-project --project-name <PROJECT-NAME>
```
#### Create a New Object
Creates a new object of the specified type within a project. You must specify a unique requirement ID.
```
python reqmaster3000.py create-object --project-name <PROJECT-NAME> --object-type <OBJECT-TYPE> --object-id <OBJECT-ID> --attributes <KEY=VALUE> ...
```
Example:

```
python reqmaster3000.py create-object --project-name Project-A --object-type requirement --object-id req-001 --attributes "Requirement Description=New requirement" "Status=Open" "Verification Method=Inspection"
```
####Edit an Existing Object
Edits an existing object within a project.

```
python reqmaster3000.py edit-object --project-name <PROJECT-NAME> --object-id <OBJECT-ID> --attributes <KEY=VALUE> ...
```
Example:

```
python reqmaster3000.py edit-object --project-name Project-A --object-id req-001 --attributes "Status=Closed"
```
#### Create a Link Between Objects
Creates a bi-traceable link between two objects within a project.

```
python reqmaster3000.py create-link --project-name <PROJECT-NAME> --object-id <OBJECT-ID-1> --object-id-2 <OBJECT-ID-2>
```
Example:

```
python reqmaster3000.py create-link --project-name Project-A --object-id req-001 --object-id-2 req-002
```
#### Validate Links
Validates all links within a project to ensure there are no broken links.

```
python reqmaster3000.py validate-links --project-name <PROJECT-NAME>
```
Example:

```
python reqmaster3000.py validate-links --project-name Project-A
```
#### Example Workflow
Here's a step-by-step example of creating a project, adding objects, linking them, and validating the links:

###Create a Project

```
python reqmaster3000.py create-project --project-name Project-A
```
#### Create a Requirement Object
```
python reqmaster3000.py create-object --project-name Project-A --object-type requirement --object-id req-001 --attributes "Requirement Description=Implement login feature" "Status=Open" "Verification Method=Review"
```
###List Objects and Get Object IDs

Review the objects in projects/Project-A/objects directory to get object IDs.

Create Another Requirement Object

```
python reqmaster3000.py create-object --project-name Project-A --object-type requirement --object-id req-002 --attributes "Requirement Description=Implement logout feature" "Status=Open" "Verification Method=Review"
```
#### Link the Requirement Objects
```
python reqmaster3000.py create-link --project-name Project-A --object-id req-001 --object-id-2 req-002
```
#### Validate Links

```
python reqmaster3000.py validate-links --project-name Project-A
```
## Requirements
Python 3.10 or higher
## License
MIT License

Happy managing your requirements with ReqMaster 3000!
