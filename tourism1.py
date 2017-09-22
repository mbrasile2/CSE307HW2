tokenList = []
people = 0
location_number = 0
locations = []



def main():
	# Read from the file line by line
	r = open("inputFileTourism1.txt", "r")

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
	for tokens in tokenList:
		if (tokens[0] == "people" and tokens[1].isdigit()):


main()