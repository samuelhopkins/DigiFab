import os
import sys
import math
from vertex import Vertex
from shapely.geometry import LineString

class Infill():

	def distance(self, p1, p2):
		return math.sqrt(((p2[0] - p1[0])**2 + (p2[1] - p2[1])**2))

	def calculateInfill(self, perimeter, orientation, adjustment, infill):
		outer_perimeter = perimeter[0]
		print ""
		#print "outer perimeter"
		#for p in outer_perimeter:
		#	p.show()
		if len(perimeter) < 2:
			inner_perimeter = []
		else:
			inner_perimeter = perimeter[1]
		sorted_x_outer = sorted(outer_perimeter, key=lambda x: x.x)
		sorted_y_outer = sorted(outer_perimeter, key=lambda x: x.y)
		top_left_square = Vertex(sorted_x_outer[0].x, sorted_y_outer[-1].y, 0)
		top_right_square = Vertex(sorted_x_outer[-1].x, sorted_y_outer[-1].y, 0)
		bottom_right_square = Vertex(sorted_x_outer[-1].x, sorted_y_outer[0].y, 0)
		bottom_left_square = Vertex(sorted_x_outer[0].x, sorted_y_outer[0].y, 0)

		width_square = self.distance((top_left_square.x, top_right_square.y), (top_right_square.x, top_right_square.y))
		height_square = self.distance((top_left_square.x, top_left_square.y), (bottom_left_square.x, bottom_left_square.y))

		infill_lines = []
		if orientation == 0:
			interval = width_square * infill
			if interval == 0:
				return []
			try:
				infill_intervals = int((width_square+interval-1)/interval)
			except ZeroDivisionError:
				return []
			for i in range(infill_intervals):
				if i == 0:
					line = ((top_left_square.x+adjustment,top_left_square.y-adjustment), (bottom_left_square.x+adjustment,bottom_left_square.y+adjustment))
				else:
					line = (((top_left_square.x+(i+interval)), top_left_square.y - adjustment), ((bottom_left_square.x+(i+interval)), bottom_left_square.y + adjustment))
				infill_lines.append(self.checkForInfillIntersection(line, outer_perimeter, inner_perimeter))

		if orientation == 1:
			interval = height_square * infill
			try:
				infill_intervals = int((height_square+interval-1)/interval)
			except ZeroDivisionError:
				return []
			for i in range(infill_intervals):
				if i == 0:
					line = ((top_left_square.x+adjustment,top_left_square.y-adjustment), (top_right_square.x-adjustment,top_right_square.y-adjustment))
				else:
					line = (((top_left_square.x+adjustment, top_left_square.y - (i*interval))), (bottom_right_square.x+adjustment, top_left_square.y - (i*interval)))
				infill_lines.append(self.checkForInfillIntersection(line, outer_perimeter, inner_perimeter))
		return self.linkInfillLines(infill_lines)

	def linkInfillLines(self, lines):
		linked_lines = []
		for i in range(len(lines)):
			linked_lines.extend([Vertex(lines[i][0][0],lines[i][0][1], 0),Vertex(lines[i][1][0], lines[i][1][1], 0)])
		return linked_lines

	def checkForInfillIntersection(self, line, outer_perimeter, inner_perimeter):
		intersections = []
		for i in range(len(outer_perimeter)-1):
			points = [line[0], line[1], (outer_perimeter[i].x, outer_perimeter[i].y), (outer_perimeter[i+1].x, outer_perimeter[i+1].y)]
			intersection = self.findIntersection(points)
			if intersection != []:
				intersections.append(intersection)

		if inner_perimeter:
			for i in range(len(inner_perimeter)-1):
				points = [line[0], line[1], inner_perimeter[i], inner_perimeter[i+1]]
				intersection = self.findIntersection(points)
				if intersection != []:
					intersections.append(intersection) 

		intersections = sorted(intersections, key=lambda x: x[1])
		unique = []
		[unique.append(item) for item in intersections if item not in unique]
		return (unique[0], unique[1])

	def findIntersection(self,points):
		line1 = LineString([points[0], points[1]])
		line2 = LineString([points[2], points[3]])
		try:
			intersect = line1.intersection(line2)
			return intersect.coords[0]
		except NotImplementedError:
			return []

# if __name__=="__main__":
	# infill = Infill()
	# print infill.findIntersection([(0,1),(2,0),(0,0),(2,2)])
	# #print infill.checkForInfillIntersection(((0, 1), (1, 1)), perimeters[0], [] )
