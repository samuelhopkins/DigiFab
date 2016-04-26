import math
from line import Line
from vertex import Vertex

class Perimeter:
	def __init__(self, pts):
		self.pts = pts
	
	def checkDupLine(self, i):
		if i.a in self.pts and i.b in self.pts:
			return True
		return False
	
	def show(self):
		for i in self.pts:
			i.show()
	
	def checkClosed(self, lines):
		closed = False
		for p in range(0,len(self.pts)-1):
			connection = False
			for i in lines:
				if (self.pts[p].eq(i.a) and self.pts[p+1].eq(i.b)
					or self.pts[p].eq(i.b) and self.pts[p+1].eq(i.a)):
					connection = True
			if connection == True:
				return True
		return False
			
		
		for i in range(0,len(self.pts)-1):
			if (Line(self.pts[i], self.pts[i+1]) not in lines 
				or Line(self.pts[i+1], self.pts[i]) not in lines):
				return False
		if (Line(self.pts[len(self.pts)-1], self.pts[0]) not in lines
			or Line(self.pts[0], self.pts[len(self.pts)-1]) not in lines):
			return True
		return False

	
	def connected(self,a,b,lines):
		for i in lines:
			if a.eq(b):
				return True
		return False
	
	def reorder(self, lines):
		for i in range(0,len(self.pts)-1):
			for j in range(0,len(self.pts)-1):
				if self.connected(self.pts[i], self.pts[j], lines):
					pass
				else:
					self.pts[i],self.pts[j] = self.pts[j], self.pts[i]
	
	def removeDupVertex(self):
		for i in self.pts:
			times = 0
			for j in self.pts:
				if i.eq(j) == True:
					times = times + 1
				if times > 1:
					self.pts.remove(j)
	
	def eq(self, j):
		dup = 0
		if len(self.pts) == len(j.pts):
			for a in self.pts:
				for b in range(0,len(j.pts)):
					if a.eq(j.pts[b]):
						dup = dup + 1
		if dup == len(self.pts):
			return True
	
	@classmethod
	def cycleMaker(self, lines):
		ps = []
		for i in lines:
			added = 0
			for p in ps:
				if p.checkDupLine(i): # skip exact duplicate lines
					break
				else:
					# append the new vertex
					# if p contains [0,1] and i=[1,2]
					# append 2, st p=[0,1,2]
					for v in p.pts:
						if p.connected(v,i.a,lines) and i.a not in p.pts: 
							p.pts.insert(p.pts.index(v)+1,i.b)
							added = 1
							p.reorder(lines)
						elif p.connected(v,i.b,lines) and i.b not in p.pts:
							p.pts.insert(p.pts.index(v)+1,i.a)
							added = 1
							p.reorder(lines)
			# if the current line cannot be added to any existing perimeter
			#	make it the seed of a new perimeter
			if added == 0:
				a = Perimeter([i.a,i.b])
				ps.append(Perimeter(pts=[i.a,i.b]))
		for p in ps:
			if p.checkClosed(lines) == False:
				ps.remove(p)
		for p in ps:
			p.removeDupVertex()
		nix = []
		for i in range(0,len(ps)-1):
			for j in range(0,len(ps)):
				if i == j:
					pass
				elif ps[i].eq(ps[j]):
					nix.append(j)
		for n in nix:
			ps.remove(ps[j])
		return ps
