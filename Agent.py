import random
import features
from array import array

class Agent:
	"A template agent acting randomly"
	
	#name should contain only letters, digits, and underscores (not enforced by environment)
	__name = 'Misiu'
	
	def __init__(self, stateDim, actionDim, agentParams):
		self.features = features.Features()
		self.path = agentParams[0]
		"Initialize agent assuming floating point state and action"
		self.__stateDim = stateDim
		self.__actionDim = actionDim 
		self.__action = array('d',[0 for x in range(actionDim)])
		#akcje -1 - nic 0 - zgiecie przeciwnie z ruchem, 1 - wydluzenie, 2- zgodnie z ruchem
		self.__meta_action = array('h',[x for x in range(-1,3)])
		print self.__meta_action
		self.__wages = []
		random.seed()
		
		self.__load_wages(self.path)	

		self.alpha = float(0.1)
		self.epsilon = float(0.05)
		self.discount = float(0.8)
		self.number = 0

		self.prev_state = []
		self.prev_action = []
		self.prev_action_meta = []

	def start(self, state):
		meta_action = self.__find_best_action(state)
		action = self.__curlAction(meta_action)
		self.prev_state = state
		self.prev_action = action
		self.prev_action_meta = meta_action	
		self.number=self.number+1
		return action
	
	def step(self, reward, state):
		dop=self.features.doping(self.prev_state, state)
		minQ = float("+inf")
		for act in self.__meta_action:
			q = self.get_Q_value(state, act)
			minQ = min(minQ, q)

		if minQ == float("+inf"):
			minQ = 0	
		action = []
		# reward2 = 0.01
		self.update(minQ, reward+dop, state, action)
		self.normalize()


		#Exploitation vs exploraion
		if(random.randint(0, 10)<9):
			meta_action = self.__find_best_action(state)
		else:
			meta_action = self.__randomAction()

		action = self.__curlAction(meta_action)
		self.prev_state = state
		self.prev_action = action
		self.prev_action_meta = meta_action
		self.number=1+self.number
		
		if reward==10:
			print 'Koniec!', reward
			
			self.__save_wages(self.path)
		if self.number==998:
			print 'Koniec!', reward
			self.__save_wages(self.path)	
		
		return action

	def __find_best_action(self, state):
		best_action = []
		best = 1000000 
		for i in self.__meta_action:
			temp = self.get_Q_value(state, i)
			#print temp, i
			if temp<best:
				best=temp
				best_action = [i]
			elif temp==best :
				best_action.append(i)
		if (len(best_action) >= 1):
			best = random.randint(0, len(best_action)-1)
			return best_action[best]
		else:
			return -1

	def __randomAction(self):
 		return random.randint(-1, 2)

	def get_Q_value(self, state, action):
		features = self.features.getFeatures(state, action)
		sum=0
		for i in range(len(self.__wages[action+1])):
			sum=sum+self.__wages[action+1][i]*features[i]


		return	sum
	
	def __curlAction(self, c):
		action = array('d',[0 for x in range(self.__actionDim)])	
		if c>-1:				
			for i in range(self.__actionDim):
				if (i%3 == (c)):
					action[i] = 1
				else:
					action[i] = 0

		return action

	def normalize(self):
		suma=0
		for i in range(len(self.__wages)):
			suma = suma+sum(self.__wages[i])
		for i in range(len(self.__wages)):
			self.__wages[i][:] = [x / suma for x in self.__wages[i]]

	def update(self, minQ, reward, state, action):
		features = self.features.getFeatures(state, action)
		for featurenr in range(len(features)):  
			difference = (-1*reward + self.discount * minQ) - self.get_Q_value(self.prev_state,self.prev_action_meta)
			self.__wages[self.prev_action_meta+1][featurenr] = max(self.__wages[self.prev_action_meta][featurenr] + self.alpha * difference * features[featurenr],0)

	def __save_wages(self, path):
		with open(path, 'w') as outputfile:
			for x in self.__wages:
				for a in x:
					outputfile.write(str(a))
					outputfile.write(' ')
				outputfile.write("\n")	
		print 'Wages saved with success'	

	def __load_wages(self, path):
		z=0
		with open(path) as inputfile:
			for line in inputfile:
				self.__wages.append([])
				for x in line.split():
					self.__wages[z].append(float(x)) 
					
				z=z+1
		print 'Wages loaded with success'
		
	def end(self, reward):
		print 'Koniec!'
		self.__save_wages(self.path)
	
	def cleanup(self):
		self.__action = array('d',[0 for x in range(self.__actionDim)]) 
	
	def getName(self):
		return self.__name