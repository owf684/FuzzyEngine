import json


def get_project_directory():
    with open('./project_file.json', 'r') as file:
        project_file = json.load(file)

    if project_file is not None:
        return project_file['current_project']


