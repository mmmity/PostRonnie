import unittest
from src.dllist import DLList, nxt, prv

class TestDLList(unittest.TestCase):
    def setUp(self):
        self.list = DLList()
        for i in range(5):
            self.list.push_back(i)

    def check_bypass(self, iterable):
        iterator = self.list.begin()
        self.assertEqual(len(iterable), len(self.list))
        for i in iterable:
            self.assertEqual(i, iterator.get_value())
            iterator = nxt(iterator)
        self.assertEqual(iterator, self.list.end())

    def test_iterator_bypass(self):
        self.check_bypass([0, 1, 2, 3, 4])

    def test_basic_functionality(self):
        iterator = self.list.begin()
        iterator = nxt(nxt(iterator))
        self.list.insert(iterator, 5)
        self.check_bypass([0, 1, 5, 2, 3 ,4])
        self.assertEqual(iterator.get_value(), 2)
        self.list.erase(iterator)
        self.check_bypass([0, 1, 5, 3, 4])

        self.list.push_back(2)
        self.list.push_back(3)
        self.check_bypass([0, 1, 5, 3, 4, 2, 3])
        self.list.pop_front()
        self.check_bypass([1, 5, 3, 4, 2, 3])
        self.list.pop_back()
        self.check_bypass([1, 5, 3, 4, 2])
        self.list.push_front(0)
        self.check_bypass([0, 1, 5, 3, 4, 2])

        self.assertEqual(self.list.front(), 0)
        self.assertEqual(self.list.back(), 2)

    def test_iterators(self):
        iterator = self.list.begin()
        iterator.set_value(5)
        self.check_bypass([5, 1, 2, 3, 4])
        iterator = nxt(iterator)
        self.assertNotEqual(iterator, self.list.begin())
        iterator = prv(iterator)
        self.assertEqual(iterator, self.list.begin())
        iterator = nxt(nxt(nxt(nxt(nxt(iterator)))))
        self.assertEqual(iterator, self.list.end())
        self.assertEqual(iterator.get_value(), None)

    def test_empty(self):
        for _ in range(5):
            self.assertFalse(self.list.empty())
            self.list.pop_back()
        self.assertTrue(self.list.empty())
