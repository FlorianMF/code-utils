
import unittest
import os
from py_utils.decorators.base import BaseDecorator

class TestBaseDecorator(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        pass

    def test_base_decorator(self):

        @BaseDecorator
        def return_args_kwargs(*args, **kwargs):
            return (args, kwargs)
        self.assertEqual(return_args_kwargs(), ((), {}))

        @BaseDecorator
        def return_args_kwargs(*args, **kwargs):
            return (args, kwargs)
        self.assertEqual(return_args_kwargs(1, 2, three=3), ((1,2), {'three':3}))


        @BaseDecorator()
        def return_args_kwargs(*args, **kwargs):
            return (args, kwargs)
        self.assertEqual(return_args_kwargs(1, 2, three=3), ((1,2), {'three':3}))

        # TODO check how to do this assertRaises
        @BaseDecorator(4)
        def return_args_kwargs(*args, **kwargs):
            return (args, kwargs)
        # self.assertRaises(TypeError, return_args_kwargs, (1, 2), three=3)
        print(return_args_kwargs(1, 2, three=3))
        self.assertEqual(return_args_kwargs.args, (4,))

        @BaseDecorator(five=5)
        def return_args_kwargs(*args, **kwargs):
            return (args, kwargs)
        self.assertEqual(return_args_kwargs(1, 2, three=3), ((1,2), {'three':3}))
        self.assertEqual(return_args_kwargs.kwargs, {'five':5})

        # TODO check how to do this assertRaises
        @BaseDecorator(4, five=5)
        def return_args_kwargs(*args, **kwargs):
            return (args, kwargs)
        self.assertEqual(return_args_kwargs(1, 2, three=3), ((1,2), {'three':3}))
        self.assertEqual(return_args_kwargs.args, (4,))
        self.assertEqual(return_args_kwargs.kwargs, {'five':5})

if __name__ == '__main__':
    unittest.main()
