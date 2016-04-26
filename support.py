import math
from main import Facet
class Support:
  def __init__(self, loc):
    self.loc =  loc
    # loc is a Vertex holding the support's (fixed x pos, fixed y pos, target height)
    # The current height of a support point is given by z in the main loop in main()

class SupportLine:
  def __init__(self, horiz=[], vert=[]):
    self.horiz = horiz
    self.vert = vert

def supportMaker(facets, min_support):
  ret = []
  cutting_plane = Facet([Vertex(0,0,0), Vertex(100,0,0), Vertex(0,100,0), Vertex(100,100,0)],
                        Vertex(1,1,0))
    # a perfectly horizontal x-y plane
  for f in facets:
    if f.normal.z <= 0:
      angle = arccos(f.normal.dot(cutting_plane.normal)/(f.normal.mag()*cutting_plane.normal()))
      angle = 90 - angle
        # Cura's support angle has 0 as vertical (90 degrees) and 90 as horiz (0 degrees)
      if angle >= min_support:
        ret.append(Support(Vertex(f.minX()+(f.maxX()-f.minX())/2,
                                  f.minY()+(f.maxY()-f.minY())/2,
                                  f.minZ()+(f.maxZ()-f.minZ())/2)))
  return ret

def supportLiner(supports, facet, spacer, filament_width): #spacer received as a decimal, like infill
  ret = SupportLine()

  for i in range(facet.minX(), facet.maxX(), filament_width/spacer):
    for s in supports:
      if s.loc.x == i:
        dup = False
        for h in ret.horiz:
          if s in h:
            dup = True
            break
        if dup == False: # the current Support point is not in a support line; make a new one
         ret.horiz.append([])
        ret.horiz.append(s)
  
  for i in range(facet.minY(), facet.maxY(), filament_width/spacer):
    for s in supports:
      if s.loc.y == i:
        dup = False
        for v in ret.vert:
          if s in v:
            dup = True
            break
        if dup == False: # the current Support point is not in a support line; make a new one
        ret.vert.append([])
        ret.vert.append(s)
  for s in supports:
    in_line = False
    for h in ret.horiz:
      if s in h:
        in_line = True
    if in_line == False:
      for v in ret.vert:
        if s in v:
          in_line = True
    if in_line == False:
      supports.remove(s)
  return ret

# returns an array of Lines composed of the end points of each support line
def supportLinetoLine(sl):
    ret = []
    for h in sl.horiz:
      ret.extend(h[0], h[len(h)]-1)
    for v in sl.vert:
      ret.extend(v[0], v[len(v)-1])
    return ret    

def distance(a,b):
    return sqrt((b.x-a.x)^2 + (b.y-a.y)^2 + (b.z-a.z)^2)

def supportConnector(sl, ret):
  min = 1000000
  min_index = 0
  for i in sl:
    if i not in ret:
      dist = distance(ret[len(ret)-1].loc, i.loc) # distance from current endpt to next possible vertex
      if min > dist:
          min = dist
          min_index = sl.loc(i)
  ret.append(sl[min_index])
  
def brimBuilder(sl, output, brim_no, filament_width):
  ret = []
  ret.append(sl[0]
  for i in sl:
      ret = baseBuilder(sl, ret)
      # ret should now be a cycle of the endpoints of the support lines
  line = "G1 X%.2E Y%.2E F%.2E" % (ret[0].loc.x, ret[0].loc.y, 2400)
  for i in range(brim_no):
      adj = i * filament_width
      line = "G1 X%.2E Y%.2E F%.2E" % (ret[0].loc.x+adj, ret[0].loc.y+adj, 2400)
      for j in range(1,len(ret)-1):
        e = dist(ret[j].loc, ret[j-1].loc)
        line = "G1 X%.2E Y%.2E F%.2E E%.2E" % (ret[j].loc.x+adj, ret[j].loc.y+adj, 1800, e)
        output.write(line)
      line = "G1 X%.2E Y%.2E F%.2E E%.2E" % (ret[0].loc.x+adj, ret[0].loc.y+adj, 1800, e)
      output.write(line)



      
            
      
  
  
