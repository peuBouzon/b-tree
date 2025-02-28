from node import Node
from entry import Entry

# TODO: add sentinel
# TODO: remover itens duplicados (cada item deve armazenar tambeḿ seu valor)
# TODO: fix max_entries_per_node odd values
# TODO: print tree

class BPlusTree:
    INVALID_KEY_MESSAGE = "The key to search should be informed."
    INVALID_MAX_ENTRIES_MESSAGE = "The number of entries per node should be even."

    def __init__(self, max_entries_per_node = 1000) -> None:

        if not max_entries_per_node % 2 == 0:
            raise ValueError(BPlusTree.INVALID_MAX_ENTRIES_MESSAGE)

        self.max_entries_per_node = max_entries_per_node
        self.root = Node(0, max_entries_per_node)
        self.height = 0
        self.n_entries = 0

    def get(self, key):
        if key is None:
            raise ValueError(BPlusTree.INVALID_KEY_MESSAGE)
        return self._search(self.root, key, self.height)

    def _search(self, node : Node, key, height : int):
        if height == 0:
            for i in range(len(node)):
                if node.entries[i].key == key:
                    return node.entries[i].value
        else:
            for i in range(len(node)):
                if i+1 == len(node) or key < node.entries[i+1].key: # find the greater entry whose value is smaller or equal to the key 
                    return self._search(node.entries[i].next_node, key, height - 1)
    
    def put(self, key, value):
        if key is None:
            raise ValueError(BPlusTree.INVALID_KEY_MESSAGE)
        new_node : Node = self._insert(self.root, key, value, self.height)
        self.n_entries += 1
        if not new_node is None:
            new_root = Node(2, self.max_entries_per_node)
            new_root.entries[0] = Entry(self.root.entries[0].key, None, self.root)
            new_root.entries[1] = Entry(new_node.entries[0].key, None, new_node)
            self.root = new_root
            self.height += 1

    def _insert(self, node : Node, key, value, height : int):
        new_entry = None
        index_new_entry = 0

        if height != 0:
            n_entries_on_node = len(node)
            for i in range(n_entries_on_node):
                index_new_entry = i + 1
                if i+1 == n_entries_on_node or key < node.entries[i+1].key:
                    new_node : Node = self._insert(node.entries[i].next_node, key, value, height - 1)
                    if new_node is None:
                        return

                    new_entry = Entry(new_node.entries[0].key, None, new_node)
                    break
        else:
            new_entry = Entry(key, value, None)
            for i in range(len(node)):
                # replace the value instead of adding a new entry if the key is already present 
                if key == node.entries[i].key:
                    node.entries[i].value = value
                    self.n_entries -= 1 # substracts one to keep consistency as this will be incremented latter
                    return

                index_new_entry = i + 1
                if key < node.entries[i].key:
                    index_new_entry -= 1 # if the key is less than the entry key, it should add before
                    break

        node.insert(new_entry, index_new_entry)

        if len(node) >= self.max_entries_per_node:
            return node.split()[1]

    def delete(self, key):
        self.put(key, None)
        self.n_entries -= 1
        
if __name__ == '__main__':
        st = BPlusTree(4)
        st.put("www.cs.princeton.edu", "128.112.136.12")
        st.put("www.cs.princeton.edu", "128.112.136.11")
        st.put("www.princeton.edu",    "128.112.128.15")
        st.put("www.yale.edu",         "130.132.143.21")
        st.put("www.simpsons.com",     "209.052.165.60")
        st.put("www.apple.com",        "17.112.152.32")
        st.put("www.amazon.com",       "207.171.182.16")
        st.put("www.ebay.com",         "66.135.192.87")
        st.put("www.cnn.com",          "64.236.16.20")
        st.put("www.google.com",       "216.239.41.99")
        st.put("www.nytimes.com",      "199.239.136.200")
        st.put("www.microsoft.com",    "207.126.99.140")
        st.put("www.dell.com",         "143.166.224.230")
        st.put("www.slashdot.org",     "66.35.250.151")
        st.put("www.espn.com",         "199.181.135.201")
        st.put("www.weather.com",      "63.111.66.11")
        st.put("www.yahoo.com",        "216.109.118.65")

        print(f'Number of entries: {st.n_entries}')

        print(f'cs.princeton.edu:  {st.get("www.cs.princeton.edu")}')
        print(f'hardvardsucks.com: {st.get("www.harvardsucks.com")}')
        print(f'simpsons.com:      {st.get("www.simpsons.com")}')
        print(f'apple.com:         {st.get("www.apple.com")}')
        print(f'ebay.com:          {st.get("www.ebay.com")}')
        print(f'dell.com:          {st.get("www.dell.com")}')
        print(f'www.yahoo.com:     {st.get("www.yahoo.com")}')
        print(f'www.amazon.com:    {st.get("www.amazon.com")}')
        print(f'www.microsoft.com: {st.get("www.microsoft.com")}')
        print(f'www.google.com:    {st.get("www.google.com")}')
        print(f'www.slashdot.org:  {st.get("www.slashdot.org")}')
        print(f'www.weather.com:   {st.get("www.weather.com")}')
        print(f'www.nytimes.com:   {st.get("www.nytimes.com")}')
        print(f'www.cnn.com:       {st.get("www.cnn.com")}')
        print(f'www.espn.com:      {st.get("www.espn.com")}')
        print(f'www.yahoo.com:     {st.get("www.yahoo.com")}')