import _importer

from gtkmvc import Model, Observer

class Adder(Model):
    a = 0
    b = 0

    __observables__ = ('a', 'b', 'sum')

    @Model.getter(deps=('a', 'b'))
    def sum(self):
        return self.a + self.b

class Display(Observer):
    @Observer.observe('sum', assign=True)
    def notify(self, model, name, info):
        print self.prompt, info.new

# TODO unittest

m = Adder()
o = Display(m, spurious=False)
o.prompt = "Frugal"
p = Display(m, spurious=True)
p.prompt = "Spurious"
m.a = 0 # works as expected
