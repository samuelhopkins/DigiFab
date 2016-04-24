import math

class Vertex:
	def __init__(self, x_coord, y_coord, z_coord):
		self.x = x_coord
		self.y = y_coord
		self.z = z_coord
	
	def show(self):
		print("%.2E %.2E %.2E") % (self.x, self.y, self.z)
	
	def scale(self, size):
		self.x = self.x * size
		self.y = self.y * size
		self.z = self.z * size

	def add(self, v):
		return Vertex(self.x + v.x,
					  self.y + v.y,
					  self.z + v.z)
	
	def add_2d(self,v):
		return Vertex(self.x + v.x, 
					  self.y + v.y,
					  self.z)
	
	@classmethod
	def approx(a,b,err):
		if math.abs(a.x - b.x) <= err:
			if math.abs(a.y-b.y) <= err:
				if math.abs(a.z-b.z) <= err:
					return True
		return False
	
	def approxLine(a,dist,err):
		if math.abs(sqrt(a.x^2 + a.y^2, a.z^2) - dist) <= err:
			return True
		return False
	
	def eq(self, v):
		if self.x == v.x:
			if self.y == v.y:
				if self.z == v.z:
					return True
		return False
