from exceptions import *
from resources import keygens


class ResourceHandler:
    resource_map = dict()

    @classmethod
    def get_resource_handler(cls, resource_name):
        keygen = keygens.get(resource_name)
        if not keygen:
            raise UnknownResource(resource_name)

        return keygen
