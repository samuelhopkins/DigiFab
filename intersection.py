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
		return Vertex(x[0]+x[1]*t, y[0]+y[1]*t, z[0]+z[1]*t)


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
	 print len(ret)
	 if len(ret) == 0:
		print "ret empty"
	 	return ret

	 #case where the triangle doesn't intersect the plane at all
	 if p1.y == -2 and p2.y == -2 and p3.y == -2:
		print "triangle doesn't intersect plane"
	 	return ret

	 #cases where the plane intersects the middle of the triangle 
	 #   and one edge does not intersect the plane
	 if p1.z == -2:
	 	ret.append(Line(v1,v2))
		print "Middle"
	 elif p2.z == -2:
		print "MIddle"
	 	ret.append(Line(v2,v3))
	 elif p3.z == -2:
		print "Middle"
	 	ret.append(Line(v3,v1))
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

def distToOrigin(v1):
	math.sqrt(math.pow(v1.x,2) + math.pow(v1.y,2))

def dist(v1,v2):
	math.sqrt(math.pow(v1.x-v2.x,2) + math.pow(v1.y-v2.y,2))

#after removing duplicate lines, call this
#first find the center of the shape
#then for lines sharing an endpoint, 
def findperim(linesList):
	cto = distToOrigin(linesList[0].a)
	ctov = linesList[0].a
	for i in linesList:
		if distToOrigin(linesList[i].a) < cto:
			cto = distToOrigin(linesList[i].a)
			ctov = linesList[i].a
		elif distToOrigin(linesList[i].b) < cto:
			cto = distToOrigin(linesList[i].b)
			ctov = linesList[i].b
		else:
			pass

	#now cto should have the point closest to the origin
	#now we find the point farthest to the origin
	fto = distToOrigin(linesList[0].a)
	ftov = linesList[0].a
	for i in linesList:
		if distToOrigin(linesList[i].a) > fto:
			fto = distToOrigin(linesList[i].a)
			ftov = linesList[i].a
		elif distToOrigin(linesList[i].b) > fto:
			fto = distToOrigin(linesList[i].b)
			ftov = linesList[i].b
		else:
			pass

	#now we find the midpoint
	mid = Vertex((ftov.x-ctov.x)/2, (ftov.y-ctov.y)/2, ftov.z)

	#now we try to find the perimeter based on these facts:
	#find a line segment in which either point is the same as the previous
	#if multiple ones, then store the one with the least distance to mid
	ret = []
	ret.append(ctov)
	last = ctov
	d = 99999
	tba = Vertex(-1,-1,-1)
	dtba = 99999
	while not last.eq(ctov):
		for i in linesList:
			if linesList[i].a.eq(last) and dist(mid,linesList[i].b) >= d and dist(last, linesList[i].b) <= dtba:
				tba = linesList[i].b
				d = dist(mid, linesList[i].b)
				dtba = dist(last, linesList[i].b)
			elif linesList[i].b.eq(last) and dist(mid,linesList[i].a) >= d and dist(last, linesList[i].a) <= dtba:
				tba = linesList[i].a
				d = dist(mid, linesList[i].a)
				dtba = dist(last, linesList[i].a)
			else:
				pass
			d = 99999
			dtba = 99999
			ret.append(tba)
			last = linesList[i].a

	return ret