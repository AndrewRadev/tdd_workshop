class Stack:
    def __init__(self):
        self.storage = []

    def push(self, value):
        self.storage.append(value)

    def pop(self):
        if len(self.storage) == 0:
            return None

        return self.storage.pop()
