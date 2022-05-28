from typing import Dict, Optional

class Node(object):
    
    def __init__(self, key: str, value: object):
        self.key: str = key
        self.value: object = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

class DoubleLink(object):

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.length: int = 0

    def append_front(self, node: Node):
        if self.length <= 0:
            node.prev = None
            node.next = None
            self.head = node
            self.tail = node
            self.length += 1
            return
        old_head = self.head
        node.prev = None
        node.next = old_head
        if old_head:
            old_head.prev = node
        self.head = node
        self.length += 1

    def remove(self, node: Node):
        prev = node.prev
        next = node.next
        if node == self.head:
            self.head = next
        if node == self.tail:
            self.tail = prev
        
        if prev:
            prev.next = next
        if next:
            next.prev = prev
        
        node.prev = None
        node.next = None
        self.length -= 1
        return node

    def pop_back(self):
        tail = self.tail
        if not tail:
            return tail
        prev_tail = tail.prev
        self.tail = prev_tail
        self.length -= 1
        if prev_tail:
            prev_tail.next = None
        return tail
    
    def __str__(self):
        if self.length <= 0:
            return ""
        head = self.head
        nodes = []
        while head:
            s = "(%s: %s)" % (head.key, head.value)
            nodes.append(s)
            head = head.next
        return " -> ".join(nodes)


class Lru(object):

    def __init__(self, capacity=1024):
        self.capacity: int = capacity
        self.keys: Dict[str, Node] = dict()
        self.link: DoubleLink = DoubleLink()
    
    def set(self, key: str, value: object):
        if key in self.keys:
            node = self.keys[key]
            node.value = value
            r_node = self.link.remove(node)
            self.link.append_front(r_node)
            print(self.link.length, self.link)
            return

        if self.link.length >= self.capacity:
            p_node = self.link.pop_back()
            if p_node:
                del self.keys[p_node.key]
                del p_node
        
        node = Node(key, value)
        self.keys[key] = node
        self.link.append_front(node)
        print("length: ", self.link.length, ", link:", self.link)
        

    def get(self, key: str):
        if key not in self.keys:
            return None
        node = self.keys[key]
        r_node = self.link.remove(node)
        self.link.append_front(r_node)
        print("[GET] %s: %s" % (key, node.value))
        return node.value


if __name__ == "__main__":
    lru = Lru(3)
    lru.set("name", "ribincao")
    lru.get("name")
    lru.set("age", "27")
    lru.get("age")
    lru.set("education", "master")
    lru.get("education")
    lru.set("occupation", "全菜工程师")
    lru.set("a", "a")
    lru.set("b", "b")
    lru.set("c", "c")