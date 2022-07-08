class LFSR:
    def __init__(self, key, taps):
        d = max(taps)
        assert len(key) == d, "Error: key of wrong size."
        self._s = key
        self._t = [d - t for t in taps]

    def _sum(self, L):
        s = 0
        for x in L:
            s ^= x
        return s

    def _clock(self):
        b = self._s[0]
        self._s = self._s[1:] + [self._sum(self._s[p] for p in self._t)]
        return b

    def getbit(self):
        return self._clock()


key = [0, 0, 1]
taps = [2, 3]
lfsr = LFSR(key, taps)
for i in range(10):
    print(lfsr.getbit(), end=" ")

P.<x> = PolynomialRing(GF(2))
P = x^19 + x^5 + x^2 + x + 1
C = companion_matrix(P, format='bottom')
