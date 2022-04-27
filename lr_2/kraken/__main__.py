import argparse
from typing import *
from kraken.serializer_creator import SerializerCreator
from pathlib import Path


format_types = ['json', 'yaml', 'toml']


def convert(_list: List[Dict[str, str]]) -> None:
    """Iterates through the list of dictionaries, where the key is the path to the file, and the value is the type of
    format to which the conversion takes place."""
    for elem in _list:
        key = list(elem.keys())[0]
        value = list(elem.values())[0]
        format_type = key[-4:]
        if format_type == value:
            print(f'{key} to {value}: from and to format types are the same')
        else:
            _object = None
            if format_type in format_types:
                _object = SerializerCreator.create_serializer(format_type).load(key)
            else:
                print(f'{key}: unsupported format type')
                continue
            value = value.lower()
            if value in format_types:
                SerializerCreator.create_serializer(value).dump(_object, key[0:-4] + value)
                print(f'{key} to {value}: converted')
            else:
                print(f'{key} to {value}: unsupported format type')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help="path to config file")
    parser.add_argument('-f', '--file', dest='files', action='append', help="path to file")
    parser.add_argument('-t', '--type', dest='types', action='append', help="format type")
    args = parser.parse_args()
    try:
        if args.config:
            config = args.config
            lines = Path(config).read_text().splitlines()
            _list = []
            count = 0
            for line in lines:
                count += 1
                temp = line.split()
                if len(temp) == 2:
                    _list.append({temp[0]: temp[1]})
                else:
                    print(f'incorrect input from config file: line {count}')
            convert(_list)
        elif args.files and args.types:
            files = args.files
            types = args.types
            if len(files) == len(types):
                _list = []
                for i in range(len(files)):
                    _list.append({files[i]: types[i]})
                convert(_list)
            else:
                print('incorrect input: different number of files and format types')
    except FileNotFoundError:
        print('one or more files not found')
