"""keyboard_controller controller."""

import sys, os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, parent_dir)

from hexapod import Hexapod

# main Python program
controller = Hexapod()
controller.run()