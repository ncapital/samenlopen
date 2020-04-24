from dataclasses import dataclass

from exceptions import *
from resources import keygens


@dataclass
class Resources:
    RESOURCE_0 = 'r0'
    RESOURCE_1 = 'r1'


class ResourceHandler:
    resource_map = dict()

    @classmethod
    def get_resource_handler(cls, resource_name):
        keygen = keygens.get(resource_name)
        if not keygen:
            raise UnknownResource(resource_name)

        return keygen


RESOURCE_MAP = dict()  # resource_name: resource_obj
