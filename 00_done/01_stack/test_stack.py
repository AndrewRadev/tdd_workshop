import unittest

from stack import Stack

class TestStack(unittest.TestCase):
    def test_pushing_items_on_top_and_removing_from_the_top(self):
        stack = Stack()

        stack.push(1)
        stack.push(2)
        stack.push(3)

        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)

        stack.push(4)
        stack.push(5)

        self.assertEqual(stack.pop(), 5)
        self.assertEqual(stack.pop(), 4)
        self.assertEqual(stack.pop(), 1)
        self.assertEqual(stack.pop(), None)

    def test_popping_an_empty_stack(self):
        stack = Stack()
        self.assertEqual(stack.pop(), None)

    def test_that_two_stacks_are_not_connected(self):
        stack1 = Stack()
        stack2 = Stack()

        stack1.push(1)
        stack2.push(2)

        self.assertEqual(stack1.pop(), 1)
        self.assertEqual(stack2.pop(), 2)

if __name__ == '__main__':
    unittest.main()
