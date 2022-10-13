# -*- coding: utf-8 -*-
"""
Fritt upplagd balk

@author: Jonas Lindemann
"""

import os

os.add_dll_directory(os.path.join(os.getcwd(), "./beam/.libs"))

from beam import *

if __name__ == "__main__":

    print(beam_model.moments.__doc__)
