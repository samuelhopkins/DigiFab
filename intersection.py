import math
from line import Line
from vertex import Vertex

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
	if not (((p1.z <= zval) and (p2.z >= zval))
		or ((p1.z >= zval) and (p2.z <= zval))):
		print "no intersection"
		return Vertex(0,0,-2)

	x = (p1.x, p2.x-p1.x)
	y = (p1.y, p2.y-p1.y)
	z = (p1.z, p2.z-p1.z)
	if z[1] == 0:
		if z[0] == zval:
			#line is on plane
			print "line is on the plane"
			return Vertex(0,0,-1)
		else:
			#line parallel to plane
			print "line parallel to plane"
			return Vertex(0,0,-2)
	else:
		t = (zval-z[0])/z[1]
		print "plane intersection"
		return Vertex(x[0]+x[1]*t, y[0]+y[1]*t, zval)


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
	 if p1.z == -1:
	 	ret.append(Line(v1,v2))
		print "Line v1,v2: " 
		Line(v1,v2).show()
	 if p2.z == -1:
	 	ret.append(Line(v2,v3))
		print "Line v2,v3:"
		Line(v2,v3).show()
	 if p3.z == -1:
	 	ret.append(Line(v3,v1))
		print "Line v3, v1:"
		Line(v3,v1).show()
	 if len(ret) > 0:
	 	return ret

	 #case where the triangle doesn't intersect the plane at all
	 if p1.z == -2 and p2.z == -2 and p3.z == -2:
		print "triangle doesn't intersect plane"
	 	return ret

	 #cases where the plane intersects the middle of the triangle 
	 #   and one edge does not intersect the plane
	 if p1.z == -2:
	 	ret.append(Line(p2,p3))
		print "Middle"
	 elif p2.z == -2:
		print "MIddle"
	 	ret.append(Line(p1,p3))
	 elif p3.z == -2:
		print "Middle"
	 	ret.append(Line(p1,p2))
	 else:
	 	tba = list(set([p1,p2,p3]))

	 	#cases where plane only intersects at 1 vertex
	 	if len(tba) == 1:
	 		return ret

	 	#cases where plane intersects on one vertex, but intersects
	 	#   at another point 
	 	if len(tba) == 2: 
	 		return ret.append(Line(tba[0],tba[1]))
	 		
	 return ret 

def removeDup(linesList):
	lines = list(set(lines))
	for i in lines:
		for j in lines:
			if i.eq(j):
				lines.remove(j)
				
	return lines
