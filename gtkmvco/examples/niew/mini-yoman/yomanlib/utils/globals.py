##  ===========================================================================
##  This file is part of Yoman, a notebook program.
##
##  Author: Baruch Even <baruch@ev-en.org>
##
##  Copyright (c) 2006 by Baruch Even
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 2 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License along
##  with this program; if not, write to the Free Software Foundation, Inc.,
##  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##
##  The author may be contact at his email <baruch@ev-en.org>.
##
##  ===========================================================================

import sys
import os

if sys.argv[0]: top_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
else: top_dir = "."
    
# A set of global vars
TOPDIR = top_dir
GLADE_DIR = os.path.join(TOPDIR, "glade")

