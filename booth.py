# Place variables and lists here
tokenList = []
global room
room = []
booths = []
targetCoord = []

class Booth:
	def __init__(self, isTarget, boothNum, dimensions):
		self.isTarget = isTarget
		self.boothNum = boothNum
		self.dimensions = dimensions

	def printInfo(self):
		print("isTarget: " + str(self.isTarget) + "\nboothNum: " + str(self.boothNum) + "\ndimensions: " + str(self.dimensions))

	def setIsTarget(self):
		self.isTarget = True

def main():
	# Read from the file line by line
	r = open("inputFileBooth.txt", "r")

	for line in r:
		line = line.replace("(", ",")
		line  = line.replace(")", ",")
		line  = line.replace(" ", '')
		line = line.split(",")
		#now check the tokens
		tokenList.append(line)
	r.close()
	parseTokens()

	for booth in booths:
		booth.printInfo()
	

def parseTokens():
	for tokens in tokenList:
		if (tokens[0] == "room" and tokens[1].isdigit() and tokens[2].isdigit()):
			room = [[0 for x in range(int(tokens[1]))] for y in range(int(tokens[2]))] 

		elif (tokens[0] == "booths" and tokens[1].isdigit()):
			boothCount = int(tokens[1])

		elif (tokens[0] == "dimension" and tokens[1].isdigit() and tokens[2].isdigit() and tokens[3].isdigit()):
			newBooth = Booth(False, int(tokens[1]), [int(tokens[2]), int(tokens[3])])
			booths.append(newBooth)

		elif (tokens[0] == "position" and tokens[1].isdigit() and tokens[2].isdigit() and tokens[3].isdigit()):
			print(tokens)
			placeBoothInRoom(room, int(tokens[1]), int(tokens[2]), int(tokens[3]))

		elif (tokens[0] == "target" and tokens[1].isdigit() and tokens[2].isdigit() and tokens[3].isdigit()):
			makeTarget(int(tokens[1]), int(tokens[2]), int(tokens[3]))
			print("target coordinates: " + str(targetCoord))

		
def makeTarget(boothNum, finalX, finalY):
	selectedBooth = []

	# Get the selected booth
	for booth in booths:
		if (getattr(booth,'boothNum') == boothNum):
			selectedBooth = booth
			break

	selectedBooth.isTarget = True
	targetCoord.append([finalX, finalY])

def placeBoothInRoom(room, boothNum, x, y):
	selectedBooth = []

	print("Booth number: " + str(boothNum) + " with coordinates of (" + str(x) +", " + str(y) + ")")
	for booth in booths:
		if (getattr(booth,'boothNum') == boothNum):
			selectedBooth = booth
			break

	for height in range(0, int(getattr(selectedBooth, 'dimensions')[0])):

		for width in range(0, int(getattr(selectedBooth, 'dimensions')[1])):
			print("Adding to [" + str(width+x) + "][" + str(height+y) + "]")

			room[y+width][height+x] = int(getattr(selectedBooth, 'boothNum'))

	print(room)


main()
