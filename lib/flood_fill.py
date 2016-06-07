def count_room(theMap, start_cell):
    theMap_list = [list(row) for row in theMap]
    x = start_cell[0]
    y = start_cell[1]
    count = 0
    theStack = [(x, y)]
    while len(theStack) > 0:
        x, y = theStack.pop()
        if not 0 <= x < len(theMap_list) or not 0 <= y < len(theMap_list[0]):
            continue
        if theMap_list[x][y] != '.':
            continue
        theMap_list[x][y] = '@'
        count = count + 1
        theStack.append((x + 1, y))  # right
        theStack.append((x - 1, y))  # left
        theStack.append((x, y + 1))  # down
        theStack.append((x, y - 1))  # up

    return count