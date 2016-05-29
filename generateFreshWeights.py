import sys

def save_weights(path, actions, features, default):
		with open(path, 'w') as outputfile:
			for action in range(actions):
				for feature in range(features):
					outputfile.write(default)
					outputfile.write(' ')
				outputfile.write("\n")	
		print 'Weights saved with success'

def generateWeights():
	actions = int(sys.argv[1])
	features= int(sys.argv[2])

	if(len(sys.argv)>3):
		default=sys.argv[3]
	else:
		default="1.0"

	path="../../weights.txt"
	save_weights(path, actions, features, default)

if __name__ == "__main__":
    generateWeights()