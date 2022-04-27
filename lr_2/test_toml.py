import unittest
from kraken.toml_serializer import TomlSerializer
from test_objects.test_functions import *
from test_objects.test_classes import *


class TestToml(unittest.TestCase):
    toml = TomlSerializer()
    func_path = 'test_output/toml/function/'
    class_path = 'test_output/toml/class/'

    def test_function1(self):
        self.toml.dump(test_func1, self.func_path + 'func1.toml')
        f = self.toml.load(self.func_path + 'func1.toml')
        self.assertEqual(test_func1(1), f(1))

    def test_function2(self):
        self.toml.dump(test_func2, self.func_path + 'func2.toml')
        f = self.toml.load(self.func_path + 'func2.toml')
        self.assertEqual(test_func2(-2), f(-2))

    def test_function3(self):
        self.toml.dump(test_func3, self.func_path + 'func3.toml')
        f = self.toml.load(self.func_path + 'func3.toml')
        self.assertEqual(test_func3(3), f(3))

    def test_function4(self):
        self.toml.dump(test_func4, self.func_path + 'func4.toml')
        f = self.toml.load(self.func_path + 'func4.toml')
        self.assertEqual(test_func4(-4), f(-4))

    def test_function5(self):
        self.toml.dump(test_func5, self.func_path + 'func5.toml')
        f = self.toml.load(self.func_path + 'func5.toml')
        self.assertEqual(test_func5(5), f(5))

    def test_function6(self):
        self.toml.dump(test_func6, self.func_path + 'func6.toml')
        f = self.toml.load(self.func_path + 'func6.toml')
        self.assertEqual(test_func6(-0.1), f(-0.1))

    def test_function7(self):
        self.toml.dump(test_func7, self.func_path + 'func7.toml')
        f = self.toml.load(self.func_path + 'func7.toml')
        self.assertEqual(test_func7(87), f(87))

    def test_function8(self):
        self.toml.dump(test_func8, self.func_path + 'func8.toml')
        f = self.toml.load(self.func_path + 'func8.toml')
        self.assertEqual(test_func8(-123.123), f(-123.123))

    def test_function9(self):
        self.toml.dump(test_func9, self.func_path + 'func9.toml')
        f = self.toml.load(self.func_path + 'func9.toml')
        self.assertEqual(test_func9(9.09), f(9.09))

    def test_function10(self):
        self.toml.dump(test_func10, self.func_path + 'func10.toml')
        f = self.toml.load(self.func_path + 'func10.toml')
        self.assertEqual(test_func10(-10), f(-10))

    def test_class1(self):
        obj1 = TestClass1()
        self.toml.dump(TestClass1, self.class_path + 'class1.toml')
        _class = self.toml.load(self.class_path + 'class1.toml')
        obj2 = _class()
        self.assertEqual(obj1.field1, obj2.field1)
        self.assertEqual(obj1.field2, obj2.field2)
        self.assertEqual(obj1.field3, obj2.field3)
        self.assertEqual(obj1.field0, obj2.field0)

    def test_class2(self):
        obj1 = TestClass2()
        self.toml.dump(TestClass2, self.class_path + 'class2.toml')
        _class = self.toml.load(self.class_path + 'class2.toml')
        obj2 = _class()
        self.assertEqual(obj1.field1, obj2.field1)
        self.assertEqual(obj1.field2, obj2.field2)
        self.assertEqual(obj1.field3, obj2.field3)
        self.assertEqual(obj1.field4, obj2.field4)
        self.assertEqual(obj1.field5, obj2.field5)
        self.assertEqual(obj1.field6, obj2.field6)
        self.assertEqual(obj1.field7, obj2.field7)
        self.assertEqual(obj1.field0, obj2.field0)

    def test_class3(self):
        obj1 = TestClass3()
        self.toml.dump(TestClass3, self.class_path + 'class3.toml')
        _class = self.toml.load(self.class_path + 'class3.toml')
        obj2 = _class()
        self.assertEqual(obj1.field1, obj2.field1)
        self.assertEqual(obj1.field2, obj2.field2)
        self.assertEqual(obj1.field3, obj2.field3)
        self.assertEqual(obj1.field4, obj2.field4)
        self.assertEqual(obj1.field5, obj2.field5)
        self.assertEqual(obj1.field6, obj2.field6)
        self.assertEqual(obj1.field7, obj2.field7)
        self.assertEqual(obj1.field0, obj2.field0)
        self.assertEqual(obj1.f(), obj2.f())
        self.assertEqual(obj1.f2(), obj2.f2())

    def test_class4(self):
        obj1 = TestClass4()
        self.toml.dump(TestClass4, self.class_path + 'class4.toml')
        _class = self.toml.load(self.class_path + 'class4.toml')
        obj2 = _class()
        self.assertEqual(obj1.field8, obj2.field8)
        self.assertEqual(obj1.f4(), obj2.f4())

    def test_class5(self):
        obj1 = TestClass5()
        self.toml.dump(TestClass5, self.class_path + 'class5.toml')
        _class = self.toml.load(self.class_path + 'class5.toml')
        obj2 = _class()
        self.assertEqual(obj1.field1, obj2.field1)
        self.assertEqual(obj1.field2, obj2.field2)
        self.assertEqual(obj1.field3, obj2.field3)
        self.assertEqual(obj1.field4, obj2.field4)
        self.assertEqual(obj1.field5, obj2.field5)
        self.assertEqual(obj1.field6, obj2.field6)
        self.assertEqual(obj1.field7, obj2.field7)
        self.assertEqual(obj1.field8, obj2.field8)
        self.assertEqual(obj1.field0, obj2.field0)
        self.assertEqual(obj1.f(), obj2.f())
        self.assertEqual(obj1.f2(), obj2.f2())
        self.assertEqual(obj1.f4(), obj2.f4())
        self.assertEqual(obj1.A().fieldA, obj2.A().fieldA)
        self.assertEqual(obj1.A().B().fieldB, obj2.A().B().fieldB)


if __name__ == '__main__':
    unittest.main()
