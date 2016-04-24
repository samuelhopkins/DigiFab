import os
import sys
import math
from shapely.geometry import LineString


def distance(p1, p2):
	return math.sqrt(((p2[0] - p1[0])**2 + (p2[1] - p2[1])**2))

def calculateInfill(perimeter, orientation, adjustment, infill):
	outer_perimeter = perimeter[0]
	inner_perimeter = perimeter[1]
	sorted_x_outer = sorted(outer_perimeter)
	sorted_y_outer = sorted(outer_perimeter, key=lambda x: x[2])
	top_left_square = (sorted_x_outer[-1], sorted_y_outer[0])
	top_right_square = (sorted_x_outer[0], sorted_y_outer[0])
	bottom_right_square = (sorted_x_outer[0], sorted_y_outer[-1])
	bottom_left_square = (sorted_x_outer[-1], sorted_y_outer[-1])

	width_square = distance(top_left_square, top_right_square)
	height_square = distance(top_left_square, bottom_left_square)

	infill_lines = []
	if orientation == 0:
		interval = width_square * infill
		infill_intervals = width_square/interval
		for i in range(infill_intervals):
			if i == 0:
				line = ((top_left_square[0]+adjustment,top_left_square[1]-adjustment), (bottom_left_square[0]+adjustment,bottom_left_square[1]+adjustment))
			else:
				line = (((top_left_square[0]+(i+interval)), top_left_square[1] - adjustment), ((bottom_left_square[0]+(i+interval)), bottom_left_square[1] + adjustment))
			infill_lines.append(checkForInfillIntersection(line, outer_perimeter, inner_perimeter))


def checkForInfillIntersection(line, outer_perimeter, inner_perimeter):
	intersections = []
	for i in range(len(outer_perimeter)-1):
		points = [line[0], line[1], outer_perimeter[i], outer_perimeter[i+1]]
		intersection = findIntersection(points)
		intersections.append(intersection)

	for i in range(len(outer_perimeter)-1):
		points = [line[0], line[1], outer_perimeter[i], outer_perimeter[i+1]]
		intersection = findIntersection(points)
		intersections.append(intersection) 
	intersections = sorted(intersections, key=lambda x: x[1])
	return (intersections[0], intersections[1])

def findIntersection(points):
	line1 = LineString([points[0], point[1]])
	line2 = LineString([points[2], points[3]])
	return line1.intersection(line2)

