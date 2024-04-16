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
    
        def get_value(self):
            # print(self, self.node)
            return self.node.value
        
        def set_value(self, value):
            self.node.value = value


    def end(self) -> Iterator:
        return self.Iterator(self.fake_node)

    def begin(self) -> Iterator:
        return next(self.end())

    def __init__(self):
        self.fake_node = DLList.Node(None, None, None)
        self.fake_node.nxt = self.fake_node
        self.fake_node.prv = self.fake_node
        self.sz = 0
    
    def insert(self, iter: Iterator, value):
        new_node: DLList.Node = DLList.Node(value, prev(iter).node, iter.node)
        prev(iter).node.nxt = new_node
        iter.node.prv = new_node
        self.sz += 1
    
    def erase(self, iter: Iterator):
        prev(iter).node.nxt = next(iter).node
        next(iter).node.prv = prev(iter).node
        self.sz -= 1
    
    def push_back(self, value):
        self.insert(self.end(), value)

    def push_front(self, value):
        self.insert(self.begin(), value)

    def pop_back(self):
        self.erase(prev(self.end()))
    
    def pop_front(self):
        self.erase(self.begin())

    def front(self):
        return self.begin().get_value()
    
    def back(self):
        return prev(self.end()).get_value()
    
    def __len__(self) -> int:
        return self.sz
    
    def empty(self) -> bool:
        return len(self) == 0

