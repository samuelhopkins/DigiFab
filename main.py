import math
import sys
from infill import Infill
import intersection
from line import Line
import perimeter
#import support
from vertex import Vertex

class Gcoder:
  def __init__(self, file, layer_height=.15, shell_no=2, infill=20):
    self.file = file
    self.layer_height = layer_height,
    self.shell_no = shell_no
    self.infill = infill

class Facet:
  def __init__(self, vs=[], normal=Vertex(0,0,0)):
    self.vs = vs
    self.normal = normal
  
  def maxX(self):
    max = 0
    for v in self.vs:
      if max < v.x:
        max = v.x
    return max	
  
  def maxY(self):
    max = 0
    for v in self.vs:
      if max < v.y:
        max = v.y
    return max
  
  def maxZ(self):
    max = 0
    for v in self.vs:
      if max < v.z:
        max = v.z
    return max
   
  def minX(self):
    min = 0
    for v in self.vs:
      if min < v.X:
        min = v.X
    return min
    
  def minY(self):
    min = 0
    for v in self.vs:
      if min < v.y:
        min = v.y
    return min
    
  def minZ(self):
    min = 0
    for v in self.vs:
      if min > v.z:
        min = v.z
    return min

def distance(a,b):
	return math.sqrt(math.pow((b.x-a.x),2) + math.pow((b.y-a.y),2) + math.pow((b.z-a.z),2))

def e(a,b,thickness=.4,diameter=1.75):
	return (distance(a,b) * thickness)/diameter
	
def shell(shell_no, perim, output, thickness, count):
	extrudate = count
	for s in range(1,shell_no+1):
		adj = s*thickness
		line = "G0 X%.3f Y%.3f F%.3f\n" % (perim[0].x+adj, perim[0].y+adj, 2400)
		output.write(line)
		for p in range(1,len(perim)-1):
			dest = perim[p]
			prev = perim[p-1]
			extrudate = extrudate + e(prev.add(Vertex(adj, adj, 0)),
									  dest.add(Vertex(adj, adj, 0)))
			line = "G1 X%.3f Y%.3f E%.5f F%.3f\n" % (dest.x+adj, dest.y+adj, extrudate, 1800)
			output.write(line)
		extrudate = extrudate + e(perim[-1], perim[0])
		line = "G1 X%.3f Y%.3f E%.5f F%.3f\n" % (perim[-1].x+adj, perim[-1].y+adj, extrudate, 1800 )
		output.write(line)
	#	line = "G1 X%.3f Y%.3f\n" % (perim[0].x + s*thickness, perim[0].y + s*thickness)
	#	output.write(line)
	return extrudate
    
def parseFile(f):
	ret = []
	line = f.readline()
	while "endsolid" not in line:
		facet = Facet([])
		line = f.readline()
		if "endsolid" in line:
			break
		while "endfacet" not in line:
			if "facet normal" in line:
				tokens = line.split(" ")
				facet.normal = Vertex(tokens[2], tokens[3], tokens[4])
			elif "vertex" in line: 
				tokens = line.split(" ")
				facet.vs.append(Vertex(float(tokens[7]),
									   float(tokens[8]),
									   float(tokens[9])))
			line = f.readline()

		ret.append(facet)
	f.close()
	return ret

def setF(extrude):
   if extrude: return 1800
   else: return 2400

def infiller(infill_lines, extrude, output, count):
  for i in range(1,len(infill_lines)-1):
    dest = infill_lines[i+1]
    if extrude == 0:
   	  line = "G0 X%.2E Y%.2E F%.2E\n" % (dest.x, dest.y, 2400)
   	  output.write(line)
   	  extrude = 1
    else:
   	  extrudate = e(infill_lines[i], dest)
   	  line = "G0 X%.2E Y%.2E E%.2E F%.2E\n" % (dest.x, dest.y, e, 1800)
    output.write(line)
    extrude = 0


def main():
  #command line arguments: file, layer thickness, #shell layers, %infill (0-100)
	args = []
	print str(sys.argv)
	filename = sys.argv[1]	
	thickness = .4
	layer_height = .15
	shell_no = 2
	infill = .2
	if len(args) >= 3:
		layer_height = float(args[2])
	if len(args) >= 4:
		shell_no = int(args[3])
	if len(args) == 5:
		infill = float(args[4])
	file = open(filename, "r")
	facets = parseFile(file)


	#writing start.gcode
	output = open("output.gcode", "w")
	output.write("G28 X0 Y0 Z0\n")
	output.write("G92 E0\n")
	output.write("G29\n")  
	
	#gcode generator for supports
	
	#find height of given solid
	height = 0
	for f in facets:
		max = f.maxZ()
		if height < max:
			height = float(max)
	print "height: %.3f" % height
	count = 0
	orientation = 0
	z = 0
	fill = Infill()
	while z <= height:
		lines = []
		infill_lines = []
		for f in facets:
			lines.extend(intersection.facetIntersect(f.vs[0], f.vs[1], f.vs[2], z))
		for l in lines:
			l.show()
		print ""
		#print len(lines)
		perims = perimeter.cycleMaker(lines)
		for p in perims:
			print "perimeter"
			for c in p:
				c.show()
			print ""
		count = shell(shell_no, perims[0], output,thickness,count)
		# infill_lines = fill.calculateInfill(perims, orientation, 0, infill)
		# if len(infill_lines) > 0:
			# output.write(";infill start\n")
			# e = distance(infill_lines[0], infill_lines[1])
			# line = "G0 X%.3f Y%.3f F%.3f\n" % (infill_lines[1].x, infill_lines[1].y, 2400)
			# output.write(line)
			# infiller(infill_lines, orientation, output, 1.75)
			# output.write(";infill end\n")
		# if orientation == 0: 
			# orientation = 1
		# else: 
			# orientation = 0
		
		z += layer_height
		line = "G0 X0 Y0 Z%.3f\n" % z
		output.write(line)
		
	output.write(";End GCode\n"
			"M104 S0                     ;extruder heater off\n"
			 "M140 S0                     ;heated bed heater off (if you have it)\n"
    	     "G91                                    ;relative positioning\n"
    	     "G1 E-1 F300                            ;retract the filament a bit before lifting the nozzle, to release some of the pressure\n"
    	     "G1 Z+0.5 E-5 X-20 Y-20 F{travel_speed} ;move Z up a bit and retract filament even more\n"
    	     "G28 X0 Y0                              ;move X/Y to min endstops, so the head is out of the way\n"
    	     "M84                         ;steppers off\n"
    	     "G90                         ;absolute positioning\n"
    	     ";{profile_string}")

   
  #     do shell infill
  #     do infill code
	#writing end-gcode

	

main()
