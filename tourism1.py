import sys
import itertools
tokenList = []
people = 0
location_number = 0
locations = []
preferences = 0
orders = {}
violations = -1


def main():
    global people, locations
    # Read from the file line by line
    r = open(sys.argv[1], "r")

    for line in r:
        line = line.replace("(", ",")
        line = line.replace(")", ",")
        line = line.replace(" ", '')
        line = line.split(",")
        # now check the tokens
        tokenList.append(line)
    r.close()
    parse_tokens()
    get_all_partial_orderings()

    # Iterate through all of the locations
    for location in locations:
        get_violations(location)

    if violations == -1:
        print("violations(0).")
    else:
        print("violations(" +str(violations)+").")


def parse_tokens():
    global tokenList, people, location_number, locations, preferences, orders
    for tokens in tokenList:
        if tokens[0] == "people" and tokens[1].isdigit():
            people = int(tokens[1])
            for i in range(people):
                orders[i + 1] = []
        elif tokens[0] == "locations" and tokens[1].isdigit():
            locations = [i+1 for i in range(int(tokens[1]))]
            locations = list(itertools.permutations(locations))
        elif tokens[0] == "preferences" and tokens[1].isdigit():
            preferences = int(tokens[1])
        elif tokens[0] == "order":
            orders[int(tokens[1])].append([int(tokens[2]), int(tokens[3])])


def get_all_partial_orderings():
    global orders, people

    for person in orders.items():
        orderings = person[1]
        order_size = len(orderings)

        for i in range(order_size - 1):
            for j in range(1, order_size):
                if i != j:
                    transitive_order = [orderings[i][0], orderings[j][1]]
                    # print(transitive_order)
                    person[1].append(transitive_order)


def get_violations(location):
    global orders, violations
    local_violate = 0

    for person in orders.items():
        # Get orderings from each person
        orderings = person[1]
        for order in orderings:
            for num in location:
                if num == order[0]:
                    break
                elif num == order[1]:
                    local_violate += 1
                    break
                else:
                    continue

    if local_violate < violations or violations == -1:
        violations = local_violate


main()