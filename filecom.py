import yaml


def load_file():
    # Read from the file and return the "commands" dictionary as a list
    with open('commands.yaml', 'r') as file:
        commands_dict = yaml.full_load(file)

        return commands_dict['commands']


def save_file(dict):
    # save to the file
    with open('commands.yaml', 'w') as file:
        documents = yaml.dump(dict, file)
