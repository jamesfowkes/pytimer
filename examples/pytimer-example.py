import time
import logging
import random

from pytimer import Timer, INFINITE_REPEATS

start_time_ms = time.time() * 1000

logging.basicConfig(level=logging.INFO)

def run_time_ms():
	return (time.time() * 1000) - start_time_ms

def example_1_runs_forever():
	print("Function 1 at {}".format(run_time_ms()))

def example_2_runs_five_times():
	print("\tFunction 2 at {}".format(run_time_ms()))

def example_3_runs_10_times_at_slightly_randomised_interval():
	print("\t\tFunction 3 at {}".format(run_time_ms()))


if __name__ == "__main__":

	timer = Timer(run_time_ms)

	timer.add_function("Example 1 task", example_1_runs_forever, INFINITE_REPEATS, 1300, None)
	timer.add_function("Example 2 task", example_2_runs_five_times, 5, 2000, None)
	timer.add_function("Example 3 task", example_3_runs_10_times_at_slightly_randomised_interval, 10, 3000, lambda: random.randint(-1000, 1000))
