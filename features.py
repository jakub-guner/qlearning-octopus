from math import acos
from numpy import var

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
		features.append(self.angleVar(state))
		return features

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

	"""Wariancja katow pomiedzy kolejnymi czlonami ramienia"""
	"""Im mniejsza tym bardziej jednolita krzywizna"""
	def angleVar(self, state):
		x1=0
		y1=0
		offsetLower=42
		totLen=0.0
		angles=[]
		for part in range(9):
			x2=state[offsetLower+part*4]
			y2=state[offsetLower+part*4+1]

			x3=state[offsetLower+(part+1)*4]
			y3=state[offsetLower+(part+1)*4+1]

			dotProduct=(x2-x1)*(x3-x2)+(y2-y1)*(y3-y2)
			length1=self.distanceBetweenPoints(x1, y1, x2, y2)
			length2=self.distanceBetweenPoints(x2, y2, x3, y3)
			# print dotProduct
			# print length1*length2
			cosinus=dotProduct/(length1*length2)
			# print cosinus
			angles.append(acos(cosinus-0.01))
			x1=x2
			y1=y2

		return var(angles)

	def doping(self, oldState, newState):
		return (self.dist(oldState)-self.dist(newState))
