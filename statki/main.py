# short example of battleships game implementation
# by Adam Balawender
# Apr 03, 2015
import random

class board:
    def __init__(self, n=10, sym=('.', '#', '/', 'X'), lengths = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1] ):
        self.n = n
        self.sym = sym
        self.lengths = lengths.copy()
        self.data = []
        for i in range(n): self.data.append( [self.sym[0]] * n )

    def __str__(self):
        ret = "_| " + " ".join( [ chr( ord('0') + i ) for i in range(self.n)] ) + '\n'
        for i, row in enumerate(self.data, ord('a') ):
            ret += chr(i) + "| " + " ".join( row ) + '\n'
        return ret

    def isValidPos(self, x, y):
        if x < 0 or y < 0 or x >= self.n or y >= self.n: return False
        return True

    def isEmptyPos(self, x, y):
        return self.data[x][y] == self.sym[0]

    def canPlaceSingle(self, x, y):
        # russian version: cannot occupy spaces next to other ships
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

        return length in self.lengths

    def place(self, x, y, length, vertical):
        if not self.canPlace(x, y, length, vertical): return False
        self.lengths.remove(length)
        if vertical:
            for x_it in range(x, x+length):
                self.data[x_it][y] = self.sym[1]
        else:
            for y_it in range(y, y+length):
                self.data[x][y_it] = self.sym[1]
        return True

    def canShoot(self, x, y):
        return self.isValidPos(x, y) and self.data[x][y] not in self.sym[2:4]

    def shoot(self, x, y):
        if not self.canShoot(x, y): return '?'
        self.data[x][y] = self.sym[2] if self.isEmptyPos(x, y) else self.sym[3]
        return self.data[x][y]

    def get(self, x, y):
        return self.data[x][y] if self.isValidPos(x, y) else '?' 

    def placeRandomly(self):
        while( self.lengths ):
            self.place( random.randrange(0, self.n),
                        random.randrange(0, self.n),
                        self.lengths[0],
                        random.randint(0, 1) )

    def mark(self, value, x, y):
        if not self.isValidPos(x, y): return False
        print("in mark", value, x, y )
        self.data[x][y] = value
        return True

class player:
    def __init__(self, name=""):
        self.name = name
        self.board1 = board()
        self.board1.placeRandomly()

        self.board2 = board()

    def __str__(self):
        s1 = str(self.board1).strip().split('\n')
        s2 = str(self.board2).strip().split('\n')
        return self.name + "\n" + \
                "".join( [s1i + " | " + s2i + '\n' for (s1i, s2i) in zip(s1, s2) ] )

    def aim(self):
        return (random.randrange(0, self.board1.n), random.randrange(0, self.board1.n))

    def handleShot(self, p):
        if not self.board1.shoot( *p ): return "invalid"
        return self.board1.get( *p )

    def handleReply(self, p, reply):
        print("in handleReply", p, reply )
        self.board2.mark( reply, p[0], p[1] )


player1 = player("CPU1")
player2 = player("CPU2")

print( player1 )
print( player2 )
for i in range(20):
    p = player1.aim()
    h = player2.handleShot(p)
    player1.handleReply(p, h)
    print(i, p, "-> ", h)
    if h == "hit": break

print( player1 )
print( player2 )
# tests for board.canPlace():
# s1 = (0, 3, 2, 1)
# print( pl.canPlace(*s1) )
# pl.place(*s1)
# s1 = (0, 3, 4, 0)
# print( pl.canPlace(*s1) )
# pl.place(*s1)
# s1 = (1, 7, 4, 1)
# print( pl.canPlace(*s1) )
# pl.place(*s1)
# s1 = (0, 9, 1, 0)
# print( pl.canPlace(*s1) )
# pl.place(*s1)
# s1 = (2, 9, 2, 1)
# print( pl.canPlace(*s1) )
# pl.place(*s1)
# print(pl)
