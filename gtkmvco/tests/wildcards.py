import _importer

import gtkmvc

class Person(gtkmvc.Model):
    __observables__ = ('name', 'age')

    @gtkmvc.Model.getter('*')
    def calculate(self, name):
        return 0

assert Person().name == 0
