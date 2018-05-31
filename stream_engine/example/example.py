import matplotlib.pyplot as plt
from stream_engine.stream import Stream, StreamAnimation
from matplotlib.ticker import FuncFormatter, FormatStrFormatter

base_style = {'figure.facecolor': '2d2d2d',
              'axes.facecolor': '404040',
              'axes.labelcolor': 'b0bdbb',
              'axes.prop_cycle': "cycler('color', ['74af60', '49b6d2', 'db4743', 'eba92b'])",
              'axes.grid': 'True',
              'grid.color': '343434',
              'grid.linestyle': '-',
              'grid.linewidth': '1.0',
              'text.color': 'b0bdbb',
              'xtick.color': 'efefef',
              'ytick.color': 'efefef'}

ave_style = [{'label': 'cpu average'}]

cpu_style = [{'label': 'cpu1'},
             {'label': 'cpu2'},
             {'label': 'cpu3'},
             {'label': 'cpu4'}]

mem_style = [{'label': 'main', 'color': '#49b6d2'},
             {'label': 'swap', 'color': '#db4743'}]


def config(*args):
    def x_format(x, pos):
        return '%1.0f' % abs(x / 10)
    for ax in args:
        ax.xaxis.set_major_formatter(FuncFormatter(x_format))
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f%%'))
        ax.set_xlabel('Time (s)')

        leg = ax.legend(loc=9, ncol=6, framealpha=.2)
        for text in leg.get_texts():
            text.set_color('w')

with plt.style.context(base_style):
    fig = plt.figure(figsize=(8, 5))
    ax1 = fig.add_subplot(311)
    ax1.set_xlim(0, 600)
    ax1.set_ylim(0, 100)

    ax2 = fig.add_subplot(312)
    ax2.set_xlim(0, 600)
    ax2.set_ylim(0, 100)

    ax3 = fig.add_subplot(313)
    ax3.set_xlim(0, 600)
    ax3.set_ylim(0, 100)


if __name__ == '__main__':
    from psutil import cpu_percent, virtual_memory, swap_memory

    def cpu_percents():
        return cpu_percent(percpu=True)

    def cpu_average():
        return [cpu_percent()]

    def memory_percent():
        return virtual_memory().percent, swap_memory().percent

    ave_stream = Stream(ax1, cpu_average, buffer=5, style=ave_style)
    cpu_stream = Stream(ax2, cpu_percents,  buffer=5, style=cpu_style, filt=True)
    mem_stream = Stream(ax3, memory_percent, buffer=5, style=mem_style)

    config(ax1, ax2, ax3)

    anim = StreamAnimation(fig, interval=100)
    anim.add_stream(ave_stream, cpu_stream, mem_stream)

    plt.tight_layout()
    plt.show()
