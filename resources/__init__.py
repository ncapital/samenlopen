import glob
import importlib
import os

from helpers import red

keygens = {}

if __name__ == 'bla':
    resources_path = os.path.realpath(__name__)
    for resource in glob.glob(f"{resources_path}/[!_]*.py"):
        # convert from resource.py to resource
        resource = os.path.basename(resource)
        resource = resource.replace('.py', '')

        try:
            module = importlib.import_module(f'resources.{resource}')
            keygens[resource] = module.KeyGen()
        except (ModuleNotFoundError, ImportError) as e:
            print(red(f"WARNING! Can't import resource {resource} from resources!"))
