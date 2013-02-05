"""cartesian coordinate system"""

class Cartesian( object ):
    __slots__ = ['x', 'y']
    def __init__( self, x = 0, y = 0 ):
        self.x, self.y = x, y
    def clone( self ):
        return Cartesian( self.x, self.y )
    def as_tuple( self ):
        return ( self.x, self.y )
    def __iadd__( self, other ):
        self.x += other.x
        self.y += other.y
        return self
    def __imul__( self, other ):
        self.x *= other
        self.y *= other
        return self
    def __mul__( self, other ):
        self.x *= other
        self.y *= other
        return self
