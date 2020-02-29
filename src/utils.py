import os
import re

def get_config(config = os.path.join("..", "config.txt")):
    with open(config, "r") as file:
        options = [re.sub(r"^\s|\n$", "", line.split(":")[-1]) for line in file]
    return options