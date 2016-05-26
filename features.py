class Features:
	def __init__(self):
		self.__food = [9,-1]
		pass

	def getFeatures(self, state, action):
		features = []
		features.append(self.dist(state))
		features.append(self.distmid(state))
		return features

	def dist(self, state):
		x = state[38]
		y = state[39]
		dist = (x-self.__food[0])**2+(y-self.__food[1])**2
		dist = dist ** (0.5)
		return dist

	def distmid(self, state):
		x = state[18]
		y = state[19]
		dist = (x-self.__food[0])**2+(y-self.__food[1])**2
		dist = dist ** (0.5)
		return dist
