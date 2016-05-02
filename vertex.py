import math

class Vertex:
	def __init__(self, x_coord, y_coord, z_coord):
		self.x = x_coord
		self.y = y_coord
		self.z = z_coord
	
	def show(self):
		print("%.2E %.2E %.2E") % (self.x, self.y, self.z)
	
	def tuple(self):
		return (self.x, self.y, self.z)
		
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
		if abs(a.x - b.x) <= err:
			if abs(a.y-b.y) <= err:
				if abs(a.z-b.z) <= err:
					return True
		return False
	
	def approxLine(a,dist,err):
		if math.abs(sqrt(a.x^2 + a.y^2, a.z^2) - dist) <= err:
			return True
		return False
	
	def eq(self, v):
		threshold = .00000001
		if abs(self.x-v.x) < threshold:
			if abs(self.y-v.y) < threshold:
				if abs(self.z-v.z) < threshold:
					return True
		return False
	
	def dot(self, v):
		return self.x(v.x + self.y*v.y + self.z*float(v.z))
		return self.x(v.x + self.y*v.y + self.z*float(v.z))
	
	def mag(self):
		return sqrt(self.x^2 + self.y^2 + float(self.z^2))
