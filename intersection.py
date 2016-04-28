import math
import sys
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
		#print "no intersection"
		return Vertex(0,0,-2)

	x = (float(p1.x), p2.x-p1.x)
	y = (float(p1.y), p2.y-p1.y)
	z = (float(p1.z), p2.z-p1.z)
	#print "z = %.2f %.2f" % (z[0], z[1])
	if z[1] == 0:
		if z[0] == zval:
			#line is on plane
			#print "line is on the plane"
			return Vertex(0,0,-1)
		else:
			#line parallel to plane
			#print "line parallel to plane"
			return Vertex(0,0,-2)
	else:
		#print "t = %.2f/%.2f" % (zval - z[0], z[1])	
		t = (zval-z[0])/float(z[1])
		#print ">>>>>>>>>>plane intersection"
		#print "t = %.2f" % t
		#p1.show()
		#p2.show()
		#p3 = Vertex(x[0]+x[1]*t, y[0]+y[1]*t, zval)
		#p3.show()
		#print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
		return Vertex(x[0]+x[1]*t, y[0]+y[1]*t, zval)

def remDupPts(v1,v2,v3):
	ret = []
	if v1.eq(v2) and v1.eq(v3):
		return [v1]
	elif v1.eq(v2) and not v1.eq(v3):
		return [v1,v3]
	elif not v1.eq(v2) and v1.eq(v3):
		return [v1,v2]
	elif v1.eq(v2) and not v2.eq(v3):
		return [v2,v3]
	else:
		return [v1,v2,v3]

#holy this function had way more cases than I thought there was
#returns a ***LIST*** of lines that intersect the plane
def facetIntersect(v1,v2,v3,zval):
	# all the points that could potentially cross w/plane
	p1 = planeIntersect(v1,v2,zval)
	p2 = planeIntersect(v2,v3,zval)
	p3 = planeIntersect(v3,v1,zval)
	#p1.show()
	#p2.show()
	#p3.show()
	ret = []
	
	#case where the triangle lies on the plane, throw it out
	if p1.z == -1 and p2.z == -1 and p3.z == -1:
 		print "on plane"
	 	return []

	#cases where one edge of the triangle lies on the plane
	if p1.z == -1:
		ret.append(Line(v1,v2))
		#print "Line v1,v2: " 
		#Line(v1,v2).show()
	elif p2.z == -1:
	 	ret.append(Line(v2,v3))
		#print "Line v2,v3:"
		#Line(v2,v3).show()
	elif p3.z == -1:
	 	ret.append(Line(v3,v1))
		#print "Line v3, v1:"
		#Line(v3,v1).show()
	if len(ret) > 0:
	 	print "one edge"
	 	return ret

	#case where the triangle doesn't intersect the plane at all
	if p1.z == -2 and p2.z == -2 and p3.z == -2:
		#print "triangle doesn't intersect plane"
		print "no intersection"
	 	return ret

	#cases where the plane intersects the middle of the triangle 
	#   and one edge does not intersect the plane
	tba = remDupPts(p1,p2,p3)
	#print "tba: %.2f" % len(tba)

	#cases where plane only intersects at 1 vertex
	if len(tba) == 2 and (p1.z == -2 or p2.z == -2 or p3.z == -2):
		print "one vertex"
		return ret

	#cases where plane intersects on one vertex, but intersects
	#   at another point 
	if len(tba) == 2: 
		print "one vertex middle"
		return ret.append(Line(tba[0],tba[1]))

	if p1.z == -2:
	 	ret.append(Line(p2,p3))
	elif p2.z == -2:
	 	ret.append(Line(p1,p3))
	elif p3.z == -2:
	 	ret.append(Line(p1,p2))	 	
	print "middle"
	return ret 

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

# def main():
# 	  #command line arguments: file, layer thickness, #shell layers, %infill (0-100)
# 	thickness = .4
# 	layer_height = 1
# 	shell_no = 2
# 	infill = .2

# 	vers = (Vertex(0,0,0),
# 			Vertex(0,10,0),
# 			Vertex(10,0,0),
# 			Vertex(10,10,0),
# 			Vertex(0,0,10),
# 			Vertex(0,10,10),
# 			Vertex(10,0,10),
# 			Vertex(10,10,10))

# 	facets = ((vers[0], vers[1], vers[2]),
# 			  (vers[1], vers[2], vers[3]),
# 			  (vers[0], vers[4], vers[5]),
# 			  (vers[0], vers[4], vers[1]),
# 			  (vers[0], vers[4], vers[2]),
# 			  (vers[0], vers[4], vers[6]),
# 			  (vers[4], vers[5], vers[6]),
# 			  (vers[5], vers[6], vers[7]),
# 			  (vers[3], vers[7], vers[1]),
# 			  (vers[3], vers[7], vers[2]),
# 			  (vers[3], vers[7], vers[5]),
# 			  (vers[3], vers[7], vers[6]))


# 	z = 0
# 	height = 10
# 	while z <= height:
# 		print "*********************************************************"
# 		print z
# 		lines = []	
# 		for f in facets:
# 			boo = facetIntersect(f[0], f[1], f[2], z)
# 			lines.extend(boo)
# 			#print "intersection num: %.2f" % len(boo)
# 		z = z + layer_height


# main()