
class When():
    def __init__(self, target):
        self.target = target

    @property
    def then(self):
        return self

    @property
    def it(self):
        return self    

    def called_with(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self

    def init_with(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self

    def raises(self, exception):
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

    def returns(self, expected_value):
        assert self.target(*self.args, **self.kwargs) == expected_value

def when(*args, **kwargs):
    return When(*args, **kwargs)

class Item():
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

def item(*args, **kwargs):
    return Item(*args, **kwargs)