import _importer

from gtkmvc import Model, Observer

class Adder(Model):
    # With None the sum getter would raise on getting the "old" value for
    # the notification fired by the assignment in our constructor.
    numbers = tuple()

    __observables__ = ('numbers', 'sum')

    def __init__(self):
        Model.__init__(self)
        # Assignment to property only works after init.
        self.numbers = []

    @Model.getter(deps=['numbers'])
    def sum(self):
        return sum(self.numbers)

class Display(Observer):
    # Adding after=True makes no difference.
    @Observer.observe('sum', assign=True)
    def notify(self, model, name, info):
        print info.new

m = Adder()
o = Display(m)
m.numbers = [1] # notifies
m.numbers.append(2) # does not notify
