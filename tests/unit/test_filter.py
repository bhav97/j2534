#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import j2534.filter as filter
import unittest

class TestFilters(unittest.TestCase):
    """ Unit tests for the ``j2534.filter``"""

    def setUp(self):
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_FilterMsg_tomsg4(self):
        filter.Filter.to_msg4(1, 2, 3, 4, [], [])

if __name__=="__main__":
    unittest.main()