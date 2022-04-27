from kraken.serializer_creator import SerializerCreator
import math


c = 42


def f(x):
    a = 123
    return math.sin(x * a * c)


def main():
    serializer = SerializerCreator().create_serializer('json')
    serializer.dump(f, 'test_output/test.json')


if __name__ == '__main__':
    main()
