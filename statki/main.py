# short example of battleships game implementation
# by Adam Balawender
# Apr 03, 2015

class board:
    def __init__(self, n=10):
        self.n = n
        self.data = []
        for i in range(n): self.data.append( ['.'] * n )

    def __str__(self):
        ret = "_| " + " ".join( [ chr( ord('0') + i ) for i in range(self.n)] ) + '\n'
        for i, row in enumerate(self.data, ord('a') ):
            ret += chr(i) + "| " + " ".join( row ) + '\n'
        return ret

    def isValidPos(self, x, y):
        if x < 0 or y < 0 or x >= self.n or y >= self.n: return False
        return True

    def isEmptyPos(self, x, y):
        return '.' == self.data[x][y]

    def canPlaceSingle(self, x, y):
        for x_it in range(x-1, x+2):
            for y_it in range(y-1, y+2):
                if self.isValidPos(x_it, y_it):
                    if not self.isEmptyPos(x_it, y_it): return False
        return self.isValidPos(x, y)

    def canPlace(self, x, y, length, vertical):
        if vertical:
            for x_it in range(x, x+length):
                if not self.canPlaceSingle(x_it, y): return False
        else:
            for y_it in range(y, y+length):
                if not self.canPlaceSingle(x, y_it): return False

        return True

    def place(self, x, y, length, vertical):
        if vertical:
            for x_it in range(x, x+length):
                self.data[x_it][y] = 'x'
        else:
            for y_it in range(y, y+length):
                self.data[x][y_it] = 'x'

pl = board()
s1 = (0, 3, 2, 1)
print( pl.canPlace(*s1) )
pl.place(*s1)
s1 = (0, 3, 4, 0)
print( pl.canPlace(*s1) )
pl.place(*s1)
s1 = (1, 7, 4, 1)
print( pl.canPlace(*s1) )
pl.place(*s1)
s1 = (0, 9, 1, 0)
print( pl.canPlace(*s1) )
pl.place(*s1)
s1 = (2, 9, 2, 1)
print( pl.canPlace(*s1) )
pl.place(*s1)
print(pl)
