from kraken.serializer import Serializer
import inspect
import yaml
import io


class YamlSerializer(Serializer):
    def dump(self, _object: object, file_path: str) -> None:
        """Serializes the received object into a yaml format string and writes it to the specified file."""
        yaml_string = self.dumps(_object)
        file = open(file_path, 'w')
        file.write(yaml_string)
        file.close()

    def dumps(self, _object: object) -> str:
        """Serializes the received object into a yaml format string and returns it."""
        dictionary = {}
        if inspect.isfunction(_object):
            dictionary = self.function_to_dictionary(_object)
        elif inspect.isclass(_object):
            dictionary = self.class_to_dictionary(_object)
        yaml_string = yaml.dump(dictionary)
        return yaml_string

    def load(self, file_path: str) -> object:
        """Deserializes an object from a string read from the received file."""
        file = open(file_path, 'r')
        yaml_string = ''
        for line in file:
            yaml_string += line
        file.close()
        return self.loads(yaml_string)

    def loads(self, yaml_string: str) -> object:
        """Deserializes an object from the given string and returns it."""
        stream = io.StringIO(yaml_string)
        dictionary = yaml.load(stream, yaml.Loader)
        _object = None
        if dictionary['__type__'] == 'function':
            _object = self.dictionary_to_function(dictionary)
        elif dictionary['__type__'] == 'class':
            _object = self.dictionary_to_class(dictionary)
        return _object
