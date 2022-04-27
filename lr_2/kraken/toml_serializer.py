from kraken.serializer import Serializer
from kraken.json_serializer import JsonSerializer
import inspect
import toml
from typing import *


class TomlSerializer(Serializer):
    def dump(self, _object: object, file_path: str) -> None:
        """Serializes the received object into a toml format string and writes it to the specified file."""
        toml_string = self.dumps(_object)
        file = open(file_path, 'w')
        file.write(toml_string)
        file.close()

    def dumps(self, _object: object) -> str:
        """Serializes the received object into a toml format string and returns it."""
        dictionary = {}
        if inspect.isfunction(_object):
            dictionary = self.function_to_dictionary(_object)
            dictionary['__code__']['co_consts'] = self.list_to_bytes(dictionary['__code__']['co_consts'])
        elif inspect.isclass(_object):
            dictionary = self.class_to_dictionary(_object)
            dictionary['__bases__'] = self.list_to_bytes(dictionary['__bases__'])
            dictionary['__dict__'] = self.dictionary_to_bytes(dictionary['__dict__'])
        toml_string = toml.dumps(dictionary)
        return toml_string

    def load(self, file_path: str) -> object:
        """Deserializes an object from a string read from the received file."""
        file = open(file_path, 'r')
        toml_string = ''
        for line in file:
            toml_string += line
        file.close()
        return self.loads(toml_string)

    def loads(self, toml_string: str) -> object:
        """Deserializes an object from the given string and returns it."""
        dictionary = toml.loads(toml_string)
        _object = None
        if dictionary['__type__'] == 'function':
            dictionary['__code__']['co_consts'] = self.bytes_to_list(dictionary['__code__']['co_consts'])
            _object = self.dictionary_to_function(dictionary)
        elif dictionary['__type__'] == 'class':
            dictionary['__bases__'] = self.bytes_to_list(dictionary['__bases__'])
            dictionary['__dict__'] = self.bytes_to_dictionary(dictionary['__dict__'])
            _object = self.dictionary_to_class(dictionary)
        return _object

    @staticmethod
    def list_to_bytes(_list: List[Any]) -> bytes:
        """Converts a list to a json format string and converts the string to bytes."""
        j = JsonSerializer()
        return bytes(j.list_to_json(_list, 1), 'utf-8')

    @staticmethod
    def bytes_to_list(_bytes: bytes) -> List[Any]:
        """Converts bytes to a json format string and converts the string to a list."""
        j = JsonSerializer()
        return j.json_to_list(bytes(_bytes).decode())

    @staticmethod
    def dictionary_to_bytes(_dict: Dict[str, Any]) -> bytes:
        """Converts a dictionary to a json format string and converts the string to bytes."""
        j = JsonSerializer()
        return bytes(j.dictionary_to_json(_dict), 'utf-8')

    @staticmethod
    def bytes_to_dictionary(_bytes: bytes) -> Dict[str, Any]:
        """Converts bytes to a json format string and converts the string to a dictionary."""
        j = JsonSerializer()
        return j.json_to_dictionary(bytes(_bytes).decode())
