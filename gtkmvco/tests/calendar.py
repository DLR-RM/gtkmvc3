import datetime
import unittest

import gtk

from _importer import refresh_gui

import gtkmvc

class Model(gtkmvc.Model):
    date = datetime.date(2011, 12, 24)
    time = datetime.datetime(2011, 12, 24, 18)
    __observables__ = ('date', 'time')

class Date(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.v = v = gtkmvc.View()
        v['window'] = w = gtk.Window()
        v['calendar'] = c = gtk.Calendar()
        w.add(c)
        w.show_all()
        self.c = gtkmvc.Controller(self.m, self.v)
        refresh_gui()
        self.adapt()
        refresh_gui()

    def testAdaption(self):
        # Month is zero-based
        self.assertEqual((2011, 11, 24), self.v['calendar'].get_date())

    def testAssign(self):
        self.m.date = datetime.date(2010, 1, 1)
        self.m.time = datetime.datetime(2010, 1, 1, 1)
        self.assertEqual((2010, 0, 1), self.v['calendar'].get_date())

    def testDay(self):
        self.assertEqual(self.m.date, self.m.time.date())
        self.v['calendar'].select_day(25)
        # Depending on subclass one of them is adapted
        self.assertNotEqual(self.m.date, self.m.time.date())
        # Changing date should keep time
        self.assertEqual(18, self.m.time.hour)

    def adapt(self):
        self.c.adapt('date', 'calendar')

class DateLessCode(Date):
    def adapt(self):
        """
        Controller handles Calendar specially and creates three
        RoUserClassAdapter instances. This is only necessary for datetime
        instances, as regular Adapter doesn't give the getter access to the
        old model value to copy the time. Still, datetime may occur in the
        wild, adapted to a Calendar and two or three SpinButton.
        """
        a = gtkmvc.adapters.Adapter(self.m, 'date')
        def setter(c, d):
            # TODO test if this flickers, maybe add "if new != old"
            c.select_month(d.month - 1, d.year)
            c.select_day(d.day)
        a.connect_widget(
            self.v['calendar'], getter=lambda w: datetime.date(*w.get_date()),
            setter=setter, signal='day-selected')
        self.c.adapt(a)

class Time(Date):
    def adapt(self):
        self.c.adapt('time', 'calendar')        

if __name__ == "__main__":
    unittest.main()
