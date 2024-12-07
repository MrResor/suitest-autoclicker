from json import decoder
import sys

from errors import FileEmpty, PathEmpty

def error_info(message: str, code: int):
    print("ERROR! " + message + " or use provided .json files.")
    print('Exitting...')
    sys.exit(code)

def open_file(func):
    def wrapper(self):
        try:
            func(self)
        except FileEmpty:
            error_info('File is empty, ensure it is properly filled', 1)
        except decoder.JSONDecodeError:
            error_info('Given file could not be converted to JSON, please check syntax', 2)
    return wrapper

def json_keys(func):
    def wrapper(self):
        try:
            func(self)
        except KeyError as e:
            print(f'ERROR! No key {e}.')
            error_info('Given JSON file does not contain one or more of the necessary keys, please verify', 3)
    return wrapper

def no_destination(func):
    def wrapper(self, graph:dict, Start:str, Destination:str):
        try:
            path = func(self, graph, Start, Destination)
        except PathEmpty as e:
            print(f'ERROR! No key {e} on the device keyboard.\nExitting...')
            sys.exit(4)
        return path
    return wrapper