import random
import math

import cartesian


class Physics( object ):
    __slots__ = [ 'extent', 'viscosity', 'threshold' ]
    MAX_VELOCITY = 10.0
    def __init__( self ):
        self.extent = ( 640, 512 )
        self.viscosity = 1.0
        self.threshold = 100.0
    def set_world( self, xy ):
        self.extent = cartesian.Cartesian( xy[0], xy[1] )
    def set_repulsive_threshold( self, thr ):
        self.threshold = thr
    def set_viscosity( self, v ):
        self.viscosity = v
    def attractive_force( self, basis, pos, mass ):
        dx = basis.x - pos.x
        dy = basis.y - pos.y
        dist2 = dx*dx + dy*dy
        dist = math.sqrt( dist2 )
        if dist > 0.1:
            new_acc = -mass/( dist2 * dist )
            if dist < self.threshold:
                new_acc = -new_acc
            return cartesian.Cartesian( new_acc*dx, new_acc*dy )
        else:
            return cartesian.Cartesian( random.randint( -5, 5 ), random.randint( -5, 5 ) )
        #
    def apply_viscosity( self, vel ):
        nv = vel.clone()
        nv.x *= self.viscosity
        if abs( nv.x ) > Physics.MAX_VELOCITY:
            # print( nv.x )
            nv.x = max( min( nv.x, Physics.MAX_VELOCITY ), -Physics.MAX_VELOCITY )
        nv.y *= self.viscosity
        if abs( nv.y ) > Physics.MAX_VELOCITY:
            # print( nv.y)
            nv.y = max( min( nv.y, Physics.MAX_VELOCITY ), -Physics.MAX_VELOCITY )
        return cartesian.Cartesian( nv.x, nv.y )
        #
    def limit_to_world( self, pos, vel ):
        if pos.x > self.extent.x:
            pos.x = self.extent.x
            vel.x *= -1
        if pos.x < 0:
            pos.x = 0
            vel.x *= -1
        if pos.y > self.extent.y:
            pos.y = self.extent.y
            vel.y *= -1
        if pos.y < 0:
            pos.y = 0
            vel.y *= -1
        #
