from __future__ import annotations




def next(iter):
    return iter.__next__()

def prev(iter):
    return iter.__prev__()


class DLList:

    class Node:
        def __init__(self, value, prv: DLList.Node, nxt: DLList.Node):
            self.value = value
            self.nxt = nxt
            self.prv = prv


    class Iterator:
        def __init__(self, node: DLList.Node):
            self.node: DLList.Node = node
        
        def __eq__(self, other: DLList.Iterator) -> bool:
            return self.node is other.node
        
        def __ne__(self, other: DLList.Iterator) -> bool:
            return not self == other

        def __next__(self) -> DLList.Iterator:
            return DLList.Iterator(self.node.nxt)
        
        def __prev__(self) -> DLList.Iterator:
            return DLList.Iterator(self.node.prv)
    
        def value(self):
            return self.node.value


    def end(self) -> Iterator:
        return self.Iterator(self.fake_node)

    def begin(self) -> Iterator:
        return next(self.end())

    def __init__(self):
        self.fake_node = DLList.Node(None, None, None)
        self.fake_node.nxt = self.fake_node
        self.fake_node.prv = self.fake_node
    
    def insert(self, iter: Iterator, value):
        new_node: DLList.Node = DLList.Node(value, prev(iter).node, iter.node)
        prev(iter).node.nxt = new_node
        iter.node.prv = new_node
    
    def push_back(self, value):
        self.insert(self.end(), value)

    def push_front(self, value):
        self.insert(self.begin(), value)

    def is_begin(self, iter: Iterator):
        return iter == self.begin()

    def is_end(self, iter: Iterator):
        return iter == self.end()

