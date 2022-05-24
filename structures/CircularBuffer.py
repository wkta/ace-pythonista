

class CircularBuffer(object):

    def __init__(self, max_size=128):
        """Initialize the CircularBuffer with a max_size if set, otherwise
        max_size will elementsdefault to 10"""
        self.buffer = [None] * max_size
        self.head = 0
        self.tail = 0
        self.max_size = max_size

    def __str__(self):
        """Return a formatted string representation of this CircularBuffer."""
        items = ['{!r}'.format(item) for item in self.buffer]
        return '[' + ', '.join(items) + ']'

    def size(self):
        """Return the size of the CircularBuffer
        Runtime: O(1) Space: O(1)"""
        y = -self.head
        if self.tail < self.head:
            return y + self.max_size - self.tail
        else:
            return y + self.tail

    def is_empty(self):
        """Return True if the head of the CircularBuffer is equal to the tail,
        otherwise return False
        Runtime: O(1) Space: O(1)"""
        return self.tail == self.head

    def is_full(self):
        """Return True if the tail of the CircularBuffer is one before the head,
        otherwise return False
        Runtime: O(1) Space: O(1)"""
        return self.tail == (self.head-1) % self.max_size

    def enqueue(self, item):
        """Insert an item at the back of the CircularBuffer
        Runtime: O(1) Space: O(1)"""
        if self.is_full():
            raise OverflowError("CircularBuffer is full, unable to enqueue item")
        if self.tail > self.max_size and self.head > self.max_size:
            self.tail -= self.max_size
            self.head -= self.max_size

        self.buffer[self.tail % self.max_size] = item
        self.tail = self.tail + 1

    def front(self):
        """Return the item at the front of the CircularBuffer
        Runtime: O(1) Space: O(1)"""
        return self.buffer[self.head]

    def dequeue(self):
        """Return the item at the front of the Circular Buffer and remove it
        Runtime: O(1) Space: O(1)"""
        if self.tail == self.head:  # is empty
            raise IndexError("CircularBuffer is empty, unable to dequeue")
        item = self.buffer[self.head % self.max_size]
        self.buffer[self.head % self.max_size] = None
        self.head = self.head + 1
        return item


# test
if __name__ == '__main__':
    cb = CircularBuffer(5)
    print("Empty: {}".format(cb.is_empty()))
    print("Full: {}".format(cb.is_full()))
    print(str(cb))
    cb.enqueue("one")
    cb.enqueue("two")
    cb.enqueue("three")
    cb.enqueue("four")
    print(str(cb))
    print(cb.dequeue())
    print(cb.dequeue())
    print(str(cb))
    cb.enqueue("five")
    cb.enqueue("six")
    print(str(cb))
    print("Full: {}".format(cb.is_full()))
