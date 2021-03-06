#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.datatypes import Entity, Classes, Parameters, Applications
import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock

@mock.patch.multiple('reclass.datatypes', autospec=True, Classes=mock.DEFAULT,
                     Applications=mock.DEFAULT,
                     Parameters=mock.DEFAULT)
class TestEntity(unittest.TestCase):

    def _make_instances(self, Classes, Applications, Parameters):
        return Classes(), Applications(), Parameters()

    def test_constructor_default(self, **mocks):
        # Actually test the real objects by calling the default constructor,
        # all other tests shall pass instances to the constructor
        e = Entity()
        self.assertEqual(e.name, '')
        self.assertIsInstance(e.classes, Classes)
        self.assertIsInstance(e.applications, Applications)
        self.assertIsInstance(e.parameters, Parameters)

    def test_constructor_empty(self, **types):
        instances = self._make_instances(**types)
        e = Entity(*instances)
        self.assertEqual(e.name, '')
        cl, al, pl = [getattr(i, '__len__') for i in instances]
        self.assertEqual(len(e.classes), cl.return_value)
        cl.assert_called_once_with()
        self.assertEqual(len(e.applications), al.return_value)
        al.assert_called_once_with()
        self.assertEqual(len(e.parameters), pl.return_value)
        pl.assert_called_once_with()

    def test_constructor_empty_named(self, **types):
        name = 'empty'
        e = Entity(*self._make_instances(**types), name=name)
        self.assertEqual(e.name, name)

    def test_equal_empty(self, **types):
        instances = self._make_instances(**types)
        self.assertEqual(Entity(*instances), Entity(*instances))
        for i in instances:
            i.__eq__.assert_called_once_with(i)

    def test_equal_empty_named(self, **types):
        instances = self._make_instances(**types)
        self.assertEqual(Entity(*instances), Entity(*instances))
        name = 'empty'
        self.assertEqual(Entity(*instances, name=name),
                         Entity(*instances, name=name))

    def test_unequal_empty_named(self, **types):
        instances = self._make_instances(**types)
        name = 'empty'
        self.assertNotEqual(Entity(*instances, name='empty'),
                            Entity(*instances, name='ytpme'))
        for i in instances:
            i.__eq__.assert_called_once_with(i)

    def _test_constructor_wrong_types(self, which_replace, **types):
        instances = self._make_instances(**types)
        instances[which_replace] = 'Invalid type'
        e = Entity(*instances)

    def test_constructor_wrong_type_classes(self, **types):
        self.assertRaises(TypeError, self._test_constructor_wrong_types, 0)

    def test_constructor_wrong_type_applications(self, **types):
        self.assertRaises(TypeError, self._test_constructor_wrong_types, 1)

    def test_constructor_wrong_type_parameters(self, **types):
        self.assertRaises(TypeError, self._test_constructor_wrong_types, 2)

    def test_merge(self, **types):
        instances = self._make_instances(**types)
        e = Entity(*instances)
        e.merge(e)
        for i, fn in zip(instances, ('merge_unique', 'merge_unique', 'merge')):
            getattr(i, fn).assert_called_once_with(i)

    def test_merge_newname(self, **types):
        instances = self._make_instances(**types)
        newname = 'newname'
        e1 = Entity(*instances, name='oldname')
        e2 = Entity(*instances, name=newname)
        e1.merge(e2)
        self.assertEqual(e1.name, newname)

if __name__ == '__main__':
    unittest.main()
