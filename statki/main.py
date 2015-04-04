# short example of battleships game implementation
# by Adam Balawender
# Apr 03, 2015
import random

class board:
    def __init__(self, n=10, sym=('.', '#', '/', 'x', 'X'), lengths = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1] ):
        self.n = n
        self.sym = sym
        self.lengths = lengths.copy()
        self.data = []
        self.placed = []
        self.mapped = {}
        for i in range(n): self.data.append( [self.sym[0]] * n )

    def __str__(self):
        #print("str DBG!\n", self.__dict__)
        ret = "_| " + " ".join( [ chr( ord('0') + i ) for i in range(self.n)] ) + '\n'
        for i, row in enumerate(self.data, ord('a') ):
            ret += chr(i) + "| " + " ".join( row ) + '\n'
        return ret

    def dbg( self ):
        #print("dbg DBG!\n", self.mapped )
        #print("dbg DBG!\n", self.__dict__)
        ret = "_| " + " ".join( [ chr( ord('0') + i ) for i in range(self.n)] ) + '\n'
        for i in range(self.n):
            ret += chr(ord('a')+i) + "| " + \
                    " ".join( [chr(ord('0')+self.mapped.get((i,j), [-2])[0]) for j in range(self.n)]) + '\n'
        return ret

    def isValidPos(self, x, y):
        if x < 0 or y < 0 or x >= self.n or y >= self.n: return False
        return True

    def isEmptyPos(self, x, y):
        return self.data[x][y] in (self.sym[0], self.sym[2])

    def canPlaceSingle(self, x, y):
        # russian version: cannot occupy spaces next to other ships
        for x_it in range(x-1, x+2):
            for y_it in range(y-1, y+2):
                if self.isValidPos(x_it, y_it):
                    if not self.isEmptyPos(x_it, y_it): return False
        return self.isValidPos(x, y)

    def canPlaceShip(self, x, y, length, vertical):
        if vertical:
            for x_it in range(x, x+length):
                if not self.canPlaceSingle(x_it, y): return False
        else:
            for y_it in range(y, y+length):
                if not self.canPlaceSingle(x, y_it): return False

        return length in self.lengths

    def placeShip(self, x, y, length, vertical):
        if not self.canPlaceShip(x, y, length, vertical): return False
        self.lengths.remove(length)
        self.placed.append( [length] )
        if vertical:
            for x_it in range(x, x+length):
                self.mark( self.sym[1], x_it, y)
                self.mapped[ (x_it, y) ] = self.placed[-1]
        else:
            for y_it in range(y, y+length):
                self.mark(self.sym[1], x, y_it)
                self.mapped[ (x, y_it) ] = self.placed[-1]
        return True

    def canShoot(self, x, y):
        return self.isValidPos(x, y) and self.data[x][y] not in self.sym[2:5]

    def findShip(self, x, y):
        # print("looking for ship crossing" , x, y)
        surr = set( [(x, y)] )
        found = []

        while( surr ):
            (x, y) = surr.pop()
            found.append( (x,y) )
            for pos in ( (x-1, y), (x+1, y), (x, y-1), (x, y+1) ):
                if self.isValidPos( *pos ) and not self.isEmptyPos( *pos ) and not pos in found:
                    surr.add( pos )
        (x, y) = min(found)
        return (x, y, len(found), x != max(found)[0] )

    def sinkShip(self, x, y, length, vertical):
        if vertical:
            for x_it in range(x, x+length):
                #self.data[x_it][y] = self.sym[4]
                self.mark( self.sym[4], x_it, y)
        else:
            for y_it in range(y, y+length):
                #self.data[x][y_it] = self.sym[4]
                self.mark( self.sym[4], x, y_it)
        return True

    def shoot(self, x, y):
        if not self.canShoot(x, y): return '?'
        if self.isEmptyPos(x, y):
            self.data[x][y] = self.sym[2]
        else:
            self.data[x][y] = self.sym[3]
            self.mapped[ (x, y) ][0] -= 1
            if not self.mapped[ (x, y) ][0]:
                self.sinkShip( *self.findShip(x, y) )
        return self.data[x][y]

    def get(self, x, y):
        return self.data[x][y] if self.isValidPos(x, y) else '?'

    def placeRandomly(self):
        while( self.lengths ):
            self.placeShip( random.randrange(0, self.n),
                        random.randrange(0, self.n),
                        self.lengths[0],
                        random.randint(0, 1) )

    def mark(self, value, x, y):
        if not self.isValidPos(x, y): return False
        #print("in mark", value, x, y )
        self.data[x][y] = value
        return True

    def getRandomPos(self):
        return ( random.randrange(0, self.n), random.randrange(0, self.n) )

class player:
    def __init__(self, name=""):
        self.name = name
        self.board1 = board()
        self.board1.placeRandomly()

        self.board2 = board()

    def __str__(self):
        s1 = str(self.board1).strip().split('\n')
        s2 = self.board1.dbg().strip().split('\n')
        s3 = str(self.board2).strip().split('\n')
        return self.name + "\n" + \
                "".join( [s1i + " | " + s2i + " |" + s3i + '\n'
                for (s1i, s2i, s3i) in zip(s1, s2, s3) ] )

    def aim(self):
        for x in range(self.board2.n):
            for y in range(self.board2.n):
                if self.board2.get(x, y) == self.board2.sym[3]:
                    # if we have two hits on a ship, let's check it's direction
                    _, _, lp, vp  = self.board2.findShip( x, y )
                    pos = []
                    if lp > 1:
                        if vp: pos += [ (x-1, y), (x+1, y) ]
                        else:  pos += [ (x, y-1), (x, y+1) ]
                    else:
                        pos += [ (x-1, y), (x+1, y), (x, y-1), (x, y+1) ]
                    while pos:
                        p = random.choice(pos)
                        pos.remove( p )
                        if self.board2.canShoot( *p ): return p
        for i in range(100):
            p = self.board2.getRandomPos()
            if self.board2.canShoot( *p ) and self.board2.canPlaceSingle( *p ):
                return p
        print( "FALLBACK TO RANDOM WHICH IS UNQUESTIONABLY SAD" )
        while(True):
            p = self.board2.getRandomPos()
            if self.board2.canShoot( *p ):
                return p

    def handleShot(self, p):
        return self.board1.shoot( *p )

    def handleReply(self, p, reply):
        # print("in handleReply", p, reply )
        if reply == self.board2.sym[4]:
            x, y, l, v = self.board2.findShip( *p )
            if( v ): #vertical
                for x_it in range( x-1, x+l+1 ):
                    for y_it in range( y-1, y+2 ):
                        if self.board2.canShoot( x_it, y_it ):
                            self.board2.mark( self.board2.sym[2], x_it, y_it )
            else:
                for y_it in range( y-1, y+l+1 ):
                    for x_it in range( x-1, x+2 ):
                        if self.board2.canShoot( x_it, y_it ):
                            self.board2.mark( self.board2.sym[2], x_it, y_it )
            self.board2.sinkShip( x, y, l, v )
        elif reply == self.board2.sym[3]:
            x, y, l, v = self.board2.findShip( *p )
            if l > 1:
                if( v ): #vertical
                    for x_it in range( x-1, x+l+1 ):
                        for y_it in ( y-1, y+1 ):
                            if self.board2.canShoot( x_it, y_it ):
                                self.board2.mark( self.board2.sym[2], x_it, y_it )
                else:
                    for y_it in range( y-1, y+l+1 ):
                        for x_it in ( x-1, x+1 ):
                            if self.board2.canShoot( x_it, y_it ):
                                self.board2.mark( self.board2.sym[2], x_it, y_it )

        self.board2.mark( reply, p[0], p[1] )

    def hasWon(self):
        ret = 0
        # print(self.board2.__dict__)
        for x in range( self.board2.n ):
            for y in range( self.board2.n ):
                if self.board2.get(x, y) == self.board2.sym[4]:
                    ret += 1
        return ret == sum(self.board2.lengths)

class humanPlayer(player):
    def aim(self):
        inp = ""
        print( self )
        while( True ):
            inp = input("shoot >: ")
            if len(inp) != 2: continue
            pos = (ord( inp[0].lower() ) - ord('a'), ord( inp[1] ) - ord('0') )
            if self.board2.canShoot( *pos ): return pos

# player1 = player("CPU1")
player1 = humanPlayer("Me")
player2 = player("CPU")

#print( player1 )
#print( player2 )
for i in range(1000):
    p = player1.aim()
    h = player2.handleShot(p)
    player1.handleReply(p, h)
    if player1.hasWon():
        print(player1.name + " WON! ", i)
        break

    p = player2.aim()
    h = player1.handleShot(p)
    player2.handleReply(p, h)
    if player2.hasWon():
        print(player2.name + " WON! ", i)
        break

print( player1 )
print( player2 )
# tests for board.canPlaceShip():
# s1 = (0, 3, 2, 1)
# print( pl.canPlaceShip(*s1) )
# pl.placeShip(*s1)
# s1 = (0, 3, 4, 0)
# print( pl.canPlaceShip(*s1) )
# pl.placeShip(*s1)
# s1 = (1, 7, 4, 1)
# print( pl.canPlaceShip(*s1) )
# pl.placeShip(*s1)
# s1 = (0, 9, 1, 0)
# print( pl.canPlaceShip(*s1) )
# pl.placeShip(*s1)
# s1 = (2, 9, 2, 1)
# print( pl.canPlaceShip(*s1) )
# pl.placeShip(*s1)
# print(pl)
