from math import acos

class Features:
	def __init__(self):
		self.__food = [9,-1]
		self.__foodLength=self.distanceBetweenPoints(0, 0, self.__food[0], self.__food[1])
		pass

	def distanceBetweenPoints(self, x1, y1, x2, y2):
		d=(x1-x2)**2+(y1-y2)**2
		d=d**(0.5)
		return d

	def getFeatures(self, state, action):
		features = []
		features.append(self.dist(state))
		features.append(self.distmid(state))
		features.append(self.totalLength(state))
		features.append(self.angleDelta(state))
		return features

	# def dist(self, state):
	# 	x = state[38]
	# 	y = state[39]
	# 	dist = (x-self.__food[0])**2+(y-self.__food[1])**2
	# 	dist = dist ** (0.5)
	# 	return dist

	# def distmid(self, state):
	# 	x = state[18]
	# 	y = state[19]
	# 	dist = (x-self.__food[0])**2+(y-self.__food[1])**2
	# 	dist = dist ** (0.5)
	# 	return dist

	"""Odleglosc koncowki od kropki """
	def dist(self, state):
		x = state[38]
		y = state[39]
		return self.distanceBetweenPoints(x, y, self.__food[0], self.__food[1])

	"""Odleglosc punktu w polowie ramienia od kropki """
	def distmid(self, state):
		x = state[18]
		y = state[19]
		return self.distanceBetweenPoints(x, y, self.__food[0], self.__food[1])

	"""Calkowita dlugosc ramienia liczona po dolnej krawedzi """
	def totalLength(self, state):
		x1=0
		y1=0
		offsetLower=42
		totLen=0.0
		for part in range(10):
			x2=state[offsetLower+part*4]
			y2=state[offsetLower+part*4+1]
			totLen+=self.distanceBetweenPoints(x1, y1, x2, y2)
			
			x1=x2
			y1=y2
		return totLen

	""" Kat pomiedzy wektorem koncowki (dolna krawedz) a wektorem kropki"""
	def angleDelta(self, state):
		xEnd = state[78]
		yEnd = state[79]
		dotProduct=xEnd*self.__food[0]+yEnd*self.__food[1]
		endLength=self.distanceBetweenPoints(0,0, xEnd, yEnd)
		cosinus=dotProduct/(endLength*self.__foodLength)
		return acos(cosinus)

	def doping(self, oldState, newState):
		return (self.dist(oldState)-self.dist(newState))/5
