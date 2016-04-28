from vertex import Vertex
class Line:
	def __init__(self,a,b):
		self.a = a
		self.b = b
		
	def dist(self):
		return sqrt(((self.b.x-self.a.x)^2) + (self.b.y-self.a.y)^2 + (self.b.z-self.a.z)^2)
	
	def tuple(self):
		return (self.a.tuple(), self.b.tuple())
		
	@classmethod
	def dot(a,b):
		return a.x*b.x + a.y*b.y + a.z*b.z 
	
	@classmethod
	def angle(a,b):
		return arcos((Line.dot(a,b))/(a.dist()*b.dist()))
	
	def show(self):
		self.a.show(), self.b.show()

	def eq(self,j):
		if (self.a.eq(j.a) and self.b.eq(j.b)
			or self.a.eq(j.b) and self.b.eq(j.a)):
			return True
		return False
