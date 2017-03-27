class Stack:
    def __init__(self):
        self._array = []

    def push(self, val):
        self._array.append((val))

    def pop(self):
        if not self._array:
            raise RuntimeError("Attempt to call pop on empty stack")
        val = self._array[-1]
        del self._array[-1]
        return val

    def stackSize(self):
        return len(self._array)

def testStack():
    stack = Stack()
    for i in range(5):
        stack.push(i)
    for x in range(5):
        print(stack.pop())
