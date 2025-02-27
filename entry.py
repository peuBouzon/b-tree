from node import Node

class Entry:
    def __init__(self, key, value, next_node : Node) -> None:
        self.key = key
        self.value = value
        self.next_node = next_node