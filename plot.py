import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.patches as patches
import matplotlib.text as text
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


def circle_plot(fig, data):
    # Artists are scaled according to aspect ratio. We'll need to undo this to draw circles.
    xsize, ysize = fig.get_size_inches()
    yscale = xsize / ysize

    # This magic invisible line makes the figure show up
    fig.lines.append(lines.Line2D([0, 0], [0, 1], transform=fig.transFigure,
                                  figure=fig, color='white'))

    spacing = 1.0 / (len(data) + 1)
    radius = 0.8 * spacing
    smallest = min(*data)
    largest = max(*data)

    def scaled_radius(value):
        interp = (value - smallest) / (largest - smallest)
        return radius * (0.6 + interp * 0.4)

    for i, v in enumerate(data):
        x = (i + 0.5) * spacing
        y = 0.5
        r = scaled_radius(v)
        c = patches.Ellipse((x, y), r, yscale * r, transform=fig.transFigure, figure=fig,
                          fill=False)
        fig.patches.append(c)

        t = text.Text(x, y, str(v), transform=fig.transFigure, figure=fig,
                     verticalalignment='center', horizontalalignment='center',
                     fontsize=300 * r)
        fig.texts.append(t)
