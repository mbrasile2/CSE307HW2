import sys
import copy
token_list = []
vessels = []
people = 0
horizon = 0
states = {}
queue = []
total_amount = 0
capacities = []


class Vessel:
    def __init__(self, vessel_num):
        self.vessel_num = vessel_num
        self.is_source = False


def main():
    global vessels, queue, horizon
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

    while queue:
        vessels = queue.pop(0)
        trace_num = get_trace(vessels)

        if check_if_split():
            print("split(yes).")
            break
        elif trace_num > horizon:
            print("split(no).")
            break

        explore()

        if not queue:
            print("split(no).")


def parse_tokens():
    global vessels, people, horizon, total_amount, capacities

    # print(token_list)
    for tokens in token_list:
        if tokens[0] == "vessels" and tokens[1].isdigit():
            for n in range(0, int(tokens[1])):
                vessel = Vessel(n+1)
                vessel.filled = 0
                vessels.append(vessel)

        elif tokens[0] == "source" and tokens[1].isdigit():
            for vessel in vessels:
                if vessel.vessel_num == int(tokens[1]):
                    vessel.is_source = True
                    break

        elif tokens[0] == "people" and tokens[1].isdigit():
            people = int(tokens[1])

        elif tokens[0] == "capacity" and tokens[1].isdigit() and tokens[2].isdigit():
            for vessel in vessels:
                if vessel.vessel_num == int(tokens[1]):
                    vessel.capacity = int(tokens[2])
                    break

        elif tokens[0] == "horizon" and tokens[1].isdigit():
            horizon = int(tokens[1])

    for vessel in vessels:
        capacities.append(vessel.capacity)
        if vessel.is_source:
            vessel.filled = vessel.capacity
            total_amount = vessel.capacity

    vessels = tuplify(vessels)
    propose(vessels, 0)

    capacities = tuple(capacities)


def tuplify(state):
    tuple_vessels = []
    for vessel in state:
        tuple_vessels.append(vessel.filled)

    return tuple(tuple_vessels)


def propose(current, prev):
    global states, queue

    if current not in states:
        states[current] = prev
        queue.append(current)
        return True

    return False


def explore():
    global vessels, capacities
    new_vessels = list(copy.deepcopy(vessels))

    for pour_give, v1 in enumerate(new_vessels):
        new_vessels = list(copy.deepcopy(vessels))
        if new_vessels[pour_give] != 0:
            for pour_rec, v2 in enumerate(new_vessels):
                new_vessels = list(copy.deepcopy(vessels))
                if v1 != v2 and new_vessels[pour_rec] != capacities[pour_rec]:
                    # pour the current vessel's contents into the proposed vessel
                    if (new_vessels[pour_rec] + new_vessels[pour_give]) <= capacities[pour_rec]:
                        new_vessels[pour_rec] += new_vessels[pour_give]
                        new_vessels[pour_give] = 0
                    else:
                        for i in range(new_vessels[pour_give]):
                            i += 1
                            if new_vessels[pour_rec] + i == capacities[pour_rec]:
                                break
                        new_vessels[pour_give] = new_vessels[pour_give] - i
                        new_vessels[pour_rec] = new_vessels[pour_rec] + i

                    propose(tuple(new_vessels), vessels)


# Uses best fit heuristic to check if the vessels can be split evenly amongst people
def check_if_split():
    global vessels, total_amount, people, capacities
    filled_sort = sorted(vessels, reverse=True)

    amount_per_person = total_amount / people
    person = []
    person.insert(0, 0)

    # iterate through the vessels
    for capacity in filled_sort:
        # If the vessel has more than the amount per person, return false
        if capacity > amount_per_person:
            return False
        # if the vessel is less than amount, check if it can be added to the amount
        elif capacity <= amount_per_person:
            # Check if added amount can fit into the current person
            if (capacity + person[0]) <= amount_per_person:
                person[0] = capacity + person[0]
                if (capacity + person[0]) == amount_per_person:
                    person.insert(0, 0)
                continue
            else:
                person.insert(0, capacity)

    if len(person) == people and sum(person) == total_amount:
        return True
    else:
        return False


def get_trace(current):
    global states, step
    previous_state = states[current]

    if previous_state == 0:
        return 0
    else:
        step = get_trace(previous_state) + 1
    return step


main()
