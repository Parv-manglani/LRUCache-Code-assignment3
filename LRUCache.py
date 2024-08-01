class Node:
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class DLL:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.trav = None

    def get_size(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def get_tail(self):
        return self.tail

    def get_head(self):
        return self.head

    def append(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def __str__(self):
        l = []
        trav = self.head
        while trav is not None:
            l.append(str(trav.data))
            trav = trav.next
        string = "<-->".join(l)
        return string

    def add_first(self, data):
        newNode = Node(data)
        if self.is_empty():
            self.head = newNode
            self.tail = newNode
        else:
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode
        self.size += 1

    def add_at(self, ind, data):
        if ind < 0 or ind > self.size:
            raise Exception("Index out of range.")
        if ind == 0 or ind == self.get_size():
            self.append(data)
        else:
            id = 0
            trav = self.head
            while id != ind - 1:
                id += 1
                trav = trav.next
            newNode = Node(data, trav, trav.next)
            trav.next = newNode
            newNode.next.prev = newNode
        self.size += 1


class LRUCache:
    def __init__(self, cap):
        self.cap = cap
        self.data = {}
        self.keyList = DLL()
        self.keymap = {}

    def get(self, key):
        if key not in self.data:
            return -1
        self.use(key)
        return self.data[key]

    def put(self, key, value):
        if key in self.data:
            self.data[key] = value
        else:
            if self.keyList.get_size() >= self.cap:
                oldest_key = self.keyList.head.data
                self.keyList.head = self.keyList.head.next
                if self.keyList.head:
                    self.keyList.head.prev = None
                self.keyList.size -= 1
                del self.data[oldest_key]
                del self.keymap[oldest_key]
            self.data[key] = value
            new_node = Node(key)
            if self.keyList.tail:
                self.keyList.tail.next = new_node
                new_node.prev = self.keyList.tail
                self.keyList.tail = new_node
            else:
                self.keyList.head = new_node
                self.keyList.tail = new_node
            self.keyList.size += 1
            self.keymap[key] = new_node
        self.use(key)

    def use(self, key):
        node = self.keymap[key]
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node == self.keyList.tail:
            return
        if node == self.keyList.head:
            self.keyList.head = node.next
            if self.keyList.head:
                self.keyList.head.prev = None
        node.prev = self.keyList.tail
        node.next = None
        if self.keyList.tail:
            self.keyList.tail.next = node
        self.keyList.tail = node
        if not self.keyList.head:
            self.keyList.head = node

