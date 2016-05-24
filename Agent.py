import random 
from array import array

class Agent:
    "A template agent acting randomly"
    
    #name should contain only letters, digits, and underscores (not enforced by environment)
    __name = 'Misiu'
    
    def __init__(self, stateDim, actionDim, agentParams):
	self.path = agentParams[0]
        "Initialize agent assuming floating point state and action"
        self.__stateDim = stateDim
        self.__actionDim = actionDim 
        self.__action = array('d',[0 for x in range(actionDim)])
	self.__meta_action = array('h',[x for x in range(-1,3)])
	print self.__meta_action
	self.__wages = []

	self.__food = [9,-1]
        #we ignore agentParams because our agent does not need it.
        #agentParams could be a parameter file needed by the agent.
        random.seed()
	
	self.__load_wages(self.path)	
	print self.__wages
#	self.__wages[1]=self.__wages[1]-1

#	self.__save_wages(self.path)

	self.alpha = float(0.1)
        self.epsilon = float(0.05)
        self.discount = float(0.8)
	self.number = 0

	self.prev_state = []
	self.prev_action = []
	self.prev_action_meta = []


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
    
	#akcje -1 - nic 0 - zgiecie przeciwnie z ruchem, 1 - wydluzenie, 2- zgodnie z ruchem


    def __find_best_action(self, state):
	best_action = []
	best = 1000000 
	for i in self.__meta_action:
		temp = self.get_Q_value(state, i)
		if temp<best:
			best=temp
			best_action = [i]
		elif temp==best :
			best_action.append(i)
	if (len(best_action) >= 1):
		best = random.randint(0, len(best_action)-1)
		#print 'Best actions: ', best_action, ' and picked: ',  best_action[best]
		return best_action[best]
	else:
		#print 'Best action not found'
		return -1

    def get_Q_value(self, state, action):
	sum=self.__wages[action+1][0]*self.dist(state)+self.__wages[action+1][1]*self.distmid(state)
	return	sum

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
				
