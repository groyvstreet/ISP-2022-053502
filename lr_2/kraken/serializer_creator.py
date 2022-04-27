from abc import ABC
from kraken.json_serializer import JsonSerializer
from kraken.yaml_serializer import YamlSerializer
from kraken.toml_serializer import TomlSerializer
from typing import *


class SerializerCreator(ABC):
    @staticmethod
    def create_serializer(s_type: str) -> Any:
        """Returns the serializer of the format specified in the received string."""
        if s_type == 'json':
            return JsonSerializer()
        if s_type == 'yaml':
            return YamlSerializer()
        if s_type == 'toml':
            return TomlSerializer()
        return None
