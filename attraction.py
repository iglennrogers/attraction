import pygame
import random
import math

from vertex import Vertex, VertexRing, Cartesian
from physics import Physics


class Shape( object ):
    __slots__ = [ 'colour', 'ring' ]
    def __init__( self, colour, coords ):
        self.colour = colour
        self.ring = coords


class PolygonShape( Shape ):
    def __init__( self, c, r ):
        Shape.__init__( self, c, r )
    def draw( self, surface ):
        return pygame.draw.polygon( surface, self.colour, self.ring.as_coord_pairs() )
    def outline( self, surface ):
        return pygame.draw.polygon( surface, (0,0,0), self.ring.as_coord_pairs(), 1 )


class HollowPolygonShape( Shape ):
    def __init__( self, c, r ):
        Shape.__init__( self, c, r )
    def draw( self, surface ):
        return pygame.draw.polygon( surface, self.colour, self.ring.as_coord_pairs(), 1 )
    def outline( self, surface ):
        pass


class SplineShape( Shape ):
    def __init__( self, c, r ):
        Shape.__init__( self, c, r )
    def draw( self, surface ):
        return pygame.draw.polygon( surface, self.colour, self.ring.as_spline_pairs() )
    def outline( self, surface ):
        return pygame.draw.polygon( surface, (0,0,0), self.ring.as_spline_pairs(), 1 )


class HollowSplineShape( Shape ):
    def __init__( self, c, r ):
        Shape.__init__( self, c, r )
    def draw( self, surface ):
        return pygame.draw.polygon( surface, self.colour, self.ring.as_spline_pairs(), 1 )
    def outline( self, surface ):
        pass


class BallShape( Shape ):
    def __init__( self, c, r ):
        Shape.__init__( self, c, r )
    def draw( self, surface ):
        for b in self.ring:
            pos = ( int(b.position.x), int(b.position.y) )
            pygame.draw.circle( surface, self.colour, pos, b.size )
    def outline( self, surface ):
        pass


class GlowingBallShape( BallShape ):
    def __init__( self, c, r ):
        BallShape.__init__( self, None, r )
    def ball_colour( self, b ):
        if self.colour != (0,0,0):
            v = b.velocity.clone() * (1.0/Physics.MAX_VELOCITY)
            return ( 255, int(255*( 1 - abs(v.x) )), int(255*( 1 - abs(v.y) )) )
        else:
            return self.colour
    def draw( self, surface ):
        try:
            for b in self.ring:
                col = self.ball_colour( b )
                pos = ( int(b.position.x), int(b.position.y) )
                pygame.draw.circle( surface, col, pos, b.size )
        except TypeError:
            pass
    def outline( self, surface ):
        pass


class PolygonShapeChain( object ):
    __slots__ = [ 'shapes', 'segments', 'rear', 'shape_function' ]
    def __init__( self, segments, initial_ring, initial_colour, fn ):
        self.shapes = []
        self.segments = segments
        self.rear = None
        self.shape_function = fn
        self.add_new( initial_ring, initial_colour )
    def last_point_list( self ):
        return self.shapes[-1].ring
    def add_new( self, ring, colour ):
        poly = self.shape_function( colour, ring )
        self.shapes += [ poly ]
        if len( self.shapes ) > self.segments:
            self.rear = self.shapes[0]
            del self.shapes[0]
    def draw( self, surface ):
        if self.rear:
            self.rear.colour = (0,0,0)
            self.rear.draw( surface )
        for sh in self.shapes:
            rc = sh.draw( surface )
        self.shapes[-1].outline( surface )
    def advance( self, world, new_colour ):
        new_ring = self.last_point_list().clone()
        for b in new_ring:
            b.reset_acceleration()
            for o in new_ring:
                if b != o:
                    b.update_acceleration( world, o )
        for b in new_ring:
            b.update_position( world )
        self.add_new( new_ring, new_colour )


def create_initial_ring( surface, points, size ):
    vertex_ring = VertexRing( points )
    midx, midy = surface.get_width()/2.0, surface.get_height()/2.0
    radius = min( surface.get_width(), surface.get_height() )*0.4
    th = 2.0*math.pi*random.randint( 0, 72 )/72.0
    for i in range( 0, points ):
        a = 2.0*math.pi*i/points + th
        #
        b = Vertex()
        b.position = Cartesian( midx + radius*math.sin( a ), midy + radius*math.cos( a ) )
        b.velocity = Cartesian( 0, 0 )
        b.reset_acceleration()
        b.size = size
        vertex_ring.append( b )
    return vertex_ring


class ColourGen( object ):
    def __init__( self ):
        self.current_colour = 0
    def translate( self, col ):
        r = math.radians( col )
        return ( 128, int(127.5 + 127.5*math.sin(r)), int(127.5 + 127.5*math.cos(r)) )
    def current( self ):
        return self.translate( self.current_colour )
    def next_colour( self ):
        self.current_colour += 8
        if self.current_colour >= 360:
            self.current_colour -= 360
        return self.current()
    

class Worker( object ):
    def __init__( self, surface ):
        self.surface = surface
        self.points = 8
        self.segments = 20
        #
        self.world = Physics()
        self.world.set_world( self.surface.get_size() )
        self.world.set_repulsive_threshold( 100.0 )
        self.world.set_viscosity( 0.85 )
        #
        vertex_ring = create_initial_ring( self.surface, self.points, 10 )
        self.colour = ColourGen()
        self.polygon_chain = PolygonShapeChain( self.segments, vertex_ring, self.colour.current(), GlowingBallShape )
        #
    def run( self ):
        self.polygon_chain.draw( self.surface )
        self.polygon_chain.advance( self.world, self.colour.next_colour() )

    
class Screensaver( object ):
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode( (640,480) )
        #self.window = pygame.display.set_mode( (1280,1024), pygame.FULLSCREEN )
        pygame.display.set_caption( "Attraction" )
        self.screen = pygame.display.get_surface()
        self.worker = Worker( self.screen )
        self.running = True
        self.screen.fill( (0,0,0) )
        pygame.display.flip()
    def run(self):
        # look for user input here
        while self.running:
            pygame.time.wait( 100 )
            self.worker.run()
            # our UI input loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    #self.worker.run()
                    if event.key == pygame.K_ESCAPE:
                        # bail out on ESC
                        self.running = False
            # redraw the screen
            pygame.display.flip()
        self.window = None
        pygame.quit()


if __name__ == "__main__":
    Screensaver().run()
