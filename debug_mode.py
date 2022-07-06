# exec(open("./main.py").read())
# http://www.semanticweb.org/fialho/kipo#
from cmath import pi
from owlready2 import *

print('Starting...')
try:
    world = World(filename='/tmp/semantic.sqlite3', exclusive=False)
    onto_path.append('./')
    world.get_ontology('./kipo_fialho.owl').load()
    kipo = world.get_ontology('http://www.semanticweb.org/fialho/kipo#').load()
    sync_reasoner_pellet(x = world, infer_property_values=True, debug = 2)
    world.save()
    print(list(world.inconsistent_classes()))
        
except Exception as e:
    print(e)

print("Loaded")
