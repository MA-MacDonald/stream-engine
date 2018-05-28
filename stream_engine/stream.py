from collections import deque
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib.animation import FuncAnimation


class StreamAnimation(FuncAnimation):
    """
    StreamAnimation is an extension of matplotlib Animation class,
    this class facilitates plotting of real time streaming data.

    Args:
        fig (matplotlib.figure.Figure): The figure to use.
    Keyword arguments:
        interval (number):  optional
            Delay between frames in milliseconds.  Defaults to 200.
    """

    def __init__(self, fig, **kwargs):
        self._stream_bundle = []
        FuncAnimation.__init__(self, fig, None, blit=True, **kwargs)

    def _draw_frame(self, framedata):
        # self._save_seq.append(framedata)
        # self._save_seq = self._save_seq[-self.save_count:]

        self._drawn_artists = []
        for stream in self._stream_bundle:
            stream_data = stream.func()
            self._drawn_artists.extend([stream.proc(thread, data)
                                        for thread, data
                                        in zip(stream.threads, stream_data)])

        for a in self._drawn_artists:
            a.set_animated(self._blit)

    def add_stream(self, *streams):
        for stream in streams:
            self._stream_bundle.append(stream)


class Stream:
    """
    The data structure used for plotting to a StreamAnimation.

    A Stream holds data, settings and, instructions
    for a StreamAnimation object to process.

    Args:
        ax (matplotlib.axes._subplots.AxesSubplot):
                        The AxesSubplot the Stream will be associated with.
        func (callable): The function that returns new data to be plotted.

    Keyword arguments:
        proc (callable): A function that processes a thread and returns it.
        buffer (int): Extends the data so the beginning and end
                        of the streaming data is not plotted
                        default: buffer='0'
        filt (bool): Used to filter noisy data.
                        gaussian_filter1d is applied.
                        default: filt=False
        s_len (int): The number of data points the stream holds.
                        default: s_len=600
        style (dict): A dict containing matplotlib styles which will
                        be applied to each line in the thread group.
                        default: style=None
                        example: {'linestyle': '-', 'color': 'b'}
        group_style (list): A list of dicts containing matplotlib styles
                        which will be applied sequentially to each
                        corresponding line in the thread group.
                        default=None
                        example:
                            [{'linestyle': '-', 'color': 'r'},
                             {'linestyle': '--', 'color': 'g'},
                             {'linestyle': ':', 'color': 'b'}]
       """

    def __init__(self, ax, func, **kwargs):
        _allowed_keys = ['s_len', 'buffer', 'proc', 'style', 'group_style', 'filt']
        self._init_keys(_allowed_keys, **kwargs)

        self.ax = ax
        self.func = func
        self.threads = self._init_thread()

        # Sets default data processor if one is not supplied.
        if self.proc is None:
            self.proc = self.stream_proc
            if self.filt:
                self.proc = self.filt_proc

    # Initialize keyword args, defaults to None.
    def _init_keys(self, keys, **kwargs):
        for key in keys:
            setattr(self, key, None)
        for key, value in kwargs.items():
            if key in keys:
                setattr(self, key, value)
            else:
                raise ValueError("unexpected kwarg value", key)

    # Creates the proper number of threads for
    # based on the return data of self.func
    def _init_thread(self):
        style = self.style
        group_style = self.group_style

        if group_style:
            if len(group_style) != len(self.func()):
                raise Exception('gp_style must be the same length as func()')
            return [self._new_thread(self.ax, style) for style in group_style]
        elif style:
            return [self._new_thread(self.ax, style) for _ in self.func()]
        else:
            return [self._new_thread(self.ax, {}) for _ in self.func()]

    def _new_thread(self, ax, style=None):
        buffer = self.buffer if self.buffer else 0
        buf1 = buffer
        buf2 = buffer * 2
        xmin, xmax = ax.get_xlim()
        length = int(abs(xmin - xmax))

        data = deque([float('nan')] * (length + buf2), length + buf2)
        line = ax.plot(range(-buf1, length + buf1), data, **style)[0]
        return {'line': line, 'data': data}

    # default filtered data processor
    @staticmethod
    def filt_proc(thread, data):
        thread['data'].appendleft(data)
        thread['line'].set_ydata(gaussian_filter1d(thread['data'], 3))
        return thread['line']

    # default data processor
    @staticmethod
    def stream_proc(thread, data):
        thread['data'].appendleft(data)
        thread['line'].set_ydata(thread['data'])
        return thread['line']
