# StreamEngine
StreamEngine is an extention of the matplotlib Animation class which enables the user to easily plot real time streaming data.
[![StreamEngine Example](https://i.imgur.com/lM6gSEc.png)](https://www.youtube.com/watch?v=bgwOTcpNV9Q)
## Install  
`pip install stream_engine`

## Basic Example
```Python
import matplotlib.pyplot as plt
from stream_engine.stream import Stream, StreamAnimation

if __name__ == '__main__':
    from psutil import cpu_percent

    def cpu_average():
        return [cpu_percent()]


    fig = plt.figure(figsize=(10, 3))
    ax1 = fig.add_subplot(111)
    ax1.set_xlim(0, 600)
    ax1.set_ylim(0, 100)

    anim = StreamAnimation(fig, interval=100)
    anim.add_stream(Stream(ax1, cpu_average))

    plt.tight_layout()
    plt.show()
```
![StreamEngine Example](https://i.imgur.com/ADOYrDv.png)

## Multi-Stream Example
The above exmaple graphs one stream of data (one line). This is because the data function we defined only returns one value.  
A new stream is created for each value in a list retured by the defined data function.  
**Note:** A data function must return a list of data. The above data function returns one value so we bracket the return value.

For example if we were to create a new function that returns the % for each individual cpu instead of the average...
```Python
from psutil import cpu_percent
def all_cpus():
    return cpu_percent(percpu=True)  # Note: we do not have to bracket the return because 
                                     # psutil.cpu_percent(percpu=True) returns a list by default.
```
Now lets create a new Stream with our new data function and add it to our StreamAnimation object `anim`.  
```Python
ave_stream = Stream(ax1, cpu_average)
cpus_stream = Stream(ax1, all_cpus)
anim.add_stream(ave_stream, cpu_stream)
```
![StreamEngine Example](https://i.imgur.com/3ALvZ1m.png)
ok, neat! but that data looks kinda crazy. Lets turn the filter on and see what happens.

```Python
ve_stream = Stream(ax1, cpu_average)
cpus_stream = Stream(ax1, all_cpus, filt=True)  # just add filt=True to filter this stream.
anim.add_stream(ave_stream, cpus_stream)
```
Now the `all_cpus_stream` stream is being filtered by applying a gaussian filter to smooth the data. While the `total_ave_stream` stream remains unfiltered.  
![StreamEngine Example](https://i.imgur.com/RZpHlHS.png)

The data now looks much cleaner. Ok now lets put each stream on its own axes.  
```Python
# Just create a new axes and reassign one of the streams to the new axes.
ax1 = fig.add_subplot(211)    # change the fig configuration to hold more than one plot
ax1.set_xlim(0, 500)
ax1.set_ylim(0, 100)

ax2 = fig.add_subplot(212)
ax2.set_xlim(0, 500)
ax2.set_ylim(0, 100)

ave_stream = Stream(ax1, cpu_average)
cpus_stream = Stream(ax2, all_cpus, filt=True)  # change to ax2
anim.add_stream(ave_stream, cpus_stream)
```
![StreamEngine Example](https://i.imgur.com/9IXyoRC.png)

## Styles
Each Stream line can be styled like any other matplotlib line.
```Python
# a style should be passed as a list containing dicts eg.--> style=[{'color': 'r', 'label': 'foo'}]

# for single streams
ave_style = [{'linestyle': '--', 'label': 'cpu average'}]
ave_stream = Stream(ax1, cpu_average, style=ave_style)

# for multiple streams.
cpus_style = [{'linestyle': '-', 'label': 'cpu1'},
              {'linestyle': '-', 'label': 'cpu2'},
              {'linestyle': '-', 'label': 'cpu3'},
              {'linestyle': '-', 'label': 'cpu4'}]
cpus_stream = Stream(ax2, all_cpus, filt=True, style=cpus_style)

ax1.legend(loc=9)
ax2.legend(loc=9, ncol=4)
```
<img src="media/ex5.gif" width="400"/>

## Taking it further.
ok now lets add a new stream that represents our computers memory usage.
```python
# Lets make our new data function that returns our computers memory usage.
from psutil import cpu_percent, virtual_memory, swap_memory

def memory_percent():
    return virtual_memory().percent, swap_memory().percent   # returns a tuple of data which is also exceptable.
    
# We want this stream to be on its own axes so make a new one.
ax3 = fig.add_subplot(313)  # change ax1 and ax2 to proper spot on a 3x1 figure.
ax3.set_xlim(0, 500)
ax3.set_ylim(0, 100)
    
# Lets create our Stream object.
# Lets also create a group style for it while we're at it. 
mem_style = [{'linestyle': '--', 'label': 'main', 'color': 'g'},
             {'linestyle': '--', 'label': 'swap', 'color': 'r'}]
mem_stream = Stream(ax3, mem_percent, group_style=mem_style)
ax3.legend(loc=9, ncol=2)

# Add to our StreamAnimation object.
 anim.add_stream(ave_stream, cpus_stream, mem_stream)
```

<img src="media/ex6.gif" width="400"/>

## Putting it all together

```Python
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
```
![StreamEngine Example](media/ex9.png)




