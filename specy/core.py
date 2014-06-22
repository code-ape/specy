
import inspect    

func_dict = []
pre_funcs = []

head_frame = None

def end():
    test_local_vars = get_local_vars()

    funcs = clean(test_local_vars)
    funcs_w_line_nu = get_line_numbers(funcs)
    last_func, last_line = get_last_func(funcs_w_line_nu)
    print("end calling '%s' on line %d" % (str(last_func), last_line))

    name = last_func.__name__
    kw_vals = last_func.func_code.co_consts
    kw_val = None
    if kw_vals:
        kw_val = kw_vals[0]

    if name == "describe" and kw_val:
        if inspect.isfunction(target) or inspect.isclass(target):
            target = target.__name__

        else:
            target = str(kw_val)
        print("Describing %s" % target)

    if name == "it" and kw_val:
        print("\tit %s" % str(kw_val))

    if name == "before_each":
        pre_funcs.append(last_func)
    else:
        variables = {}
        for func in pre_funcs:
            i = func()
            print(i)
            variables.update(i)

        pre_vars = {}
        gl = head_frame.f_globals
        for name, var in variables.items():
            if name in gl:
                pre_vars[name] = gl[name]
            print("Adding %s with value %s to globals" % (name, var))
            gl[name] = var
        #print("GLOBALS: %s" % str(globals().keys()))
        last_func()
        for name, var in pre_vars.items():
            gl[name] = var


def clean(local_vars):
    good_vars = []
    for name, var in local_vars.items():
        if name[0] != '_' and inspect.isfunction(var):
            if var != end and var != when:
                good_vars.append(var)
    return good_vars

def get_line_numbers(funcs):
    funcs_w_line_nu = []
    for f in funcs:
        line = inspect.getsourcelines(f)[1]
        funcs_w_line_nu.append((f, line))
    return funcs_w_line_nu

def get_local_vars(depth = 1):
    stack = inspect.stack()
    frames = [frame_obj[0] for frame_obj in stack]
    target_frame = frames[depth+1]
    global head_frame
    if not head_frame:
        head_frame = target_frame
    return target_frame.f_locals


def get_last_func(funcs_w_line_nu):
    last_func = None
    last_line = 0
    for func, line in funcs_w_line_nu:
        if line > last_line:
            last_func = func
            last_line = line
    return last_func, last_line
    



class when():
    def __init__(self, target):
        print("when called")
        self.target = target

    @property
    def then(self):
        print("then called")
        return self

    @property
    def it(self):
        print("it called")
        return self    

    def called_with(self, *args, **kwargs):
        print("called_with called")
        self.args = args
        self.kwargs = kwargs
        return self

    def init_with(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self

    def raises(self, exception):
        print("raises called")
        raised = False
        try:
            self.target(self.args, self.kwargs)
        except exception:
            raised = True
        assert raised

   
    def fails(self):
        return self.raises(Exception)

    def fails_with(self, exception):
        return self.raises(exception)

class item():
    def __init__(self, target):
        self.target = target

    @property
    def should(self):
        return self

    @property
    def be(self):
        return self

    def instance_of(self, target_class):
        assert isinstance(self.target, target_class)






