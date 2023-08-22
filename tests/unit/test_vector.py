#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from j2534.vector import VectorPassThruXLLibrary
import unittest

""" Run using ``python -m unittest tests.unit.test_vector``
"""

class TestVectorPassThruLoader(unittest.TestCase):
    """ Unit tests for the ``j2534.vector``"""

    def setUp(self):
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_load(self) -> None:
        lib = VectorPassThruXLLibrary()
        assert 1 == 1, "Assertion failure"

if __name__=="__main__":
    unittest.main()