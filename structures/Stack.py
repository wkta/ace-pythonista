"""
Python stack can be implemented using the deque class
from the collections module.
Deque is preferred over the list in the cases where we need quicker
append and pop operations from both the ends of the container,
as deque provides an O(1) time complexity for append and
pop operations as compared to list which provides O(n) time complexity...

The same methods on deque as seen in the list are used, that is:

append() and pop().
empty() – Returns whether the stack is empty – Time Complexity: O(1)
size() – Returns the size of the stack – Time Complexity: O(1)
top() – Returns a ref to the topmost elt of the stack – Time Complexity: O(1)
push(a) – Inserts the element ‘a’ at the top of the stack – Time Complexity: O(1)
pop() – Deletes the topmost element of the stack – Time Complexity: O(1)
"""


from collections import deque


class Stack:
    """
    stack implementation, uses collections.deque
    """

    def __init__(self, sequence=None):
        self._data = deque()

    def push(self, v):
        self._data.append(v)

    def pop(self):
        try:
            return self._data.pop()
        except IndexError:
            return None

    def top_down_trav(self, cb_func):
        for i in range(len(self._data)-1, -1, -1):
            cb_func(self._data[i])

    def bottom_up_trav(self, cb_func):
        for i in range(len(self._data)):
            cb_func(self._data[i])
    
    def peek(self):
        if len(self._data):
            return self._data[-1]

    @property
    def count(self):
        return len(self._data)

    def __str__(self):
        # custom display
        res = 'stack: '
        if self.count==0:
            return res
        def _addtext(x):
            nonlocal res
            res += '<-{}<-'.format(x)
        self.top_down_trav(_addtext)
        return res
