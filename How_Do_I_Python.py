#This is so weird how I don't have to write a whole bunch of
#definitions at the top for this to work what is Python magic

#returns parameterization of two points
def pointsToLine(p1,p2):
	return (p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2])

def crossProd(v1,v2):
	return (v1[1]*v2[2]-v1[2]*v2[1],
			v1[2]*v2[0]-v1[0]*v2[2],
			v1[0]*v2[1]-v1[1]*v2[0])

#given two points and the z coord of the flat plane
#find the intersection created by the line segment and plane
#if line is on the plane, returns with the z value = -1
#  (shouldn't happen normally since z should always be positive)
#if line doesn't intersect plane, the function returns with z = -2
def planeIntersect(p1,p2,zval):

	#plane definitely doesn't cross line seg
	if !(((p1[2] <= zval) && (p2[2] >= zval))
		 || ((p1[2] >= zval) && (p2[2] <= zval))):
		return (0,0,-2)

	x = (p1[0], p2[0]-p1[0])
	y = (p1[1], p2[1]-p1[1])
	z = (p1[2], p2[2]-p2[2])
	t = (zval-z[0])/z[1]
	if z[1] == 0:
		if z[0] == zval:
			#line is on plane
			return (0,0,-1)
		else:
			#line parallel to plane
			return (0,0,-2)
	else:
		return (x[0]+x[1]*t, y[0]+y[1]*t, z[0]+z[1]*t)


#holy this function had way more cases than I thought there was
#returns a ***LIST*** of lines that intersect the plane
def facetIntersect(v1,v2,v3,zval):
	# all the points that could potentially cross w/plane
	 p1 = planeIntersect(v1,v2,zval)
	 p2 = planeIntersect(v2,v3,zval)
	 p3 = planeIntersect(v3,v1,zval)
	 ret = []

	 #cases where one edge of the triangle lies on the plane
	 #    or the triangle is on the plane
	 if p1[2] == -1:
	 	ret.append(pointsToLine(v1,v2))
	 if p2[2] == -1:
	 	ret.append(pointsToLine(v2,v3))
	 if p3[2] == -1:
	 	ret.append(pointsToLine(v3,v1))

	 if len(ret) > 0:
	 	return ret

	 #case where the triangle doesn't intersect the plane at all
	 if p1[1] == -2 && p2[1] == -2 && p3[1] == -2:
	 	return ret

	 #cases where the plane intersects the middle of the triangle 
	 #   and one edge does not intersect the plane
	 if p1[2] == -2:
	 	ret.append(pointsToLine(v1,v2))
	 elif p2[2] == -2:
	 	ret.append(pointsToLine(v2,v3))
	 elif p3[2] == -2:
	 	ret.append(pointsToLine(v3,v1))
	 else:
	 	tba = list(set([p1,p2,p3]))

	 	#cases where plane only intersects at 1 vertex
	 	if len(tba) == 1:
	 		return ret

	 	#cases where plane intersects on one vertex, but intersects
	 	#   at another point 
	 	if len(tba) == 2: 
	 		return [(tba[0],tba[1])]

	 return ret 

def allStlFacets(facetList, zval):
	ret = []
	while len(facetList)!= 0:
		v = pop(facetList)
		ret.expand(facetIntersect(v[0], v[1], v[2], zval))

	return ret




