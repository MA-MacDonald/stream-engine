from collections import deque
from itertools import zip_longest as zipl
from matplotlib.animation import TimedAnimation


class StreamAnimation(TimedAnimation):
    def __init__(self, fig, **kwargs):
        self._stream_bundle = []
        TimedAnimation.__init__(self, fig, blit=True, **kwargs)

    def _step(self, *args):
        self._draw_next_frame(True, self._blit)
        return True

    def _draw_frame(self, framedata):
        self._drawn_artists = []
        for stream in self._stream_bundle:
            self._drawn_artists.extend([stream.proc(thread, data)
                                        for thread, data
                                        in zip(stream.threads, stream.func())])

        for a in self._drawn_artists:
            a.set_animated(self._blit)

    def add_stream(self, *streams):
        for stream in streams:
            self._stream_bundle.append(stream)

    def new_frame_seq(self):
        pass


class Stream:
    def __init__(self, ax, func, proc=None, style=None):
        self.func = func
        self.threads = self._build_threads(ax, style)
        self.proc = proc if proc else self.stream_proc

    def _build_threads(self, ax, style):
        styles = {} if not style else style
        return [self._new_thread(ax, style)
                for style, _
                in zipl(styles, self.func(), fillvalue={})]

    def _new_thread(self, ax, style):
        xmin, xmax = ax.get_xlim()
        length = int(abs(xmin - xmax))
        data = deque([float('nan')] * length, length)
        line, = ax.plot(range(length), data, **style)
        return {'line': line, 'data': data}

    # default data processor
    def stream_proc(self, thread, data):
        thread['data'].appendleft(data)
        thread['line'].set_ydata(thread['data'])
        return thread['line']
