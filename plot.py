import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import hypothesis.strategies as st
import sort


def plot_performance(sorts, input_sizes):
    """Create a plot of runtime for each sort with different input sizes.

Will graph each sort with each input size. Returns a matplotlib figure.
"""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for s in sorts:
        data = [(n,
                 sort.count_steps(s, st.lists(st.integers(),
                                              min_size=n, max_size=n)
                                  .example()))
                for n in input_sizes]
        ax.plot(*zip(*data))
    ax.legend([s.__name__ for s in sorts])
    plt.xlabel('Input Length')
    plt.ylabel('Steps')
    fig


def animated_bars(sort_func, data, interval):
    """Create a sort animation showing each list element as a vertical bar."""
    frames = []
    fig = plt.figure()

    def create_frame(*_):
        pic = plt.bar(x=range(len(data)), height=list(data), color='blue')
        plt.xticks([])
        plt.yticks([])
        frames.append(pic)

    sort.run(sort_func, data, create_frame)
    create_frame()              # Final state
    return ArtistAnimation(fig, frames, interval=interval)
