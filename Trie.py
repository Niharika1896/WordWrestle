class TrieNode:
    def __init__(self):
        self.children = dict()
        self.end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]
        node.end = True

    def build(self, wordlist):
        for word in wordlist:
            self.insert(word)

    def search(self, word):
        node = self.root
        for letter in word:
            if letter not in node.children:
                return False
            node = node.children[letter]
        return node.end

    def autocomplete(self, prefix: str):
        node = self.root
        suggestions: [str] = []
        for letter in prefix:
            if letter in node.children:
                node = node.children[letter]
            else:
                return suggestions
        #if node.end:
        #    suggestions.append(prefix)
        self.walktrie(node, prefix, suggestions)
        return suggestions

    def walktrie(self, node, prefix: str, suggestions: [str]):
        if node.children:
            for letter in node.children:
                suggestion_word = prefix + letter
                if node.children[letter].end:
                    suggestions.append(suggestion_word)
                self.walktrie(node.children[letter], suggestion_word, suggestions)
