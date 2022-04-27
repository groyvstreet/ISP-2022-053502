import math


a = 123


def test_func1(x):
    b = 123
    return math.sin(x * a * b)


def test_func2(x):
    b = 123

    def f():
        return 23

    return math.sin(x * a * b * f())


def test_func3(x):
    b = 123

    def f():
        def f2():
            return 12

        return 23 * f2()

    return math.sin(x * a * b * f())


def test_func4(x):
    b = 123

    def f():
        def f2():
            return 12

        return 23 * f2()

    class A:
        field = '5'

        def f(self):
            return int(self.field)

    return math.sin(x * a * b * f() * A().f())


def test_func5(x):
    b = 123

    def f():
        def f2():
            return 12

        return 23 * f2()

    class A:
        class B:
            field = '11'

            def f(self):
                return int(self.field)

        field = '5'

        def f(self):
            return int(self.field)

    return math.sin(x * a * b * f() * A().f() * A().B().f())


def test_func6(x):
    b = 123

    def f():
        def f2():
            def f3():
                return 98

            return 12 * f3()

        return 23 * f2()

    class A:
        class B:
            field = '11'

            def f(self):
                return int(self.field)

        field = '5'

        def f(self):
            return int(self.field)

    class C:
        class D:
            field = '45'

            def f(self):
                return int(self.field)

        field = '98'

        def f(self):
            return int(self.field)

    return math.sin(x * a * b * f() * A().f() * A().B().f() * C().f() * C().D().f())


def test_func7(x):
    b = 123

    def f():
        c = 76
        return math.sin(x * a * b * c)

    return f()


def test_func8(x):
    b = 123

    def f():
        c = 78

        def f2():
            d = 546
            return math.sin(x * a * b * c * d)

        return 23 * f2()

    return f()


def test_func9(x):
    b = 123

    def f():
        c = 78

        def f2():
            d = 546
            return math.sin(x * a * b * c * d)

        return 23 * f2()

    class A:
        field = '5'

        def f(self):
            return math.sin(x * a * b) * int(self.field)

    return A().f() * f()


def test_func10(x):
    b = 123

    def f():
        c = 78

        def f2():
            d = 546
            return math.sin(x * a * b * c * d)

        return 23 * f2()

    class A:
        class B:
            field = '11'

            def f(self):
                return math.sin(x * a * b) * int(self.field)

        field = '5'

        def f(self):
            return self.B().f()

    return math.sin(x * a * b * f() * A().f() * A().B().f())
