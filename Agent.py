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
				
			z=z+1
	print 'Wages loaded with success'

    def __randomAction(self):
	return random.randint(-1, 3)
  
    
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
            
    def start(self, state):
	meta_action = self.__find_best_action(state)
        action = self.__curlAction(meta_action)
	self.prev_state = state
	self.prev_action = action
	self.prev_action_meta = meta_action	
	#print self.__wages
	#print 'Best action: ', meta_action
	self.number=self.number+1
        return action
    
    def step(self, reward, state):	
	#self.__update_wages(self, self.prev_action_meta, ):			
        #"Given current reward and state, agent returns next action"
	minQ = float("-inf")
        for act in self.__meta_action:
            q = self.get_Q_value(state, act)
            minQ = min(minQ, q)

        if minQ == float("-inf"):
            minQ = 0	
	
	reward2 = 0.01

	difference = ( -1*reward + self.discount * minQ) + self.get_Q_value(self.prev_state,self.prev_action_meta)   
	#difference = (reward + self.discount * self.get_Q_value(state,self.prev_action_meta) ) + self.get_Q_value(self.prev_state,self.prev_action_meta)    
        self.__wages[self.prev_action_meta+1][0] = max(self.__wages[self.prev_action_meta][0] + self.alpha * difference * self.dist(state),0)
	self.__wages[self.prev_action_meta+1][1] = max(self.__wages[self.prev_action_meta][1] + self.alpha * difference * self.distmid(state),0)
	self.normalize()
	#print self.__wages
	meta_action = self.__find_best_action(state)
	
	#print meta_action, reward
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
    	
    def end(self, reward):
	print 'Koniec!'
        self.__save_wages(self.path)
    
    def cleanup(self):
	self.__action = array('d',[0 for x in range(self.__actionDim)]) 
    
    def getName(self):
        return self.__name
    
          
