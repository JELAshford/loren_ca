"""Recreate loren's CA from this skeet: https://bsky.app/profile/lorenschmidt.bsky.social/post/3lnnnrx3ea22l"""

from scipy.signal import convolve2d
import matplotlib.pylab as plt
import numpy as np


SEED = 1701
STEPS = 10

rules = np.array(
    [
        [2, 2, 2, 2, 0],
        [2, 1, 0, 0, 0],
        [1, 1, 0, 2, 0],
        [0, 2, 1, 0, 1],
        [2, 2, 2, 2, 0],
    ]
)

orthog_kernel = [
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0],
]
diag_kernel = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

rng = np.random.default_rng(SEED)
grid = rng.integers(0, 2, size=(100, 100))

for step in range(STEPS):
    orthog_counts = convolve2d(grid, orthog_kernel, mode="same")
    diag_counts = convolve2d(grid, diag_kernel, mode="same")

    new_grid = rules[orthog_counts, diag_counts]
    new_grid[new_grid == 2] = grid[new_grid == 2]
    grid = new_grid
    plt.imshow(grid, cmap="gray")
    plt.show()

plt.imshow(grid, cmap="gray")
plt.savefig("out/final_state.png", dpi=200)
plt.close()
