import math
import inspect


class TestClass1:
    field1 = 'field1'
    field2 = 1
    field3 = 1.1

    def __init__(self):
        self.field0 = 0


class TestClass2(TestClass1):
    field4 = True
    field5 = False
    field6 = [1, 2, 3, 4, 5]
    field7 = {'key1': 1, 'key2': 2}


class TestClass3(TestClass2):
    def f(self):
        return self.field1

    def f2(self):
        def f3():
            return math.cos(0)

        return int(f3()) * self.f()


class TestClass4:
    field8 = [[1, '2'], [3, '4'], 5, '6']

    def f4(self):
        return inspect.iscode(self.field8)


class TestClass5(TestClass3, TestClass4):
    field9 = 'Cb|N'

    class A:
        def __init__(self):
            self.fieldA = 'fieldA'

        class B:
            def __init__(self):
                self.fieldB = 'fieldB'
