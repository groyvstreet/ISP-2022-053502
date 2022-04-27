from kraken.serializer import Serializer
import inspect
from typing import *


class JsonSerializer(Serializer):
    def dump(self, _object: object, file_path: str) -> None:
        """Serializes the received object into a json format string and writes it to the specified file."""
        json = self.dumps(_object)
        file = open(file_path, 'w')
        file.write(json + '\n')
        file.close()

    def dumps(self, _object: object) -> str:
        """Serializes the received object into a json format string and returns it."""
        dictionary = {}
        if inspect.isfunction(_object):
            dictionary = self.function_to_dictionary(_object)
        elif inspect.isclass(_object):
            dictionary = self.class_to_dictionary(_object)
        json = self.dictionary_to_json(dictionary)
        return json

    def load(self, file_path: str) -> object:
        """Deserializes an object from a string read from the received file."""
        file = open(file_path, 'r')
        json = ''
        for line in file:
            json += line
        file.close()
        return self.loads(json)

    def loads(self, json: str) -> object:
        """Deserializes an object from the given string and returns it."""
        dictionary = self.json_to_dictionary(json)
        _object = None
        if dictionary['__type__'] == 'function':
            _object = self.dictionary_to_function(dictionary)
        elif dictionary['__type__'] == 'class':
            _object = self.dictionary_to_class(dictionary)
        return _object

    def dictionary_to_json(self, dictionary: dict, level=1) -> str:
        """Converts dictionary to json format string."""
        json = '{\n'
        count = 0
        for key, value in dictionary.items():
            json += '\t' * level + self.value_to_json(key) + ': '
            if isinstance(value, dict):
                json += self.dictionary_to_json(value, level + 1)
            elif isinstance(value, (list, tuple, set, frozenset)):
                json += self.list_to_json(value, level + 1)
            else:
                json += self.value_to_json(value)
            json += '\n' if count == len(dictionary) - 1 else ',\n'
            count += 1
        json += '\t' * (level - 1) + '}'
        return json

    def list_to_json(self, _list: list, level: int) -> str:
        """Converts list to json format string."""
        json = '[\n'
        for i in range(len(_list)):
            json += '\t' * level + self.value_to_json(_list[i], level + 1) + ('\n' if i == len(_list) - 1 else ',\n')
        json += '\t' * (level - 1) + ']'
        return json

    def json_to_dictionary(self, json: str) -> Dict[Any, Any]:
        """Converts json format string to dictionary."""
        dictionary = {}
        key = ''
        value = ''
        key_writing = False
        value_writing = False
        close = ''
        close_setting = False
        count = 0
        for i in range(len(json)):
            if json[i] == '"' and not value_writing and not close_setting:
                if not key_writing:
                    key_writing = True
                    continue
                else:
                    key_writing = False
                    continue
            if json[i] == ' ' and not key_writing and not value_writing:
                close_setting = True
                continue
            if close_setting:
                close_setting = False
                if json[i] == '"':
                    close = '"'
                    count -= 1
                elif json[i] == '[':
                    close = ']'
                elif json[i] == '{':
                    close = '}'
                else:
                    close = '\n'
                    count -= 1
                    value += json[i]
                value_writing = True
                continue
            if key_writing:
                key += json[i]
            if value_writing:
                if (close == '}' and json[i] == '{') or (close == ']' and json[i] == '[') or \
                        (close == ')' and json[i] == '('):
                    count += 1
                if (close == '}' and json[i] == '}') or (close == ']' and json[i] == ']') or \
                        (close == ')' and json[i] == ')'):
                    count -= 1
                if (json[i] == close and count == -1) or (close == '\n' and (json[i] == ',' or json[i] == '\n')):
                    value_writing = False
                    if json[i] == '"':
                        dictionary[key] = self.json_to_value(value)
                    elif json[i] == ']':
                        dictionary[key] = self.json_to_list(value)
                    elif json[i] == '}':
                        dictionary[key] = self.json_to_dictionary(value)
                    else:
                        dictionary[key] = self.json_to_value(value)
                    key = ''
                    value = ''
                    close = ''
                    count = 0
                else:
                    value += json[i]
        return dictionary

    def json_to_list(self, json: str) -> List[Any]:
        """Converts json format string to list."""
        _list = []
        value = ''
        value_writing = False
        close = ''
        count = 0
        for i in range(len(json) - 1):
            if json[i] == '\t' and not json[i + 1] == '\t' and not value_writing:
                value_writing = True
                if json[i + 1] == '{':
                    close = '}'
                if json[i + 1] == '[':
                    close = ']'
                continue
            if close == '}' or close == ']':
                if (close == '}' and json[i] == '{') or (close == ']' and json[i] == '[') or \
                        (close == ')' and json[i] == '('):
                    count += 1
                if (close == '}' and json[i] == '}') or (close == ']' and json[i] == ']') or \
                        (close == ')' and json[i] == ')'):
                    count -= 1
                if json[i] == close and count == 0:
                    value_writing = False
                    if json[i] == ']':
                        _list.append(self.json_to_list(value))
                    elif json[i] == '}':
                        _list.append(self.json_to_dictionary(value))
                    value = ''
                    close = ''
            else:
                if (json[i] == ',' and json[i + 1] == '\n') or json[i] == '\n':
                    value_writing = False
                    if not value == '':
                        _list.append(self.json_to_value(value))
                    value = ''
            if value_writing:
                value += json[i]
        return _list

    def json_to_value(self, json: str) -> Any:
        """Converts json format string to value."""
        if json.isdigit() or (json[0] == '-' and json.replace('-', '').isdigit()):
            return int(json)
        if '.' in json:
            temp = json.replace('.', '', 1)
            temp = self.json_to_value(temp)
            if isinstance(temp, int):
                return float(json)
        if json == 'true':
            return True
        if json == 'false':
            return False
        if json == 'null':
            return None
        if json[0] == '"':
            return json[1:-1]
        return json

    def value_to_json(self, value: Any, level=0) -> str:
        """Converts value to json format string."""
        if isinstance(value, str):
            return '"' + value + '"'
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, dict):
            return self.dictionary_to_json(value, level)
        if isinstance(value, list):
            return self.list_to_json(value, level)
        return 'null'
