"""
deque API:
------------
    append(x)
     append to the right

    appendleft(x)

    clear()
      new length<-0

    copy()
      shallow copy

    count(x)
      cardinality of elt equal to x

    extend(iterable)
      extend on the right side

    extendleft(iterable)

    index(x[, start[, stop]])
       returns the position, from START idx, until the STOP idx excluded
     ValueError if nothing is found

    insert(i, x)
      Insère x at position i
      can throw  IndexError if size isnt large enough

    pop()
      remove from right & returns the element

    popleft()

    remove(value)
      removes x,
      can throw ValueError

    reverse()
      changes the order

    rotate(n=1)
      shift elements of n slots towards right,
      if n <0 shifts to the left

    read-only attribute:
    maxlen
"""
from collections import deque


class CircularBuffer:

    def __init__(self, gmax_len=64):
        """
        Initialize the CircularBuffer with a gmax_len if given. Default size is 64
        """
        self.deque_obj = deque(maxlen=gmax_len)

    def __str__(self):
        """Return a formatted string representation of this CircularBuffer."""
        items = ['{!r}'.format(item) for item in self.deque_obj]
        return '[' + ', '.join(items) + ']'

    def size(self):
        return len(self.deque_obj)

    def is_empty(self):
        """Return True if the head of the CircularBuffer is equal to the tail,
        otherwise return False"""
        return len(self.deque_obj) == 0

    def is_full(self):
        """Return True if the tail of the CircularBuffer is one before the head,
        otherwise return False"""
        return len(self.deque_obj) == self.deque_obj.maxlen

    def enqueue(self, item):
        """Insert an item at the back of the CircularBuffer
        Runtime: O(1) Space: O(1)"""
        self.deque_obj.append(item)

    def dequeue(self):
        """Return the item at the front of the Circular Buffer and remove it
        Runtime: O(1) Space: O(1)"""
        return self.deque_obj.popleft()

    def front(self):
        """Return the item at the front of the CircularBuffer
        Runtime: O(1) Space: O(1)"""
        if len(self.deque_obj):
            return self.deque_obj[len(self.deque_obj) - 1]
        raise IndexError('circular buffer is currently empty!')


if __name__ == '__main__':
    cb = CircularBuffer(3)
    print(str(cb))
    print("Empty: {}".format(cb.is_empty()))
    print("Full: {}".format(cb.is_full()))
    print()

    cb.enqueue("one")
    cb.enqueue("two")
    cb.enqueue("three")
    cb.enqueue("four")
    print(str(cb))
    print("Empty: {}".format(cb.is_empty()))
    print("Full: {}".format(cb.is_full()))
    print()

    print(cb.dequeue())

    print('front?', cb.front())
    print(str(cb))
    print(cb.size())
    print("Empty: {}".format(cb.is_empty()))
    print("Full: {}".format(cb.is_full()))
    print()

    cb.enqueue("five")
    cb.enqueue("six")
    print(str(cb))
    print('front? ', cb.front())
    print(cb.size())
    print("Empty: {}".format(cb.is_empty()))
    print("Full: {}".format(cb.is_full()))
    print()

    print(cb.dequeue())
    print(cb.dequeue())
    print(cb.dequeue())
    print(str(cb))
    print(cb.size())
    print("Empty: {}".format(cb.is_empty()))
    print("Full: {}".format(cb.is_full()))
