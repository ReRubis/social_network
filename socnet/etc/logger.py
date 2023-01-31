import asyncio
import os
from datetime import datetime
from typing import Callable

import yaml


def create_logs_yaml():
    file_name = "logs.yaml"

    if not os.path.exists(file_name):
        data = {'the log': 'data'}
        with open(file_name, "w") as file:
            yaml.dump(data, file)


def logsomething(func: Callable):
    def wrapper(*args, **kwargs):
        file_name = "logs.yaml"

        with open(file_name, "a") as file:
            data = {f'some user called for {func.__name__}': f'{datetime.now()}'}
            yaml.dump(data, file)

        return func(*args, **kwargs)

    return wrapper
