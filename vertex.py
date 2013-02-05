import random

from splines import compute_closed_spline
from physics import Physics
from cartesian import Cartesian


class Vertex( object ):
    MAX_BALL_SIZE = 16
    __slots__ = [ 'position', 'velocity', 'accel', 'size', 'mass' ]
    def __init__( self ):
        pass
    def __setattr__( self, name, value ):
        newval = value
        if name == 'velocity':
            newval = value.clone()
            if newval.x == 0:
                newval.x = random.randint( -Physics.MAX_VELOCITY, Physics.MAX_VELOCITY )/2
            if newval.y == 0:
                newval.y = random.randint( -Physics.MAX_VELOCITY, Physics.MAX_VELOCITY )/2
        elif name == 'size':
            if newval == 0:
                newval = random.randint( Vertex.MAX_BALL_SIZE/2, Vertex.MAX_BALL_SIZE )
            object.__setattr__( self, 'mass', newval*newval*10 )
        elif name == 'mass':
            raise AttributeError
        object.__setattr__( self, name, newval )
    def clone( self ):
        c = Vertex()
        c.position = self.position.clone()
        c.velocity = self.velocity.clone()
        c.accel = self.accel.clone()
        c.size = self.size
        return c
    def reset_acceleration( self ):
        self.accel = Cartesian()
    def update_acceleration( self, physics, other ):
        change = physics.attractive_force( self.position, other.position, other.mass )
        self.accel += change
    def update_position( self, physics ):
        self.velocity += self.accel
        physics.apply_viscosity( self.velocity )
        self.position += self.velocity
        physics.limit_to_world( self.position, self.velocity )


class VertexRing( list ):
    def __init__( self, num_items ):
        list.__init__( self )
        self.num_items = num_items
        self.coord = None
        self.spline = None
    def clone( self ):
        cp = VertexRing( self.num_items )
        for item in self:
            cp.append( item.clone() )
        return cp
    def as_coord_pairs( self ):
        if not self.coord:
            self.coord = []
            for v in self:
                self.coord += [( v.position.x, v.position.y )]
            self.coord += [ self.coord[0] ]
        return self.coord
    def as_spline_pairs( self ):
        if not self.spline:
            splist = self.as_coord_pairs()
            self.spline = compute_closed_spline( splist )
        return self.spline
    
