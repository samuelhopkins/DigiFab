import sys

class Gcoder:
  def __init__(self, file, layer_height=.15, shell_no=2, infill=20):
    self.file = file
    self.layer_height = layer_thickness,
    self.shell_no = shell_no
    self.infill = infill

class Facet:
  def __init__(self, vs=[], normal=Vertex(0,0,0)):
    self.vs = vs
    self.normal = normal
  
  def maxZ(self):
    max = 0
    for v in self.vs:
      if max < v.z:
        max = v.z
    return max
    
def shell(shell_no, perim, output, thickness):
  for s in range(shell_no):
    for p in range(0,len(perim.pts)-1):
    	current = perim.pts[p]
    	dest = perim.pts[p+1]
    	e = Infill.distance(current, dest)
    	line = "G0 X%.2E Y%.2E E.2E F%.2E" % (dest.x, dest.y, e, #f)
    	output.write(line)
    e = Infill.distance(perim.pts[len(perim.pts)-1], perim.pts[0])
    line = "G0 X%.2E Y%.2E E%.2E" % (perim.pts[0].x, perim.pts[0].y, e)
    output.write(line)
    line = "G0 %X.2E Y%.2E" % (perim.pts[0].x + thickness, perim.pts[0].y + thickness)
    output.write(line)
    	
def parseFile(file):
  ret = []
	f = open(self.file, "r")
	line = f.readline()
	while "endsolid" not in line:
		facet = Facet()
		line = f.readline()
	  while "endfacet" not in line:
			if "facet normal" in line:
			  tokens = line.split(" ")
				facet.normal = Vertex(tokens[2], tokens[3], tokens[4])
			elif "vertex" in line:
				tokens = line.split(" ")
				facet.vs.append(tokens[1])
				facet.vs.append(tokens[2])
				facet.vs.append(tokens[3])
			else:
				pass
		ret.append(facet)
	f.close()
  return ret

def setF(extrude):
   if extrude: return 1800
   else: return 2400

def infiller(infill_lines, extrude, output):
 for i in range(1,len(infill_lines)-1):
   dest = infill_lines[i+1]
   if extrude == 0:
   	line = "G0 X%.2E Y%.2E F%.2E" % (dest.x, dest.y, 2400)
   	output.write(line)
   	extrude == 1
   else:
   	e = Infill.distance(i, dest)
   	line = "G0 X%.2E Y%.2E E%.2E F%.2E" % (dest.x, dest.y, e, 1800)
	output.write(line)
	extrude == 0

def main(self):
  #command line arguments: file, layer thickness, #shell layers, %infill (0-100)
  args = []
  for i in range(1,len(sys.argv)-1):
    args.append(i)
  coder = GCoder(args)
  facets = parser(coder.file)
  #writing start.gcode
  output = file.open("output.gcode", "w")
  output.write("G28 X0 Y0 Z0")
  output.write("G92 E0")
  output.write("G29")
  
  #gcode generator for supports
 
  #find height of given solid
  height = 0:
  for f in facets:
    max = f.maxZ()
    if height < max:
      height = max
  
  orientation = 0
  for z in range(starting_height, height, coder.layer_height):
    lines = []
    for f in facets:
      lines.extend(facetIntersect(f.vs.x, f.vs.y, f.vs.z, z))
    perims = Perimeter.cyclemaker(lines)
    shell(coder.shell_no, perims[0], coder.infill, 

    infill_lines = Infill.calculateInfill(perims, orientation, adjustment, coder.infill)
    e = Infill.distance(infill_lines[0], infill_lines[1])
    line = "G0 X%.2E Y%.2E F%.2E" % (infill_lines[1].x, infill_lines[1].y, 2400)
    output.write(line)
    infiller(infill_lines, extrude, output, 1.75)
    
    if orientation == 0: orientation = 1
    else: orientation = 0
    						 
  #     do shell infill
  #     do infill code
