import os
import sys
import math
from shapely.geometry import LineString

class Infill():

	def distance(self, p1, p2):
		return math.sqrt(((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2))


	def calculateInfill(self, perimeter, orientation, adjustment, infill):
		outer_perimeter = perimeter[0]
		inner_perimeter = perimeter[1]
		sorted_x_outer = sorted(outer_perimeter)
		sorted_y_outer = sorted(outer_perimeter, key=lambda x: x[1])
		top_left_square = (sorted_x_outer[0][0], sorted_y_outer[-1][1])
		top_right_square = (sorted_x_outer[-1][0], sorted_y_outer[-1][1])
		bottom_right_square = (sorted_x_outer[-1][0], sorted_y_outer[0][1])
		bottom_left_square = (sorted_x_outer[0][0], sorted_y_outer[0][1])

		width_square = self.distance(top_left_square, top_right_square)
		height_square = self.distance(top_left_square, bottom_left_square)

		infill_lines = []
		if orientation == 0:
			interval = width_square * infill
			infill_intervals = int(width_square/interval)+1
			for i in range(infill_intervals):
				if i == 0:
					line = ((top_left_square[0],top_left_square[1]), (bottom_left_square[0],bottom_left_square[1]))
				else:
					line = (((top_left_square[0]+(i*interval)), top_left_square[1]), ((bottom_left_square[0]+(i*interval)), bottom_left_square[1]))
				infill_lines.append(self.checkForInfillIntersection(line, outer_perimeter, inner_perimeter))

		if orientation == 1:
			interval = height_square * infill
			infill_intervals = int(height_square/interval)+1
			for i in range(infill_intervals):
				if i == 0:
					line = ((top_left_square[0],top_left_square[1]), (top_right_square[0],top_right_square[1]))
				else:
					line = (((top_left_square[0], top_left_square[1] - (i*interval))), (bottom_right_square[0], top_left_square[1] - (i*interval)))
				infill_lines.append(self.checkForInfillIntersection(line, outer_perimeter, inner_perimeter))
		return self.linkInfillLines(list(infill_lines))

	def linkInfillLines(self, lines):
		linked_lines = []
		for i in range(len(lines)):
			linked_lines.extend([lines[i][0], lines[i][1]])
		return linked_lines

	def checkForInfillIntersection(self, line, outer_perimeter, inner_perimeter):
		intersections = []
		for i in range(len(outer_perimeter)-1):
			points = [line[0], line[1], outer_perimeter[i], outer_perimeter[i+1]]
			intersection = self.findIntersection(points)
			if intersection != []:
				intersections.append(intersection)
		last_line = self.findIntersection([line[0], line[1], outer_perimeter[0], outer_perimeter[-1]])
		if last_line != []:
			intersections.append(last_line)

		if inner_perimeter != []:
			for i in range(len(inner_perimeter)-1):
				points = [line[0], line[1], inner_perimeter[i], inner_perimeter[i+1]]
				intersection = self.findIntersection(points)
				if intersection != []:
					intersections.append(intersection)
			last_line = self.findIntersection([line[0], line[1], inner_perimeter[0], inner_perimeter[-1]])
			if last_line != []:
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

if __name__=="__main__":
	infill = Infill()
	perimeters = ([(0,0,0), (0,1,0), (1,1,0),(1,0,0)],[])
	print infill.calculateInfill(perimeters, 1, 0.1, 0.1)
	#print infill.checkForInfillIntersection(((0, 1), (1, 1)), perimeters[0], [] )
	#print infill.findIntersection([(0,1),(2,0),(0,0),(2,2)])
