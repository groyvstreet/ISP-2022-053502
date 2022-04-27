import inspect
import types
import importlib
from abc import ABC, abstractmethod
from typing import *


class Serializer(ABC):
    @abstractmethod
    def dump(self, _object, file_path):
        pass

    @abstractmethod
    def dumps(self, _object):
        pass

    @abstractmethod
    def load(self, file_path):
        pass

    @abstractmethod
    def loads(self, string):
        pass

    def function_to_dictionary(self, function) -> Dict[str, Any]:
        """Serializes a function into a dictionary with a set of its attributes."""
        _globals = {}
        co_names = function.__code__.co_names
        globals_attrs = function.__globals__
        for key, value in globals_attrs.items():
            if key in co_names or self.key_in_co_consts(function.__code__.co_consts, key):
                if inspect.ismodule(value):
                    _globals[key] = 'module'
                else:
                    _globals[key] = value
        code = function.__code__
        code = self.code_to_dictionary(code)
        return {'__type__': 'function', '__name__': function.__name__, '__globals__': _globals, '__code__': code}

    def key_in_co_consts(self, co_consts: list, key: str) -> bool:
        """Returns true if the key is in co_consts, false if not."""
        for elem in co_consts:
            if inspect.iscode(elem):
                if key in elem.co_names or self.key_in_co_consts(elem.co_consts, key):
                    return True
        return False

    def code_to_dictionary(self, code) -> Dict[str, Any]:
        """Serializes code into a dictionary with a set of its attributes."""
        co_consts = []
        for elem in list(code.co_consts):
            if inspect.iscode(elem):
                co_consts.append(self.code_to_dictionary(elem))
            else:
                co_consts.append(elem)
        dictionary = {'co_argcount': code.co_argcount, 'co_posonlyargcount': code.co_posonlyargcount,
                      'co_knowlyargcount': code.co_kwonlyargcount, 'co_nlocals': code.co_nlocals,
                      'co_stacksize': code.co_stacksize, 'co_flags': code.co_flags, 'co_code': list(code.co_code),
                      'co_consts': co_consts, 'co_names': list(code.co_names),
                      'co_varnames': list(code.co_varnames), 'co_filename': code.co_filename, 'co_name': code.co_name,
                      'co_firstlineno': code.co_firstlineno, 'co_lnotab': list(code.co_lnotab),
                      'co_freevars': list(code.co_freevars), 'co_cellvars': list(code.co_cellvars)}
        return dictionary

    def dictionary_to_function(self, dictionary: Dict[str, Any]) -> types.FunctionType:
        """Deserializes a function from a dictionary with a set of its attributes."""
        for key, value in dictionary['__globals__'].items():
            if value == 'module':
                dictionary['__globals__'][key] = importlib.import_module(key)
        dictionary['__globals__']['__builtins__'] = importlib.import_module('builtins')
        code = self.dictionary_to_code(dictionary['__code__'])
        return types.FunctionType(code, dictionary['__globals__'], dictionary['__name__'])

    def dictionary_to_code(self, dictionary: Dict[str, Any]) -> types.CodeType:
        """Deserializes code from a dictionary with a set of its attributes."""
        co_consts = []
        for elem in dictionary['co_consts']:
            if isinstance(elem, dict):
                co_consts.append(self.dictionary_to_code(elem))
            else:
                co_consts.append(elem)
        code = types.CodeType(dictionary['co_argcount'], dictionary['co_posonlyargcount'],
                              dictionary['co_knowlyargcount'], dictionary['co_nlocals'], dictionary['co_stacksize'],
                              dictionary['co_flags'], bytes(dictionary['co_code']), tuple(co_consts),
                              tuple(dictionary['co_names']), tuple(dictionary['co_varnames']),
                              dictionary['co_filename'], dictionary['co_name'], dictionary['co_firstlineno'],
                              bytes(dictionary['co_lnotab']), tuple(dictionary['co_freevars']),
                              tuple(dictionary['co_cellvars']))
        return code

    def class_to_dictionary(self, _class) -> Dict[str, Any]:
        """Serializes the class into a dictionary with its attributes."""
        dictionary = {'__type__': 'class', '__name__': _class.__name__}
        _list = []
        for elem in _class.__bases__:
            _list.append(self.class_to_dictionary(elem))
        dictionary['__bases__'] = _list
        _dict = {}
        dict_attrs = _class.__dict__
        for key, value in dict_attrs.items():
            if len(key) == 1 or (not key[0] == '_' and not key[1] == '_'):
                if isinstance(value, (str, int, float, bool, dict, list, tuple, set, frozenset)):
                    _dict[key] = value
                elif inspect.isfunction(value):
                    _dict[key] = self.function_to_dictionary(value)
                elif inspect.isclass(value):
                    _dict[key] = self.class_to_dictionary(value)
            elif key == '__init__' and inspect.isfunction(value):
                _dict[key] = self.function_to_dictionary(value)
        dictionary['__dict__'] = _dict
        return dictionary

    def dictionary_to_class(self, dictionary: Dict[str, Any]) -> type:
        """Deserializes a class from a dictionary with its attributes."""
        bases = []
        for elem in dictionary['__bases__']:
            bases.append(self.dictionary_to_class(elem))
        for key, value in dictionary['__dict__'].items():
            if isinstance(value, dict) and '__type__' in value.keys():
                if value['__type__'] == 'function':
                    dictionary['__dict__'][key] = self.dictionary_to_function(value)
                elif value['__type__'] == 'class':
                    dictionary['__dict__'][key] = self.dictionary_to_class(value)
        return type(dictionary['__name__'], tuple(bases), dictionary['__dict__'])
