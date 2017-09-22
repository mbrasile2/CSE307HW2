
tokenList = []
vessels = []
people = 0
horizon = 0

class Vessel:
	def __init__(self, vesselNum):
		self.vesselNum = vesselNum
		self.isSource = False

def main():
	# Read from the file line by line
	r = open("inputFilePour.txt", "r")

	for line in r:
		line = line.replace("(", ",")
		line  = line.replace(")", ",")
		line  = line.replace(" ", '')
		line = line.split(",")
		# now check the tokens
		tokenList.append(line)
	r.close()
	parseTokens()




def parseTokens():
	print(tokenList)
	for tokens in tokenList:
		if (tokens[0] == "vessels" and tokens[1].isdigit()):
			for n in range(0, int(tokens[1])):
				vessel = Vessel(n+1)
				vessel.filled = 0
				vessels.append(vessel)

		elif (tokens[0] == "source" and tokens[1].isdigit()):
			for vessel in vessels:
				if (vessel.vesselNum == int(tokens[1])):
					vessel.isSource = True;
					break

		elif (tokens[0] == "people" and tokens[1].isdigit()):
			people = int(tokens[1])

		elif (tokens[0] == "capacity" and tokens[1].isdigit() and tokens[2].isdigit()):
			for vessel in vessels:
				if (vessel.vesselNum == int(tokens[1])):
					vessel.capacity = int(tokens[2])
					break

		elif (tokens[0] == "horizon" and tokens[1].isdigit()):
			horizon = int(tokens[1])

	for vessel in vessels:
		if (vessel.isSource == True):
			vessel.filled = vessel.capacity


	for vessel in vessels:
		print(str(vessel.vesselNum) + " " + str(vessel.isSource) + " " + str(vessel.capacity) + " " + str(vessel.filled))


main()