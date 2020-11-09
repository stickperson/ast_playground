from time import sleep
import unittest
from example.code.thing import MyClass


class MyClassTestCase(unittest.TestCase):
    def test_my_class(self):
        my_class = MyClass()
        self.assertEqual(my_class.true(), True)
