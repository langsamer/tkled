from time import perf_counter


class Blinker:
    def __init__(self, after=None, period=500, indfunc=None):
        self.after = after or (lambda *args: None)
        self.indfunc = indfunc or (lambda: None)
        self.period = period

    def action(self):
        before = perf_counter()
        self.indfunc()
        now = perf_counter()
        print("[{}] Blinker {!r} is active".format(now-before, self))
        self.after(self.period, self.action)


class Eventer:
    def __init__(self, after=None, period=500, indicate_func=None):
        self.indicate = indicate_func or (lambda *args: None)
        self.after = after or (lambda *args: None)
        self.period = period

    def action(self):
        self.indicate('Info', 'Lights')
        self.after(self.period, self.action2)

    def action2(self):
        self.indicate('Info', 'Camera')
        self.after(self.period, self.action3)

    def action3(self):
        self.indicate('Alert', 'Action', 'whoop! whoop!')
