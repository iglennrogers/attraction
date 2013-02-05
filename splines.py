

def third_point( x0, x1 ):
	return ( ( 2*x0[0] + x1[0] )/3.0, ( 2*x0[1] + x1[1] )/3.0 )

def mid_point( x0, x1 ):
	return ( ( x0[0] + x1[0] )/2.0, ( x0[1] + x1[1] )/2.0 )

def can_approx_with_line( p0, p2, p3 ):
	triangle_area = p0[0] * p2[1] - p2[0] * p0[1] + p2[0] * p3[1] - p3[0] * p2[1] + p3[0] * p0[1] - p0[0] * p3[1]
	# actually 4 times the area.
	triangle_area *= triangle_area
	dx = p3[0] - p0[0]
	dy = p3[1] - p0[1]
	side_squared = dx * dx + dy * dy
	return triangle_area <= side_squared

def add_line( s, p0, p1 ):
	if len( s ) == 0:
		s.append( p0 )
	s.append( p1 )

def add_bezier_arc( s, p0, p1, p2, p3 ):
	m01 = mid_point( p0, p1 )
	m12 = mid_point( p1, p2 )
	m23 = mid_point( p2, p3 )
	ml = mid_point( m01, m12 )
	mr = mid_point( m12, m23 )
	c = mid_point( ml, mr )
	#
	if can_approx_with_line( p0, ml, c ):
		add_line( s, p0, c )
	elif m01 != p1 or ml != p2 or c != p3:
		add_bezier_arc( s, p0, m01, ml, c )
	#
	if can_approx_with_line( c, m23, p3 ):
		add_line( s, c, p3 )
	elif c != p0 or mr != p1 or m23 != p2:
		add_bezier_arc( s, c, mr, m23, p3 )

def calc_section( s, cm1, c0, cp1, cp2 ):
	p1 = third_point( c0, cp1 )
	p2 = third_point( cp1, c0 )
	t = third_point( c0, cm1 )
	p0 = mid_point( t, p1 )
	t = third_point( cp1, cp2 )
	p3 = mid_point( t, p2 )
	add_bezier_arc( s, p0, p1, p2, p3 )


def compute_closed_spline( ctrl_list ):
	spline = []
	calc_section( spline, ctrl_list[-1], ctrl_list[0], ctrl_list[1], ctrl_list[2] )
	for s in xrange( 1, len( ctrl_list ) - 2 ):
		calc_section( spline, ctrl_list[s - 1], ctrl_list[s], ctrl_list[s + 1], ctrl_list[s + 2] )
	calc_section( spline, ctrl_list[-3], ctrl_list[-2], ctrl_list[-1], ctrl_list[0] )
	calc_section( spline, ctrl_list[-2], ctrl_list[-1], ctrl_list[0], ctrl_list[1] )
	return spline
