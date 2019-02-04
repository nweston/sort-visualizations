import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sort


def plot_performance(sorts, input_sizes):
    """Create a plot of runtime for each sort with different input sizes.

Will graph each sort with each input size. Returns a matplotlib figure.
"""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for s in sorts:
        data = [(n, sort.count_steps(s, sort.random_list(n)))
                for n in input_sizes]
        ax.plot(*zip(*data))
    ax.legend([s.__name__ for s in sorts])
    plt.xlabel('Input Length')
    plt.ylabel('Steps')


def animated_bars(sort_func, data, interval):
    """Create a sort animation showing each list element as a vertical bar."""

    # Run the entire sort, remembering all intermediate states
    states = [list(data)]
    def save_state(*_):
        states.append(list(data))

    sort.run(sort_func, data, save_state)
    save_state() # Final state

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    bars = ax.bar(x=range(len(data)), height=list(data))
    plt.xticks([])
    plt.yticks([])
    plt.close()

    def animate(i):
        for b, h in zip(bars, states[i]):
            b.set_height(h)
        return bars

    return FuncAnimation(fig, animate, frames=len(states), interval=interval)
