class txtResult:
    def __init__(self, name, pq, sen, wp, pos, top):
        self.name = name
        self.pq = pq
        self.sen = sen
        self.wp = wp
        self.pos = pos
        self.top = top
        # Key: book, value: list of tfidf values
        self.tfidf = {}
        self.tfidf_words = []
