import unittest

from stack import Stack

class TestStack(unittest.TestCase):
    def test_simple_push_pop(self):
        stack = Stack()

        stack.push(3)
        self.assertEqual(stack.pop(), 3)

        stack.push(5)
        self.assertEqual(stack.pop(), 5)

    def test_multiple_pushes_and_pops(self):
        stack = Stack()

        stack.push(1)
        stack.push(2)
        stack.push(3)

        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.pop(), 1)
        self.assertEqual(stack.pop(), None)

    def test_popping_empty_stack(self):
        stack = Stack()
        self.assertEqual(stack.pop(), None)
        self.assertEqual(stack.pop(), None)


if __name__ == '__main__':
    unittest.main()
