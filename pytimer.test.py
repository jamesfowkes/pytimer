import unittest
import time

from pytimer import TimedFunction, INFINITE_REPEATS

class PyTimerTest(unittest.TestCase):
    
    def callback(self):
        self.callback_count += 1

    def random_provider(self):
        return 4

    def test_make_classmethod_returns_scheduled_function_with_same_interval_and_next_time(self):
        obj = TimedFunction.make("TestFunction", self.callback, 1, 100, None, lambda: self.millis)

        self.assertEqual(TimedFunction, type(obj))

    def test_function_does_not_run_until_interval_has_elapsed(self):
        function = TimedFunction.make("TestFunction", self.callback, 1, 100, None, lambda: self.millis)

        self.assertEqual(1, function.repeats)

        self.millis = 99
        function = function.run()

        self.assertEqual(1, function.repeats)
        self.assertEqual(0, self.callback_count)

        self.millis = 100
        function = function.run()

        self.assertEqual(0, function.repeats)
        self.assertEqual(1, self.callback_count)

    def test_function_increments_next_time_when_run(self):
        function = TimedFunction.make("TestFunction", self.callback, 1, 100, None, lambda: self.millis)

        self.assertEqual(100, function.next_time)

        self.millis = 100

        function = function.run()

        self.assertEqual(200, function.next_time)

    def test_function_runs_over_many_intervals(self):
        function = TimedFunction.make("TestFunction", self.callback, INFINITE_REPEATS, 100, None, lambda: self.millis)

        for expected_count in range(1, 10):
            self.millis += 100
            function = function.run()
            self.assertEqual(expected_count, self.callback_count)

    def test_function_runs_exactly_number_of_times_specified(self):

        function = TimedFunction.make("TestFunction", self.callback, 5, 100, None, lambda: self.millis)

        for _ in range(1, 10):
            self.millis += 100
            function = function.run()
        
        self.assertEqual(5, self.callback_count)

    def test_function_uses_randomiser_when_provided(self):

        function = TimedFunction.make("TestFunction", self.callback, 5, 100, self.random_provider, lambda: self.millis)

        self.assertEqual(104, function.next_time)

        self.millis = 104

        function = function.run()

        self.assertEqual(208, function.next_time)

    def setUp(self):
        self.callback_count = 0
        self.millis = 0

if __name__ =="__main__":
    unittest.main()