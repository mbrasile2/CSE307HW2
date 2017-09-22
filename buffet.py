
tokenList = []
demand = {}
dishes = []
table_width = 0
global separation

class Dish:
	def __init__(self, dishNum):
		self.dishNum = dishNum



def main():
	# Read from the file line by line
	r = open("inputFileBuffet.txt", "r")

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
		if (tokens[0] == "dishes" and tokens[1].isdigit()):
			for n in range(0, int(tokens[1])):
				dish = Dish(n+1)
				dishes.append(dish)

		elif (tokens[0] == "separation" and tokens[1].isdigit()):
			seperation = int(tokens[1])

		elif (tokens[0] == "hot" and tokens[1].isdigit()):
			for dish in dishes:
				if ((int(tokens[1])) >= dish.dishNum):
					dish.isHot = True
				else:
					dish.isHot = False

		elif (tokens[0] == "table_width" and tokens[1].isdigit()):
			table_width = int(tokens[1])

		elif (tokens[0] == "dish_width" and tokens[1].isdigit() and tokens[2].isdigit()):
			for dish in dishes:
				if (dish.dishNum == int(tokens[1])):
					dish.width = int(tokens[2])
					break

		elif (tokens[0] == "demand" and tokens[1].isdigit() and tokens[2].isdigit()):
			for dish in dishes:
				if (dish.dishNum == int(tokens[1])):
					demand[dish] = int(tokens[2])

	# print(dishes)
	# print(demand)

	for dish in dishes:
		print(str(dish.dishNum) + " " + str(dish.isHot) +" " + str(dish.width))

main()