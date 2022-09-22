import copy, random, sys, time

WIDTH = 50
HEIGHT = 50
ALIVE = "0"
DEAD = " "

idk = 0

nextCells = {}

for x in range(WIDTH):
    for y in range(HEIGHT):
        if random.randint(0, 2) == 1:
            nextCells[(x, y)] = ALIVE

        else:
            nextCells[(x, y)] = DEAD


while True:
    cells = copy.deepcopy(nextCells)

    if idk % 800 == 0:
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if random.randint(0, 2) == 1:
                    cells[(x, y)] = ALIVE

                else:
                    cells[(x, y)] = DEAD

    for y in range(HEIGHT):
        for x in range(WIDTH):
            # print(cells[x,y], end='')
            print(cells[x, y], end="")

        print()

    print("Press cntrol-C to quit  :::::::" + str(idk))
    for y in range(HEIGHT):
        for x in range(WIDTH):

            left = (x - 1) % WIDTH
            right = (x + 1) % WIDTH
            above = (y - 1) % HEIGHT
            below = (y + 1) % HEIGHT

            numNeighbors = 0
            if cells[(left, above)] == ALIVE:
                numNeighbors += 1  # Top-left neighbor is alive.
            if cells[(x, above)] == ALIVE:
                numNeighbors += 1  # Top neighbor is alive.
            if cells[(right, above)] == ALIVE:
                numNeighbors += 1  # Top-right neighbor is alive.
            if cells[(left, y)] == ALIVE:
                numNeighbors += 1  # Left neighbor is alive.
            if cells[(right, y)] == ALIVE:
                numNeighbors += 1  # Right neighbor is alive.
            if cells[(left, below)] == ALIVE:
                numNeighbors += 1  # Bottom-left neighbor is alive.
            if cells[(x, below)] == ALIVE:
                numNeighbors += 1  # Bottom neighbor is alive.
            if cells[(right, below)] == ALIVE:
                numNeighbors += 1  # Bottom-right neighbor is alive.

            # Set cell based on Conway's Game of Life rules:
            if cells[(x, y)] == ALIVE and (numNeighbors == 2 or numNeighbors == 3):
                # Living cells with 2 or 3 neighbors stay alive:
                nextCells[(x, y)] = ALIVE
            elif cells[(x, y)] == DEAD and numNeighbors == 3:
                # Dead cells with 3 neighbors become alive:
                nextCells[(x, y)] = ALIVE
            else:
                # Everything else dies or stays dead:
                nextCells[(x, y)] = DEAD

    try:
        pass
    except KeyboardInterrupt:
        print("Conway's Game of Life")
        print("By Al Sweigart al@inventwithpython.com")
        sys.exit()  # When Ctrl-C is pressed, end the program.
    idk += 1
