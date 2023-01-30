import os
import yaml
from typing import Callable
from datetime import datetime


def create_logs_yaml():
    file_name = "logs.yaml"

    if not os.path.exists(file_name):
        data = {'the log': 'data'}
        with open(file_name, "w") as file:
            yaml.dump(data, file)


def logsomething(func: Callable):
    def wrapper():
        file_name = "logs.yaml"

        with open(file_name, "a") as file:

            data = {f'some user called for {func.__name__}': f'{datetime.now()}'}
            yaml.dump(data, file)

        func()
        print('something2')

    return wrapper


# @logsomething
# def print_something():
#     print('incurso')


# print_something()
