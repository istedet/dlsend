import yaml


def load_file():
    with open('commands.yaml', 'r') as file:
        commands_dict = yaml.full_load(file)

        return commands_dict['commands']


def save_file(list):
    with open('commands.yaml', 'r') as file:
        print('saved')
