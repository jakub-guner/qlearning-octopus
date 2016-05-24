import random 
from array import array
import math

class Agent:
    
    #name should contain only letters, digits, and underscores (not enforced by environment)
    __name = 'JT_JG'
    
    def __init__(self, stateDim, actionDim, agentParams):
    	self.path = agentParams[0]
        "Initialize agent assuming floating point state and action"
        self.__stateDim = stateDim
    	print self.__stateDim #82
        self.__actionDim = actionDim 
        self.__action = array('d',[0 for x in range(actionDim)]) #30
    	self.__weights = array('d',[0 for x in range(3)]) 
        #we ignore agentParams because our agent does not need it.
        #agentParams could be a parameter file needed by the agent.
        random.seed()

    	self.__load_weights(self.path)	

    #	self.__weights[1]=self.__weights[1]-1

    #	self.__save_weights(self.path)
    	#[0,0],[0,1],[1,0], [1,1], [-1,1]
    	self.prev_state = []
    	self.prev_action = []

        self.steps_done=0    

    def __update_weights(self):
    	pass
	
    #TODO
    def __get_legal_actions(self):
	   pass
	
    #TODO
    def __cal_Q_value(self, action):
	   pass
	#TODO

    def __save_weights(self, path):
    	with open(path+'/weights.txt', 'w') as outputfile:
    		for x in self.__weights:
    			outputfile.write(str(x))
    			outputfile.write(' ')
    	print 'weights saved with success'	

    def __load_weights(self, path):
    	z=0
    	with open(path+'/weights.txt') as inputfile:
    		for line in inputfile:
    			for x in line.split():
    				self.__weights[z]= float(x) 
    				z=z+1
    	print 'weights loaded with success'

    def __randomAction(self):
        for i in range(self.__actionDim):
            self.__action[i] = random.random() 

    def _maxLenthAction(self):
        for i in range(self.__actionDim):
            self.__action[i] = 1 if i%3==1 else 0

    
    def __curlAction(self):
        for i in range(self.__actionDim):
            if (i%3 == 2):
                self.__action[i] = 1
            else:
                self.__action[i] = 0

            
    def start(self, state):
        "Given starting state, agent returns first action"
        # self.__action=
        print "Init state:"
        print state
        # self.__randomAction()
        self._maxLenthAction()
        self._displayLenghths(state)





        # print "Akcja"
        # print self.__action
        return self.__action

    def _displayLenghths(self, state):
        ls=self.getArmLengths(state)
        for i in range(10):
            print "Arm "+str(i)+": "+str(ls[i])
        print "Sum: ", sum(ls[0:10])
        print "Estimate", ls[10]

    def getArmLengths(self, state):
        offsetUpper=2
        offsetLower=42
        lengths=[]
        x1=0
        y1=0
        x2=0
        y2=0
        for arm in range(10):
            x2=state[offsetLower+arm*4]
            y2=state[offsetLower+arm*4+1]
            l=math.sqrt((x2-x1)**2+(y2-y1)**2)
            lengths.append(l)
            # print x1, y1, x2, y2
            x1=x2
            y1=y2
            

            # x1=state[offsetUpper+arm*4]
            # y1=state[offsetUpper+arm*4+1]

            # x2=state[offsetLower+arm*4]
            # y2=state[offsetLower+arm*4+1]

            # l=math.sqrt((x2-x1)**2+(y2-y1)**2)
            # lengths.append(l)

            # if(arm==0):
            # print x1, y1, x2, y2
        totalEst=l=math.sqrt((x2)**2+(y2)**2)
        lengths.append(totalEst)
        return lengths


    "Given current reward and state, agent returns next action"
    def step(self, reward, state):     
        self.steps_done+=1

        if(self.steps_done<300 and self.steps_done%30==0):
            print "Steps", self.steps_done
            self._displayLenghths(state)
	
        
        self._maxLenthAction()
#        self.__curlAction()
	
        return self.__action
    
    def end(self, reward):
        pass
    
    #Tylko dla 'Communication error'
    def cleanup(self):
        self.__action = array('d',[0 for x in range(actionDim)]) 
    
    def getName(self):
        return self.__name
    
            
