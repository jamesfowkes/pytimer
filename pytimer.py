import multiprocessing
import logging

from collections import namedtuple

TimedFunctionTuple = namedtuple("TimedFunctionTuple", ["name", "fn", "repeats", "interval", "next_time", "random", "ms_provider"])

INFINITE_REPEATS = -1


def get_runner(fn):

    def runner():
        nonlocal fn
        while(True):
            fn = fn.run()

    return runner

class Timer:

    def __init__(self, ms_provider):
        self.jobs = []
        self.ms_provider = ms_provider

    def add_function(self, name, fn, repeats, interval, random):
        fn = TimedFunction.make(name, fn, repeats, interval, random, self.ms_provider)
        p = multiprocessing.Process(target = get_runner(fn))
        self.jobs.append(p)
        p.start()

class TimedFunction(TimedFunctionTuple):
    __slots__ = ()

    def __repeat_str__(self):
        return "indefinitely" if self.repeats == INFINITE_REPEATS else "{} times".format(self.repeats)

    def __str__(self):
        return "Task '{}' calling {} every {}ms ({})".format(self.name, self.fn.__name__, self.interval, self.__repeat_str__)

    def should_run(self):
        return self.repeats > 0 or self.repeats == INFINITE_REPEATS

    def next_repeat_number(self):
        if self.repeats > 0:
            return self.repeats - 1
        elif self.repeats == INFINITE_REPEATS:
            return INFINITE_REPEATS
        else:
            return 0

    def get_random_delta(self):
        return self.random() if self.random is not None else 0

    def run(self):

        new_fn = self

        if self.should_run() and (self.ms_provider() >= self.next_time):
            new_repeats = self.next_repeat_number()
            new_time = self.next_time + self.interval + self.get_random_delta()
            self.fn()
            new_fn = TimedFunction(self.name, self.fn, new_repeats, self.interval, new_time, self.random, self.ms_provider)

        return new_fn

    @classmethod
    def make(cls, name, fn, repeats, interval, random, ms_provider):

        if random is not None:
            next_time = interval + random()
        else:
            next_time = interval

        return cls(name, fn, repeats, interval, next_time, random, ms_provider)
