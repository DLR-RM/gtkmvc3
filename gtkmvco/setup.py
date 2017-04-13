#!/usr/bin/env python

# ----------------------------------------------------------------------
# Author: Ionutz Borcoman <borco@go.ro>
#
# ----------------------------------------------------------------------

from distutils.core import setup
from gtkmvc import get_version

setup(name="python-gtkmvc-dlr",
      version=".".join(map(str, get_version())), 
      description="Model-View-Controller and Observer patterns "\
                  "for developing pygtk-based applications",
      author="Roberto Cavada",
      author_email="roboogle@gmail.com",
      license="LGPL",
      url="http://pygtkmvc.sourceforge.net/",
      packages=['gtkmvc', 'gtkmvc.support', 'gtkmvc.adapters', 'gtkmvc.progen'],
      package_data={'gtkmvc.progen': ['progen.glade']},
      scripts=['scripts/gtkmvc-progen'],

      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: X11 Applications :: GTK Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Software Development :: User Interfaces',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          ],
      
     )
