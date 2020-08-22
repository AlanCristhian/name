from __future__ import annotations

import unittest

import name
import _module
import _library._inner  # type: ignore[import]


class AutoNameSuite(unittest.TestCase):
    def test_object_instance(self) -> None:
        obj = name.AutoName()
        self.assertTrue(isinstance(obj, name.AutoName))

    def test_single_assignment(self) -> None:
        obj = name.AutoName()
        self.assertEqual(obj.__name__, "obj")

    def test_multiple_assignment(self) -> None:
        a = b = name.AutoName()
        self.assertEqual(a.__name__, "b")
        self.assertEqual(b.__name__, "b")

    def test_unpacking(self) -> None:
        x, y = name.AutoName(2)
        self.assertEqual(x.__name__, "x")
        self.assertEqual(y.__name__, "y")

    def test_count_sign(self) -> None:
        description = "Expected positive 'int' number, got '-2'"
        with self.assertRaisesRegex(AssertionError, description):
            x, y = name.AutoName(-2)

    def test_subclass(self) -> None:
        class SubClass(name.AutoName):
            def __init__(self, count: int = 0) -> None:
                super().__init__(count)
        obj = SubClass()
        self.assertEqual(obj.__name__, "obj")

    def test_multiple_inheritance(self) -> None:
        class Numeric:
            def __init__(self, type: object) -> None:
                self.__type__ = type

        class Symbol(Numeric, name.AutoName):
            def __init__(self, type: object, count: int = 0) -> None:
                Numeric.__init__(self, type)
                name.AutoName.__init__(self, count)

        x = Symbol(complex)
        self.assertEqual(x.__name__, "x")
        self.assertEqual(x.__type__, complex)

    def test_assigned_name_in_a_method_of_the_child_class(self) -> None:
        """ Test the stored name in a method of a class that inherit from
        `name.AutoName`.
        """
        class Atom(name.AutoName):
            def __init__(self, count: int = 0) -> None:
                super().__init__(count)

            def __repr__(self) -> str:
                return self.__name__

        a, b, c = Atom(3)
        self.assertEqual(repr((a, b, c)), "(a, b, c)")

    def test_assigned_name_in_a_namespace(self) -> None:
        class Namespace:
            attr = name.AutoName()
        self.assertEqual(Namespace.attr.__name__, "attr")

    def test_assigned_name_in_a_property_method(self) -> None:
        class Number(name.AutoName):
            @property
            def name(self):
                return self.__name__
        n = Number()
        self.assertEqual(n.name, "n")

    def test_multiple_assignment_in_namespace(self) -> None:
        class Multiple:
            attr_1 = attr_2 = name.AutoName()
        self.assertEqual(Multiple.attr_1.__name__, "attr_2")
        self.assertEqual(Multiple.attr_2.__name__, "attr_2")

    def test_single_assignment_in_context_manager(self) -> None:
        with name.AutoName() as context_obj:
            self.assertEqual(context_obj.__name__, "context_obj")

    def test_multiple_assignment_in_context_manager(self) -> None:
        with name.AutoName(2) as (context_ob_1, context_ob_2):
            self.assertEqual(context_ob_1.__name__, "context_ob_1")
            self.assertEqual(context_ob_2.__name__, "context_ob_2")


class ModuleSuite(unittest.TestCase):
    def test_single_assignment_in_module(self) -> None:
        self.assertEqual(_module.obj_1.__name__, "obj_1")

    def test_multiple_assignment_in_module(self) -> None:
        self.assertEqual(_module.a.__name__, "a")
        self.assertEqual(_module.b.__name__, "a")

    def test_unpacking_in_module(self) -> None:
        self.assertEqual(_module.c.__name__, "c")
        self.assertEqual(_module.d.__name__, "d")

    def test_subclass(self) -> None:
        self.assertEqual(_module.obj_2.__name__, "obj_2")

    def test_multiple_inheritance(self) -> None:
        self.assertEqual(_module.obj_3.__name__, "obj_3")
        self.assertEqual(_module.obj_3.__type__, complex)

    def test_assigned_name_in_a_method_of_the_child_class(self) -> None:
        """ Test the stored name in a method of a class that inherit from
        `name.AutoName`.
        """
        expected = repr((_module.e, _module.f, _module.g))
        self.assertEqual(expected, "(e, f, g)")

    def test_assigned_name_in_a_namespace(self) -> None:
        self.assertEqual(_module.Namespace.attr.__name__, "attr")


class LibrarySuite(unittest.TestCase):
    def test_single_assignment_in_module(self) -> None:
        self.assertEqual(_library._inner.obj_1.__name__, "obj_1")

    def test_multiple_assignment_in_module(self) -> None:
        self.assertEqual(_library._inner.a.__name__, "a")
        self.assertEqual(_library._inner.b.__name__, "a")

    def test_unpacking_in_module(self) -> None:
        self.assertEqual(_library._inner.c.__name__, "c")
        self.assertEqual(_library._inner.d.__name__, "d")

    def test_subclass(self) -> None:
        self.assertEqual(_library._inner.obj_2.__name__, "obj_2")

    def test_multiple_inheritance(self) -> None:
        self.assertEqual(_library._inner.obj_3.__name__, "obj_3")
        self.assertEqual(_library._inner.obj_3.__type__, complex)

    def test_assigned_name_in_a_method_of_the_child_class(self) -> None:
        """ Test the stored name in a method of a class that inherit from
        `name.AutoName`.
        """
        expected = repr((_library._inner.e, _library._inner.f,
                         _library._inner.g))
        self.assertEqual(expected, "(e, f, g)")

    def test_assigned_name_in_a_namespace(self) -> None:
        self.assertEqual(_library._inner.Namespace.attr.__name__, "attr")


if __name__ == '__main__':
    unittest.main()
