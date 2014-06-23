import imp
import os

module_name = "specy"

test_dir = os.path.realpath(__file__)
core_path = test_dir.rsplit('/',2)[0] 


f, filename, description = imp.find_module(module_name, [core_path])

pyspec = imp.load_module(module_name, f, filename, description)    
