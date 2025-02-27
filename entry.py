class Entry:
    def __init__(self, key, value, next_node) -> None:
        self.key = key
        self.value = value
        self.next_node = next_node

    def __repr__(self) -> str:
        return f'{self.key}: {self.value}'