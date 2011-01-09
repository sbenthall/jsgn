#!/usr/bin/env python

"""
doctest runner
"""

import doctest
import os

def run_tests():
    directory = os.path.dirname(os.path.abspath(__file__))
    extraglobs = {'here': directory}
    tests =  [ test for test in os.listdir(directory)
               if test.endswith('.txt') ]
    for test in tests:
        doctest.testfile(test, extraglobs=extraglobs)

if __name__ == '__main__':
    run_tests()

