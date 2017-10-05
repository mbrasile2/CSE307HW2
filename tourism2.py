import sys
import itertools
token_list = []
location_size = 0
people_size = 0
locations = []
people = {}
preferences = 0


def main():
    global token_list, locations, people, people_size
    satisfactions = []
    # Read from the file line by line
    r = open(sys.argv[1], "r")

    for line in r:
        line = line.replace("(", ",")
        line = line.replace(")", ",")
        line = line.replace(" ", '')
        line = line.split(",")
        # now check the tokens
        token_list.append(line)
    r.close()
    parse_tokens()
    locations = list(itertools.permutations(locations))
    for location_subset in locations:
        satisfactions.append(get_optimal_satisfaction(get_location_sequence(location_subset)))

    print("satisfaction("+str(max(satisfactions))+").")


def parse_tokens():
    global token_list, location_size, people_size, locations, people, preferences
    for tokens in token_list:
        if tokens[0] == "people" and tokens[1].isdigit():
            people_size = int(tokens[1])
            for i in range(people_size):
                people[i+1] = []
        elif tokens[0] == "locations" and tokens[1].isdigit():
            location_size = int(tokens[1])
        elif tokens[0] == "preferences" and tokens[1].isdigit():
            preferences = int(tokens[1])
        elif tokens[0] == "location":
            locations.append((int(tokens[1]), int(tokens[2]), int(tokens[3]), int(tokens[4])))
        elif tokens[0] == "prefer":
            people[int(tokens[1])].append(int(tokens[2]))


def get_location_sequence(locations):
    time = 0
    return_set = []
    # Iterate through the locations
    for location in locations:
        if location[2] > time:
            time = location[2] + location[1]
            return_set.append(location[0])
        elif (time + location[1]) <= location[3]:
            time += location[1]
            return_set.append(location[0])
    return return_set


def get_optimal_satisfaction(location_set):
    global people
    opt_sat = 0
    ratio_sat = float(1)

    for person in people.items():
        temp_sat = 0
        for location in person[1]:
            if location in location_set:
                temp_sat += 1

        if (temp_sat / float(len(person[1]))) <= ratio_sat or temp_sat == 0:
            ratio_sat = temp_sat / float(len(person[1]))
            opt_sat = temp_sat

    return opt_sat


main()