"""Recreate loren's CA from this skeet: https://bsky.app/profile/lorenschmidt.bsky.social/post/3lnnnrx3ea22l"""

from scipy.signal import convolve2d
from mediapy import VideoWriter
import matplotlib.pylab as plt
import numpy as np


SEED = 1701
STEPS = 500
SIZE = 200
SHOW_SIZE = 800
SHOW_SCALE = SHOW_SIZE // SIZE


orthog_kernel = [
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0],
]

diag_kernel = [
    [1, 0, 1],
    [0, 0, 0],
    [1, 0, 1],
]


# Setup state
rules = np.array(
    [
        [2, 2, 2, 2, 0],
        [2, 1, 0, 0, 0],
        [1, 1, 0, 2, 0],
        [0, 2, 1, 0, 1],
        [2, 2, 2, 2, 0],
    ],
    dtype=np.uint8,
)
rng = np.random.default_rng(SEED)
grid = rng.integers(0, 2, size=(SIZE, SIZE), dtype=np.uint8)


# Apply rules and save to video
with VideoWriter("out/video.mp4", (SHOW_SIZE, SHOW_SIZE), fps=60) as writer:
    for step in range(STEPS):
        # Count neighbour (orthog and diagonal)
        orthog_counts = convolve2d(grid, orthog_kernel, mode="same")
        diag_counts = convolve2d(grid, diag_kernel, mode="same")
        # Set new state based on counts/rules
        new_grid = rules[orthog_counts, diag_counts]
        new_grid[new_grid == 2] = grid[new_grid == 2]
        # Update state
        grid = new_grid
        # Add to video
        show_grid = np.kron(new_grid, np.ones((SHOW_SCALE, SHOW_SCALE))) * 255
        writer.add_image(show_grid)


# Show final state
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.imshow(grid, cmap="gray")
ax.set_xticks([])
ax.set_yticks([])
plt.tight_layout()
plt.savefig("out/final_state.png", dpi=200, bbox_inches="tight")
plt.close()
