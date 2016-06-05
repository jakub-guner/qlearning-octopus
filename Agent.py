import random
import features
from array import array

"""1 decyzja co X krokow => zsumowane nagrody """
"""feature - czas ??? """

class Agent:
	#name should contain only letters, digits, and underscores (not enforced by environment)
	__name = 'JT_JG'
	
	"""Initialize agent assuming floating point state and action"""
	def __init__(self, stateDim, actionDim, agentParams):
		
		self.features = features.Features()
		self.path = agentParams[0]
		
		self.__stateDim = stateDim
		self.__actionDim = actionDim 
		self.__action = array('d',[0 for x in range(actionDim)])
		"""akcje -1 - nic 0 - zgiecie przeciwnie z ruchem, 1 - wydluzenie, 2- zgodnie z ruchem"""
		meta_act = [-1,0,1, 2]
		self.__meta_action=[-1,0,1, 2]
		self.__weights = []
		random.seed()
		
		self.__load_weights(self.path)	

		self.alpha = float(0.005)
		self.epsilon = float(0.05)
		self.discount = float(1.00)
		self.number = 0

		self.prev_state = []
		self.prev_action = []
		self.prev_action_meta = []

	def start(self, state):
		meta_action = self.__find_best_action(state)
		action = self.__meta_to_action(meta_action)
		self.prev_state = state
		self.prev_action = action
		self.prev_action_meta = meta_action	
		self.number=self.number+1
		return action
	
	def step(self, reward, state):
		dop=self.features.doping(self.prev_state, state)
		if(dop>0 and reward==-0.01):
			reward/=2
		if(dop<0 and reward==-0.01):
				reward*=2

		for part in range(10):
			maxQ = float("-inf")
			for act in self.__meta_action:
				q = self.get_Q_value(state, act, part)
				maxQ = max(maxQ, q)

			action = []

			self.update(maxQ, reward, state, action, part)
			# self.normalize()

		#Exploitation vs exploraion
		if(random.randint(0, 10)<9):
			meta_action = self.__find_best_action(state)
		else:
			meta_action = self.__randomAction()

		action = self.__meta_to_action(meta_action)
		self.prev_state = state
		self.prev_action = action
		self.prev_action_meta = meta_action
		self.number=1+self.number
		
		if reward==10:
			print 'Koniec - touch!', reward-self.number*0.01
			self.number=0
			self.__save_weights(self.path)
		if self.number==998:
			print 'Koniec - timeout!', reward-self.number*0.01
			self.number=0
			self.__save_weights(self.path)	
		
		return action

	def __find_best_action(self, state):
		best_meta_action = []
		for j in range(10):		
			best_action = []
			best = float("-inf")
			for i in self.__meta_action:
				temp = self.get_Q_value(state, i, j)
				if temp>best:
					best=temp
					best_action = [i]
				elif temp==best :
					best_action.append(i)
			if (len(best_action) >= 1):
				best = random.randint(0, len(best_action)-1)
				best_meta_action.append(best_action[best])
			else:
				best_meta_action.append(-1)
		return best_meta_action

	def __randomAction(self):
		best_meta_action = []
		for i in range(10):
			best_meta_action.append(random.randint(-1, 2))
 		return best_meta_action

	def get_Q_value(self, state, action, part):
		features = self.features.getFeatures(state, action, part)
		indeks_wag_akcji=part*4 + action + 1
		sum=0
		for i in range(len(self.__weights[indeks_wag_akcji])):
			sum=sum+self.__weights[indeks_wag_akcji][i]*features[i]

		return	sum
	
	def __meta_to_action(self, c):
		action = array('d',[0 for x in range(self.__actionDim)])
		
		for j in range (len(c)):	
			if c[j]>-1:				
				for i in range((j*self.__actionDim/len(c)), (j+1)*(self.__actionDim/len(c))):
					if (i%3 == (c[j])):
						action[i] = 1
					else:
						action[i] = 0
		return action

	def normalize(self):
		suma = 0
		for i in range(len(self.__weights)):
			sumtemp=0
			for j in self.__weights[i]:
				sumtemp=sumtemp+abs(j)
			suma = suma+sumtemp
		for i in range(len(self.__weights)):
			self.__weights[i][:] = [x / suma for x in self.__weights[i]]

	"""minQ - best w biezacym stanie """
	"""reward - nagroda za dojscie do biezacego stanu"""
	"""state - biezacy stan """
	"""action - zawsze puste """
	def update(self, maxQ, reward, state, action, part):
		features = self.features.getFeatures(state, action, part)
		indeks_wag_akcji=part*4 + (self.prev_action_meta[part]+1)
		# Regularyzacja
		row=[abs(w) for w in self.__weights[indeks_wag_akcji]]
		bias=sum(row)
		print maxQ
		for featurenr in range(len(features)):  
			difference = (reward + self.discount * maxQ) - self.get_Q_value(self.prev_state, self.prev_action_meta[part], part)
			# if(difference<0):
			# 	difference-=bias
			# else:
			# 	difference+=bias
			#new_value = max(self.__weights[indeks_wag_akcji][featurenr] + self.alpha * difference * features[featurenr], 0)
			new_value = self.__weights[indeks_wag_akcji][featurenr] + self.alpha * difference * features[featurenr]
			self.__weights[indeks_wag_akcji][featurenr] = new_value

	def __save_weights(self, path):
		with open(path, 'w') as outputfile:
			for x in self.__weights:
				for a in x:
					outputfile.write(str(a))
					outputfile.write(' ')
				outputfile.write("\n")	
		# print 'Weights saved with success'	

	def __load_weights(self, path):
		z=0
		with open(path) as inputfile:
			for line in inputfile:
				self.__weights.append([])
				for x in line.split():
					self.__weights[z].append(float(x)) 
					
				z=z+1
		print 'Weights loaded with success'
		
	def end(self, reward):
		print 'Koniec!'
		self.__save_weights(self.path)
	
	def cleanup(self):
		self.__action = array('d',[0 for x in range(self.__actionDim)]) 
	
	def getName(self):
		return self.__name
