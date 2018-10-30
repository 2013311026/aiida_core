# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida_core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import collections
import random
import unittest

from aiida.backends.testbase import AiidaTestCase
from six.moves import range


class TestCleanValueConsistency(AiidaTestCase):
    """
    Tests for Node.clean_value that the value after a clean value is the same as when it is
    serialized and deserialized from the database.
    """

    def test_types(self):
        from aiida.orm import Node, load_node

        test_data = {
            'set': {1, 2, 3, None, True, False, 'string'},
            'tuple': (1, 2, 3, None, True, False, 'string'),
            'list': [1, 2, 3, None, True, False, 'string'],
            'dictionary': {
                '1': 1,
                '2': 2,
                '3': 3,
                'a': None,
                'b': True,
                'c': False,
                'd': 'string'
            },
            'ordered_dict':
            collections.OrderedDict({
                '1': 1,
                '2': 2,
                '3': 3,
                'a': None,
                'b': True,
                'c': False,
                'd': 'string'
            }),
            'float_1':
            1.13045876130857013701873290817058713,
            'float_2':
            -2.081263081264983764016240184601286340,
            'float_3':
            1.081263081264983764016240184601286340E-200,
            'float_4':
            -2.081263081264983764016240184601286340E-200,
            'float_5':
            1.081263081264983764016240184601286340E+200,
            'float_6':
            -2.081263081264983764016240184601286340E+200,
        }

        for key, value in test_data.items():
            with self.subTest(key=key):
                node = Node()
                node._set_attr(key, value)
                node_hash = node.get_hash()
                node.store()
                node2 = load_node(node.uuid)
                node2_hash = node2.get_hash()
                self.assertEqual(node_hash, node2_hash)

    def _skip_me_test_types(self):
        """Unskip this test, by removing the '_skip_me_' prefix, to generate new floats for truncation testing."""
        from aiida.orm import Node, load_node

        for exponent in [-250, -200, -100, -50, -10, 0, 10, 50, 100, 200, 250]:
            for i in range(1):
                value = random.random() * 10**exponent
                key = 'float'
                with self.subTest(key='{:.24g}'.format(value)):
                    node = Node()
                    node._set_attr(key, value)
                    node_hash = node.get_hash()
                    node.store()
                    node2 = load_node(node.uuid)
                    node2_hash = node2.get_hash()
                    self.assertEqual(node_hash, node2_hash)
