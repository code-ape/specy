
import traceback
import sys
import inspect

class TestBlock():
    def __init__(self, method=None, parent_block=None, frame=None):
        self.parent_block   = None
        self.child_blocks   = []

        self.method         = None
        self.frame          = frame
        self.block_kwargs   = None
        self.before_each    = None
        self.after_each     = None
        self.set_up         = None
        self.tear_down      = None
        self.block_name     = ""
        self.description    = ""

        self.passed         = None
        self.children_passed    = None

        self.returned_val   = None
        self.exception_type = None
        self.exception_val  = None
        self.traceback      = None

        self.global_var_storage = None

        if method:
            self.register_method(method)
        if parent_block:
            self.register_parent()

    def __repr__(self):
        s = "<TestBlock, block_name=%s, method=%s>" % (self.block_name, self.method)
        return s

    def register_method(self, method):
        self.method      = method
        self.block_name  = method.__name__
        #print("Block name: %s" % self.block_name)

        self.block_kwargs = get_keyword_defaults(self.method)
        if self.block_kwargs:
            arg = self.block_kwargs[0]
            kind = is_method_or_class(arg)
            if kind:
                target_name = arg.__name__
                target_type = kind
                self.description = "%s '%s'" % (target_type, target_name)
            else:
                self.description = arg
        else:
            self.description = self.block_name


    def register_parent(self, parent_block):
        self.parent_block = parent_block
        parent_block.child_blocks.append(self)

        self.before_each  = self.get_sibling("before_each")
        self.after_each   = self.get_sibling("after_each")


    def get_sibling(self, name):
        func = None
        if name == self.block_name:
            return func

        for b in self.parent_block.child_blocks:
            if b.block_name == name:
                func = b.method
        return func


    def run_block(self):
        self.prep_env()
        try:
            self.returned_val = self.method()
            self.passed = True
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.exception_type = exc_type
            self.exception_val  = exc_value
            self.traceback      = exc_traceback
            self.passed = False

        if self.block_name == "it":
            if self.passed:
                sys.stdout.write(".")
            else:
                sys.stdout.write("x")
        self.reset_env()


    def prep_env(self):
        variables = {}
        if self.before_each:
            variables = self.before_each()

        pre_vars = {}
        gl = self.frame.f_globals
        for name, var in variables.items():
            if name in gl:
                pre_vars[name] = gl[name]
            gl[name] = var
        self.global_var_storage = pre_vars

    def reset_env(self):
        gl = self.frame.f_globals
        for name, var in self.global_var_storage.items():
            gl[name] = var






def get_keyword_defaults(method):
    kw = inspect.getargspec(method).defaults
    return kw

def is_method_or_class(obj):
    if inspect.isclass(obj):
        return "class"
    if inspect.ismethod(obj):
        return "method"
    else:
        return None
