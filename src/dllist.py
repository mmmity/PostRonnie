'''
Implementation of double-linked list for interpreter
'''
from __future__ import annotations
from typing import Iterable


def nxt(iterator):
    '''
    Returns iterator to the next node
    '''
    return iterator.__nxt__()

def prv(iterator):
    '''
    Returns iterator to the previous node
    '''
    return iterator.__prv__()


class DLList:
    '''
    Implementation of double-linked list
    '''
    class Node:
        '''
        A node of double-linked list
        '''
        def __init__(self, value, prv_node: DLList.Node, nxt_node: DLList.Node):
            self.value = value
            self.nxt = nxt_node
            self.prv = prv_node


    class Iterator:
        '''
        Bidirectional iterator for walking over list
        '''
        def __init__(self, node: DLList.Node):
            self.node: DLList.Node = node

        def __eq__(self, other: DLList.Iterator) -> bool:
            return self.node is other.node

        def __ne__(self, other: DLList.Iterator) -> bool:
            return not self == other

        def __nxt__(self) -> DLList.Iterator:
            return DLList.Iterator(self.node.nxt)

        def __prv__(self) -> DLList.Iterator:
            return DLList.Iterator(self.node.prv)

        def get_value(self):
            '''
            Returns node value
            '''
            return self.node.value

        def set_value(self, value):
            '''
            Sets node value
            '''
            self.node.value = value


    def end(self) -> Iterator:
        '''
        Returns iterator to the element after the last
        '''
        return self.Iterator(self.fake_node)

    def begin(self) -> Iterator:
        '''
        Returns iterator to the first element
        '''
        return nxt(self.end())

    def __init__(self, iterable=[]):
        '''
        Initializes fake_node with dummy values
        If iterable is specified, initializes list with its values
        '''
        self.fake_node = DLList.Node(None, None, None)
        self.fake_node.nxt = self.fake_node
        self.fake_node.prv = self.fake_node
        self.sz = 0

        for el in iterable:
            self.push_back(el)

    def insert(self, iterator: Iterator, value):
        '''
        Inserts value just before the iter
        '''
        new_node: DLList.Node = DLList.Node(value, prv(iterator).node, iterator.node)
        prv(iterator).node.nxt = new_node
        iterator.node.prv = new_node
        self.sz += 1

    def erase(self, iterator: Iterator):
        '''
        Erases value on iter
        '''
        prv(iterator).node.nxt = nxt(iterator).node
        nxt(iterator).node.prv = prv(iterator).node
        self.sz -= 1

    def push_back(self, value):
        '''
        Adds value to the back of list
        '''
        self.insert(self.end(), value)

    def push_front(self, value):
        '''
        Adds value to the front of list
        '''
        self.insert(self.begin(), value)

    def pop_back(self):
        '''
        Removes value from back of list
        '''
        self.erase(prv(self.end()))

    def pop_front(self):
        '''
        Removes value from front of list
        '''
        self.erase(self.begin())

    def front(self):
        '''
        Returns value of first element
        '''
        return self.begin().get_value()

    def back(self):
        '''
        Returns value of last element
        '''
        return prv(self.end()).get_value()

    def __len__(self) -> int:
        return self.sz

    def empty(self) -> bool:
        '''
        Checks if list is empty
        '''
        return len(self) == 0

    def __eq__(self, other: DLList) -> bool:
        if len(self) != len(other):
            return False
        
        this_iter, other_iter = self.begin(), other.begin()
        while this_iter != self.end():
            if this_iter.get_value() != other_iter.get_value():
                return False
            this_iter = nxt(this_iter)
            other_iter = nxt(other_iter)
        
        return True

    def __ne__(self, other: DLList) -> bool:
        return not self == other
