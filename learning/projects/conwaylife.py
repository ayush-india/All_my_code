import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x = np.array([[0, 0, 255], [255, 255, 0], [0, 255, 0]])
plt.imshow(x, interpolation="nearest")
plt.show()
