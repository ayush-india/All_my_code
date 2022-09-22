from matplotlib import pyplot as plt
import numpy as np
import numba as nb

# Get Range to Check
top_range = int(input("Top Range: "))


@nb.njit("int64[:](int_)")
def collatz(top_range):
    # Initialize mem
    mem = np.zeros(top_range + 1, dtype=np.int64)
    for start in range(2, top_range + 1):
        # If mod4 == 1: (3x + 1)/4
        if start % 4 == 1:
            mem[start] = mem[(start + (start >> 1) + 1) // 2] + 3

        # If 4mod == 3: 3(3x + 1) + 1 and continue
        elif start % 4 == 3:
            num = start + (start >> 1) + 1
            num += (num >> 1) + 1
            count = 4

            while num >= start:
                if num % 2:
                    num += (num >> 1) + 1
                    count += 2
                else:
                    num //= 2
                    count += 1
            mem[start] = mem[num] + count

        # If 4mod == 2 or 0: x/2
        else:
            mem[start] = mem[(start // 2)] + 1

    print(mem)


mem = collatz(top_range)
# # Plot each starting number with the length of it's sequence
# plt.scatter([*range(1, len(mem) + 1)], mem, color = 'black', s = 1)
# plt.show()
