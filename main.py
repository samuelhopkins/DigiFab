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
  
  for z in range(starting_height, height, coder.layer_height):
    lines = []
    for f in facets:
      lines.extend(facetIntersect(f.vs.x, f.vs.y, f.vs.z, z))
    removeDup(lines)
    perims = Perimeter.cyclemaker(lines)

  # for every increment of self.layer_height from 0 to height:
  #     for every facet in the .stl file:
  #         retrieve a line(s) that intersects with the cutting plane
  #     combine all lines into a list of lines
  #     assemble all lines into a list of perimeters
  #     do shell infill
  #     do infill code
