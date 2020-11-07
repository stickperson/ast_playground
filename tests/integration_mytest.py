from time import sleep
import unittest
from mycode.thing import MyClass


class MyClassTestCase(unittest.TestCase):
    def test_my_class(self):
        my_class = MyClass()
        sleep(10)
        self.assertEqual(my_class.true(), True)
