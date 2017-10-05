import copy
import sys
# Place variables and lists here
tokenList = []
room = []
booths = []
states = {}
targetCoord = []
queue = []
targetHit = False
step = 0
horizon = -1
og_room = []
booths_back = False
old_booths = []
booth_count = 0


class Booth:
    def __init__(self, is_target, booth_num, dimensions):
        self.is_target = is_target
        self.booth_num = booth_num
        self.dimensions = dimensions
        self.current_coordinates = []

    def print_info(self):
        print("is_target: " + str(self.is_target) + "\nbooth_num: " + str(self.booth_num) + "\ndimensions: " + str(
            self.dimensions))

    def setis_target(self):
        self.is_target = True


def main():
    global booths, room, targetHit, states, booths, step, booths_back
    # steps_to_target = 0
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
    while queue:
        room = queue.pop(0)
        update_booth_coord()
        if hit_target() and not targetHit:
            targetHit = True
            get_trace(room)
            if step <= horizon:
                print("moves(" + str(step) + ").")
                break
            else:
                break
        explore()


def parse_tokens():
    global room, booth_count, booths, targetCoord, queue, horizon, og_room

    for tokens in tokenList:
        if tokens[0] == "room" and tokens[1].isdigit() and tokens[2].isdigit():
            room = [[0 for x in range(int(tokens[1]))] for y in range(int(tokens[2]))]

        elif tokens[0] == "booths" and tokens[1].isdigit():
            booth_count = int(tokens[1])

        elif tokens[0] == "dimension" and tokens[1].isdigit() and tokens[2].isdigit() and tokens[3].isdigit():
            new_booth = Booth(False, int(tokens[1]), [int(tokens[2]), int(tokens[3])])
            booths.append(new_booth)

        elif tokens[0] == "position" and tokens[1].isdigit() and tokens[2].isdigit() and tokens[3].isdigit():
            place_booth_in_room(int(tokens[1]), int(tokens[2]), int(tokens[3]))

        elif tokens[0] == "target" and tokens[1].isdigit() and tokens[2].isdigit() and tokens[3].isdigit():
            make_target(int(tokens[1]), int(tokens[3]), int(tokens[2]))

        elif tokens[0] == "horizon" and tokens[1].isdigit():
            horizon = int(tokens[1])

    # add the booths to the original booth.py squad
    for selected_booth in booths:
        old_booths.append(copy.deepcopy(selected_booth))

    # Make the room a tuple...
    tuple_room = tuplify(room)
    # add it to the queue and states dict
    og_room = tuple_room
    propose(tuple_room, 0)


def tuplify(state):
    # Make the room a tuple...
    tuple_room = []
    for row in state:
        tuple_room.append(tuple(row))
    tuple_room = tuple(tuple_room)
    return tuple_room


def propose(current, prev):
    global states, queue, room
    if current not in states:
        states[current] = prev
        queue.append(current)
        return True

    return False


def make_target(booth_num, final_x, final_y):
    global targetCoord
    selected_booth = []

    # Get the selected booth.py
    for booth in booths:
        if getattr(booth, 'booth_num') == booth_num:
            selected_booth = booth
            break

    selected_booth.is_target = True
    targetCoord.append(final_x)
    targetCoord.append(final_y)


def place_booth_in_room(booth_num, x, y):
    global room
    selected_booth = []

    for booth in booths:
        if getattr(booth, 'booth_num') == booth_num:
            selected_booth = booth
            break

    for height in range(0, int(getattr(selected_booth, 'dimensions')[0])):
        for width in range(0, int(getattr(selected_booth, 'dimensions')[1])):
            selected_booth.current_coordinates.append([y + width, x + height])
            room[y + width][height + x] = int(getattr(selected_booth, 'booth_num'))


def move_to(booth, direction):
    global booths, room, states, queue
    index = 0
    booth_coord = []

    for coord in booth.current_coordinates:
        if direction == "u":
            booth_coord.append([coord[0] + 1, coord[1]])

        elif direction == "d":
            booth_coord.append([coord[0] - 1, coord[1]])

        elif direction == "r":
            booth_coord.append([coord[0], coord[1] + 1])

        elif direction == "l":
            booth_coord.append([coord[0], coord[1] - 1])

        index += 1
    # Build a new room state by filling in 0's first

    new_room_state = [[0 for x in range(len(room))] for y in range(len(room[0]))]

    # Then populate it with the new booth.py coordinates

    for b in booths:
        if b.booth_num == booth.booth_num:
            for coord in booth_coord:
                new_room_state[coord[0]][coord[1]] = booth.booth_num
        else:
            # Populate the other booths that didnt move
            for coord in b.current_coordinates:
                new_room_state[coord[0]][coord[1]] = b.booth_num

    # Save the old room state and the current room state in the states Dictionary
    # Make the room a tuple...
    tuple_room = []
    for row in new_room_state:
        tuple_room.append(tuple(row))
    tuple_room = tuple(tuple_room)

    # Propose the new configuration to the states map, but only if the state doesnt exist yet
    return propose(tuple_room, room)


def can_move_to(booth, direction):
    global booths, room
    potential_coord = []

    # Put the new potential coordinates in potential_coord
    if direction == "u":
        for coordinate in booth.current_coordinates:
            potential_coord.append([coordinate[0] + 1, coordinate[1]])

    elif direction == "d":
        for coordinate in booth.current_coordinates:
            potential_coord.append([coordinate[0] - 1, coordinate[1]])

    elif direction == "l":
        for coordinate in booth.current_coordinates:
            potential_coord.append([coordinate[0], coordinate[1] - 1])

    elif direction == "r":
        for coordinate in booth.current_coordinates:
            potential_coord.append([coordinate[0], coordinate[1] + 1])

    # Check if the booth.py can be moved there
    for p_coord in potential_coord:
        # check if its out of bounds
        if direction == "u" and p_coord[0] >= len(room):
            return False
        elif direction == "d" and p_coord[0] < 0:
            return False
        elif direction == "r" and p_coord[1] >= len(room[0]):
            return False
        elif direction == "l" and p_coord[1] < 0:
            return False

        # now check if it collides with another booth.py
        elif room[p_coord[0]][p_coord[1]] != 0 and room[p_coord[0]][p_coord[1]] != booth.booth_num:
            return False
        # Loop is done, it can be moved
    return True


def update_booth_coord():
    global room
    global booths
    for booth in booths:
        booth.current_coordinates.clear()

    for booth in booths:
        for i, row in enumerate(room):
            for j, val1 in enumerate(row):
                if val1 is not 0:
                    if booth.booth_num == val1:
                        booth.current_coordinates.append([i, j])
                if len(booth.current_coordinates) == (booth.dimensions[0] * booth.dimensions[1]):
                    break
                j += 1
            if len(booth.current_coordinates) == (booth.dimensions[0] * booth.dimensions[1]):
                break
            i += 1


def explore():
    global booths, queue, states, targetHit
    # iterates through the booths and checks if they can be moved
    for booth in booths:
        # Won't move the target booth.py if it was already solved
        if can_move_to(booth, "u"):
            move_to(booth, "u")
        if can_move_to(booth, "d"):
            move_to(booth, "d")
        if can_move_to(booth, "r"):
            move_to(booth, "r")
        if can_move_to(booth, "l"):
            move_to(booth, "l")


def hit_target():
    global booths, room, targetCoord

    right_booths = 0
    target_booth = []

    # Get the target booth.py
    for booth in booths:
        if booth.is_target is True:
            target_booth = booth
            break

    # Checks if any part of the booth.py is in the target coordinates
    if target_booth.current_coordinates[0] == targetCoord:
        # Hooray it is
        right_booths += 1

    for i, booth in enumerate(booths):
        if not booth.is_target and booth.current_coordinates == old_booths[i].current_coordinates:
            right_booths += 1

    return right_booths == len(booths)


def booths_hit():
    global og_room, room, booths, old_booths
    right_booths = 0

    for i, booth in enumerate(booths):
        if not booth.is_target and booth.current_coordinates == old_booths[i].current_coordinates:
            right_booths += 1

    return right_booths == len(booths)-1


def get_trace(current):
    global room, states, step
    previous_state = states[tuplify(current)]

    if previous_state == 0:
        return 0
    else:
        step = get_trace(previous_state) + 1
    return step


main()
